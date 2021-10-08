from .character import Character
from definition import CharacterStatus
from server import CharacterType



class CharacterPink(Character):

    def __init__(self, state: CharacterType) -> None:
        super().__init__(state)

    def reset(self) -> None:
        self._movement = CharacterStatus.AVAILABLE
        self._end_of_turn = False

