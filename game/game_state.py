import random
from definition import AbstractGameState
from server import GameStateType
from game import character_factory
import csv
import copy
import fnmatch
import itertools

from definition.enumeration import CharacterStatus


class GameState(AbstractGameState):

    def __init__(self, state: GameStateType, character: str, question: str):
        self._active_cards = []
        self._actual_card  = None 
        self._alibi_cards = ['fantom-card', 'fantom-card']
        self._carlotta_end = state['exit']
        self._carlotta_position = state['position_carlotta']
        self._characters = []
        self._end_of_turn = False
        self._fantom = None
        self._lane_blocked = state['blocked']
        self._player = state.get('fantom', 'inspector')
        self._turn = state['num_tour']
        self._room_shadow = state['shadow']

        self._initialise_characters(state)
        self._initialise_character_cards(state)
        self._initialise_fantom(state)
        self._initialise_alibi_cards()
        self._initialise_actual_card(character, question)

    def _initialise_characters(self, state: GameStateType) -> None:
        for character_state in state['characters']:
            self._characters.append(character_factory(character_state))

    def _initialise_character_cards(self, state: GameStateType) -> None:
        for card_state in state['active character_cards']:
            for character in self._characters:
                if character.color == card_state['color']:
                    self._active_cards.append(character)

    def _initialise_fantom(self, state: GameStateType) -> None:
        if self._player == 'inspector':
            self._fantom = random.choice([character for character in self._characters if character.suspect])
        else:
            self._fantom = self._player

    def _initialise_alibi_cards(self) -> None:
        for character in self._characters:
            if character.color != self._fantom:
                self._alibi_cards.append(character)

    def _initialise_actual_card(self, actual_character: str, question: str) -> None:
        if actual_character != None:
            for character in self._characters:
                if character.color == actual_character:
                  self._actual_card = character

        if question == "select position":
            self._actual_card.pre_movement_power = CharacterStatus.NOT_ACTIVATED
        elif question == "activate brown power":
            return
        elif question == "brown character power":
            self._actual_card.pre_movement_power = CharacterStatus.ACTIVATED
        elif question == "blue character power room":
            self._actual_card.movement = CharacterStatus.ACTIVATED
        elif question == "blue character power exit":
            self._actual_card.movement = CharacterStatus.ACTIVATED
        elif question == "grey character power":
            self._actual_card.movement = CharacterStatus.ACTIVATED
            self._actual_card.post_movement_power = CharacterStatus.ACTIVATED
        elif question == "white character power move *":
            self._actual_card.movement = CharacterStatus.ACTIVATED
            self._actual_card.post_movement_power = CharacterStatus.ACTIVATED
        elif question == "purple character power":
            self._actual_card.pre_movement_power = CharacterStatus.ACTIVATED
        elif fnmatch.fnmatch(question, "activate * power"):
            self._actual_card.movement = CharacterStatus.ACTIVATED

    def shuffle_characters(self) -> None:
        random.shuffle(self._characters)

    def serialize(self) -> list:
        serialized = [
            self._actual_card.color,
            self._carlotta_position,
            self._lane_blocked,
            self._room_shadow,
        ]
        characters = copy.deepcopy(self._characters)
        characters.sort(key=lambda x: x.color)
        for character in characters:
            character_serialized = character.serialize()
            if character in self._alibi_cards:
                character_serialized.append(1)
            else:
                character_serialized.append(0)

            if character in self._active_cards:
                character_serialized.append(1)
            else:
                character_serialized.append(0)

            serialized.extend(character_serialized)
        
        return serialized

    def write_csv(self, rows: list):
        rows = list(i for i,_ in itertools.groupby(rows))
        with open('winrate.csv', 'a') as f:
            write = csv.writer(f)
            write.writerows(rows)

