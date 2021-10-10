import typing
from .character import Character
from ...definition import AbstractGameLogic, AbstractGameState, CharacterStatus, InternalQuestion
from ...server import CharacterType



class CharacterGrey(Character):

    def __init__(self, state: CharacterType) -> None:
        super().__init__(state)
        self._post_movement_power = CharacterStatus.MANDATORY

    def get_power_possibilities(self, game_logic: AbstractGameLogic, game_state: AbstractGameState) -> typing.Tuple[InternalQuestion, tuple]:
        available_rooms = [room for room in range(10) if room is not game_state.room_shadow]
        game_state._end_of_turn = True
        return (InternalQuestion.ROOM_SHADOW, available_rooms)

    def reset(self) -> None:
        self._movement = CharacterStatus.AVAILABLE
        self._post_movement_power = CharacterStatus.MANDATORY
