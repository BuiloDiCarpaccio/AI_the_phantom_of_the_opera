import typing
from .character import Character
from ...definition import AbstractGameLogic, AbstractGameState, CharacterStatus, InternalQuestion
from ...server import CharacterType


class CharacterBrown(Character):

    def __init__(self, state: CharacterType) -> None:
        super().__init__(state)
        self._character_to_move = None
        self._pre_movement_power = CharacterStatus.AVAILABLE

    def get_power_possibilities(self, game_logic: AbstractGameLogic, game_state: AbstractGameState) -> typing.Tuple[InternalQuestion, tuple]:
        available_characters = [character for character in game_state.characters if
                                        game_state.actual_card.position == character.position if
                                        character.color != "brown"]
        available_colors = [character.color for character in available_characters]
        return InternalQuestion.TAKE_AWAY, available_colors

    def reset(self) -> None:
        self._movement = CharacterStatus.AVAILABLE
        self._end_of_turn = False
        self._pre_movement_power = CharacterStatus.AVAILABLE
