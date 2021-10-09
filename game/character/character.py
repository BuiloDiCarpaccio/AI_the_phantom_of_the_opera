import typing
from definition import AbstractCharacter, AbstractGameLogic, AbstractGameState, CharacterStatus, InternalQuestion
from server import CharacterType


class Character(AbstractCharacter):

    def __init__(self, state: CharacterType) -> None:
        self._color = state['color']
        self._position = state['position']
        self._power = state['power']
        self._suspect = state['suspect']
        self._movement = CharacterStatus.AVAILABLE
        self._post_movement_power = CharacterStatus.NOT_AVAILABLE
        self._pre_movement_power = CharacterStatus.NOT_AVAILABLE
        self._character_to_move = None
        self._end_of_turn = False

    def get_power_possibilities(self, game_logic: AbstractGameLogic, game_state: AbstractGameState) -> typing.Tuple[InternalQuestion, tuple]:
        pass

    def reset(self) -> None:
        pass

    def serialize(self) -> list:
        return [self._position, self._suspect]
