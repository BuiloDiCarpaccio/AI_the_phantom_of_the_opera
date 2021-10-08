import typing
from .character import Character
from definition import AbstractGameLogic, AbstractGameState, CharacterStatus, InternalQuestion
from server import CharacterType


class CharacterBlue(Character):

    def __init__(self, state: CharacterType) -> None:
        super().__init__(state)
        self._post_movement_power = CharacterStatus.MANDATORY

    def get_power_possibilities(self, game_logic: AbstractGameLogic, game_state: AbstractGameState) -> typing.Tuple[InternalQuestion, tuple]:
        if len(game_state.lane_blocked) == 2:
            available_rooms = [room for room in range(10)]
            return (InternalQuestion.ENTRANCE_BLOCKED, available_rooms)


        passages_work = game_logic.PASSAGES[game_state.lane_blocked[0]].copy()
        available_exits = list(passages_work)
        game_state._end_of_turn = True
        return (InternalQuestion.EXIT_BLOCKED, available_exits)

    def reset(self) -> None:
        self._movement = CharacterStatus.AVAILABLE
        self._end_of_turn = False
        self._post_movement_power = CharacterStatus.MANDATORY
