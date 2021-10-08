import abc
import typing
from definition import AbstractCharacter


class AbstractGameState(metaclass=abc.ABCMeta):

    @property
    def alibi_cards(self) -> AbstractCharacter:
        return self._alibi_cards

    @property
    def actual_card(self) -> AbstractCharacter:
        return self._actual_card

    @actual_card.setter
    def actual_card(self, card: AbstractCharacter) -> None:
        self._actual_card = card

    @property
    def active_cards(self) -> typing.Tuple[AbstractCharacter]:
        return self._active_cards

    @active_cards.setter
    def active_cards(self, active_cards: list) -> None:
        self._active_cards = list(active_cards)

    @property
    def carlotta_end(self) -> int:
        return self._carlotta_end

    @property
    def carlotta_position(self) -> int:
        return self._carlotta_position

    @carlotta_position.setter
    def carlotta_position(self, position: int) -> None:
        self._carlotta_position = position

    @property
    def characters(self) -> typing.Tuple[AbstractCharacter]:
        return tuple(self._characters)

    @property
    def end_of_turn(self) -> bool:
        return self._end_of_turn

    @end_of_turn.setter
    def end_of_turn(self, end_of_turn) -> None:
        self._end_of_turn = end_of_turn

    @property
    def lane_blocked(self) -> typing.List[int]:
        return self._lane_blocked

    @lane_blocked.setter
    def lane_blocked(self, lane_blocked: typing.List[int]) -> None:
        self._lane_blocked = lane_blocked

    @property
    def room_shadow(self) -> int:
        return self._room_shadow

    @room_shadow.setter
    def room_shadow(self, room_shadow: int) -> None:
        self._room_shadow = room_shadow

    @property
    def turn(self) -> int:
        return self._turn

    @turn.setter
    def turn(self, turn: int) -> None:
        self._turn = turn

    @property
    def fantom(self) -> AbstractCharacter:
        return self._fantom