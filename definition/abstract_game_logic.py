import abc
import typing
from .abstract_game_state import AbstractGameState
from .enumeration import InternalQuestion


class AbstractGameLogic(metaclass=abc.ABCMeta):

    def apply_possibility(self, question_data: InternalQuestion, move, game_state):
        pass

    def get_next_possibilities(self, game_state: AbstractGameState) -> typing.Tuple[InternalQuestion, tuple]:
        pass
