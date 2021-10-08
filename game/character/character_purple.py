import typing
from .character import Character
from definition import AbstractGameLogic, AbstractGameState, CharacterStatus, InternalQuestion
from server import CharacterType


class CharacterPurple(Character):

    def __init__(self, state: CharacterType) -> None:
        super().__init__(state)
        self._pre_movement_power = CharacterStatus.AVAILABLE

    def get_power_possibilities(self, game_logic: AbstractGameLogic, game_state: AbstractGameState) -> typing.Tuple[InternalQuestion, tuple]:
        available_characters = [character for character in game_state.characters if
                                character.color != "purple"]
        available_colors = [character.color for character in available_characters]
        game_state._end_of_turn = True
        return InternalQuestion.EXCHANGE, available_colors

    def reset(self) -> None:
        self._movement = CharacterStatus.AVAILABLE
        self._end_of_turn = False
        self._pre_movement_power = CharacterStatus.AVAILABLE
