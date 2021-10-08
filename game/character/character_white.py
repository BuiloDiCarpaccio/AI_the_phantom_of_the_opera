import typing
from .character import Character
from definition import AbstractGameLogic, AbstractGameState, CharacterStatus, InternalQuestion
from server import CharacterType


class CharacterWhite(Character):

    def __init__(self, state: CharacterType) -> None:
        super().__init__(state)
        self._post_movement_power = CharacterStatus.AVAILABLE
    
    def get_power_possibilities(self, game_logic: AbstractGameLogic, game_state: AbstractGameState) -> typing.Tuple[InternalQuestion, tuple]:
        for moved_character in game_state.characters:
            if moved_character.position == game_state.actual_card.position and game_state.actual_card != moved_character:
                available_positions = game_logic.get_adjacent_positions(game_state.actual_card, game_state)

                # format the name of the moved character to string
                return getattr(InternalQuestion, f'MOVE_{moved_character.color.upper()}'), available_positions
            else:
                game_state._end_of_turn = True
                return InternalQuestion.NOTHING, []

    def reset(self) -> None:
        self._movement = CharacterStatus.AVAILABLE
        self._end_of_turn = False
        self._post_movement_power = CharacterStatus.MANDATORY
