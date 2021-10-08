import random
import typing
from definition import AbstractGameLogic, AbstractGameState, CharacterStatus, InternalQuestion


class GameLogic(AbstractGameLogic):

    PATTERN = ['inspector', 'fantom', 'fantom', 'inspector', 'fantom', 'inspector', 'inspector', 'fantom']
    PASSAGES = [{1, 4}, {0, 2}, {1, 3}, {2, 7}, {0, 5, 8}, {4, 6}, {5, 7}, {3, 6, 9}, {4, 9}, {7, 8}]
    PINK_PASSAGES = [{1, 4}, {0, 2, 5, 7}, {1, 3, 6}, {2, 7}, {0, 5, 8, 9}, {4, 6, 1, 8}, {5, 7, 2, 9}, {3, 6, 9, 1}, {4, 9, 5}, {7, 8, 4, 6}]

    def __init__(self) -> None:
        pass

    def _get_player_type(self, game_state: AbstractGameState):
        index = (game_state.turn + 1) % 8
        return GameLogic.PATTERN[index]

    def _fantom_appears(game_state: AbstractGameState):
        partition = [{ character for character in game_state.characters if character.position == i} for i in range(10)]
        if len(partition[game_state.fantom.position]) == 1 or game_state.fantom.position == game_state.room_shadow:
            # The fantom scream
            game_state.carlotta_position += 1
            for room, characters in enumerate(partition):
                if len(characters) > 1 and room != game_state.room_shadow:
                    for character in characters:
                        character.suspect = False
        else:
            # The fantom does not scream
            for room, characters in enumerate(partition):
                if len(characters) == 1 or room == game_state.room_shadow:
                    for character in characters:
                        character.suspect = False
        game_state.carlotta_position += len([character for character in game_state.characters if character.suspect])
        if game_state.carlotta_position >= game_state.carlotta_end:
            return InternalQuestion.END_GAME, 'fantom'
        elif len([character for character in game_state.characters if character.suspect]) <= 1:
            return InternalQuestion.END_GAME, 'inspector'
        return False, False

    def _get_moves(self, game_state: AbstractGameState):
        number_of_characters_in_room = sum([character.position == game_state.actual_card.position for character in game_state.characters])

        available_rooms = []
        available_rooms.append(self.get_adjacent_positions(game_state.actual_card, game_state))
        for step in range(1, number_of_characters_in_room):
            next_rooms = list()
            for room in available_rooms[step-1]:
                next_rooms += self.get_adjacent_positions_from_position(room,
                                                                        game_state.actual_card,
                                                                        game_state)
            available_rooms.append(next_rooms)
        temp = list()
        for sublist in available_rooms:
            for room in sublist:
                temp.append(room)
        temp = set(temp)
        available_positions = list(temp)
        if game_state.actual_card.position in available_positions:
            available_positions.remove(game_state.actual_card.position)

        return available_positions

    def get_adjacent_positions(self, charact, game_state):
        if charact.color == "pink":
            active_passages = self.PINK_PASSAGES
        else:
            active_passages = self.PASSAGES
        return [room for room in active_passages[charact.position] if set([room, charact.position]) != set(game_state.lane_blocked)]

    def get_adjacent_positions_from_position(self, position, charact, game_state):
        if charact.color == "pink":
            active_passages = self.PINK_PASSAGES
        else:
            active_passages = self.PASSAGES
        return [room for room in active_passages[position] if set([room, position]) != set(game_state.lane_blocked)]

    def _get_number_of_characters_in_room(self, game_state: AbstractGameState, room: int) -> int:
        index = 0

        for character in game_state.characters:
            index += int(room == character.position)
        return index - 1

    def _next_turn(self, game_state: AbstractGameState):
        game_state.end_of_turn = False
        game_state.actual_card = None
        game_state.turn = game_state.turn + 1

        if not game_state.active_cards:
            win, winner = GameLogic._fantom_appears(game_state)
            if win == InternalQuestion.END_GAME:
                return InternalQuestion.END_GAME, winner
            GameLogic._reset_round(game_state)
        return False, False

    def _reset_round(game_state: AbstractGameState):
        if (game_state.turn + 1) % 2 == 0:
            for character in game_state.characters:
                character.reset()
                game_state.shuffle_characters()
                game_state.active_cards = game_state.characters[:4]
        else:
            game_state.active_cards = game_state.characters[4:]

    def apply_possibility(self, question_data: InternalQuestion, move, game_state):
        if question_data == InternalQuestion.PICK_CARD:
            color_picked = move
            for character in game_state.characters:
                if character.color == color_picked:
                    game_state.actual_card = character
                    game_state.active_cards.remove(character)

        if question_data == InternalQuestion.MOVE:
            game_state.actual_card.movement = CharacterStatus.ACTIVATED
            new_position = move
            game_state.actual_card.position = new_position
            if game_state.actual_card.character_to_move != None:
                game_state.actual_card.character_to_move.position = new_position

        if question_data == InternalQuestion.ACTIVATE_PRE_MOVEMENT_POWER:
            game_state.actual_card.pre_movement_power = move

        if question_data == InternalQuestion.ACTIVATE_POST_MOVEMENT_POWER:
            game_state.actual_card.post_movement_power = move

        if question_data == InternalQuestion.ENTRANCE_BLOCKED:
            game_state.lane_blocked = [move]

        if question_data == InternalQuestion.EXIT_BLOCKED:
            lane_blocked = game_state.lane_blocked
            lane_blocked.append(move)
            game_state.lane_blocked = lane_blocked
        
        if question_data == InternalQuestion.TAKE_AWAY:
            c_to_follow = move
            for character in game_state.characters:
                if character.color == c_to_follow:
                    game_state.actual_card.character_to_move = character

        if question_data == InternalQuestion.EXCHANGE:
            target_color = move
            for character in game_state.characters:
                if character.color == target_color:
                    target_position = character.position
                    character.position = game_state.actual_card.position 
                    game_state.actual_card.position = target_position
        
        if question_data == InternalQuestion.ATTRACT:
            for character in game_state.characters:
                if character.position in self.get_adjacent_positions(game_state.actual_card, game_state):
                    character.position = game_state.actual_card.position

        if question_data == "Move *":
            color = question_data.split()
            for c in game_state.get_characters():
                if c.get_color() == color:
                    c.set_position = move
                    break

        if question_data == InternalQuestion.DRAW:
            draw = random.choice(game_state.alibi_cards)
            game_state.alibi_cards.remove(draw)
            if draw == "fantom-card":
                if self._get_player_type(game_state) == 'inspector':
                    game_state.carlotta_position -= 1
                else:
                    game_state.carlotta_position += 1
            elif self._get_player_type(game_state) == 'inspector':
                draw.suspect = False

        if question_data in [
            InternalQuestion.MOVE_BLACK,
            InternalQuestion.MOVE_BLUE,
            InternalQuestion.MOVE_BROWN,
            InternalQuestion.MOVE_GREY,
            InternalQuestion.MOVE_PINK,
            InternalQuestion.MOVE_PURPLE,
            InternalQuestion.MOVE_RED
            ]:
            color = question_data.name.split('_')[1].lower()
            for character in game_state.characters:
                if character.color == color:
                    character.position = move

    def get_next_possibilities(self, game_state: AbstractGameState) -> typing.Tuple[InternalQuestion, typing.Tuple]:
        if game_state._end_of_turn == True:
            win, winner = self._next_turn(game_state)
            if win == InternalQuestion.END_GAME:
                return InternalQuestion.END_GAME, [winner]

        if game_state.actual_card == None:
            return InternalQuestion.PICK_CARD, tuple(character.color for character in game_state.active_cards)
        if game_state.actual_card.pre_movement_power == CharacterStatus.AVAILABLE:
            if game_state.actual_card.color == 'brown' and self._get_number_of_characters_in_room(game_state, game_state.actual_card.position) == 0:
                game_state.actual_card.pre_movement_power = CharacterStatus.NOT_AVAILABLE
            else:
                return InternalQuestion.ACTIVATE_PRE_MOVEMENT_POWER, (CharacterStatus.NOT_ACTIVATED, CharacterStatus.ACTIVATED)
        if game_state.actual_card.pre_movement_power == CharacterStatus.ACTIVATED and game_state.actual_card.character_to_move == None:
            return game_state.actual_card.get_power_possibilities(self, game_state)
        if game_state.actual_card.movement == CharacterStatus.AVAILABLE:
            return InternalQuestion.MOVE, self._get_moves(game_state)
        if game_state.actual_card.post_movement_power == CharacterStatus.AVAILABLE:
            return InternalQuestion.ACTIVATE_POST_MOVEMENT_POWER, (CharacterStatus.NOT_ACTIVATED, CharacterStatus.ACTIVATED)
        if game_state.actual_card.post_movement_power in (CharacterStatus.ACTIVATED, CharacterStatus.MANDATORY):
            return game_state.actual_card.get_power_possibilities(self, game_state)
        game_state._end_of_turn = True
        return self.get_next_possibilities(game_state)
