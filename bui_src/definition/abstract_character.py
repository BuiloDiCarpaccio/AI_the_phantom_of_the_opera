import abc
from .enumeration import CharacterStatus


class AbstractCharacter(metaclass=abc.ABCMeta):

    @property
    def color(self) -> str:
        return self._color

    @property
    def suspect(self) -> bool:
        return self._suspect

    @suspect.setter
    def suspect(self, is_suspect: bool) -> None:
        self._suspect = is_suspect

    @property
    def movement(self) -> CharacterStatus:
        return self._movement

    @movement.setter
    def movement(self, character_status: CharacterStatus) -> None:
        self._movement = character_status

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, position: int) -> None:
        self._position = position

    @property
    def post_movement_power(self) -> CharacterStatus:
        return self._post_movement_power

    @post_movement_power.setter
    def post_movement_power(self, character_status: CharacterStatus) -> None:
        self._post_movement_power = character_status

    @property
    def pre_movement_power(self) -> CharacterStatus:
        return self._pre_movement_power

    @pre_movement_power.setter
    def pre_movement_power(self, character_status: CharacterStatus) -> None:
        self._pre_movement_power = character_status

    @property
    def character_to_move(self) -> 'AbstractCharacter':
        return self._character_to_move

    @character_to_move.setter
    def character_to_move(self, character: 'AbstractCharacter') -> None:
        self._character_to_move = character