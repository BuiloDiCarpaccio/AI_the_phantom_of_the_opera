from ...definition import AbstractCharacter
from ...server import CharacterType
from .character_black import CharacterBlack
from .character_blue import CharacterBlue
from .character_brown import CharacterBrown 
from .character_grey import CharacterGrey
from .character_pink import CharacterPink
from .character_purple import CharacterPurple
from .character_red import CharacterRed
from .character_white import CharacterWhite


def character_factory(state: CharacterType) -> AbstractCharacter:
    return {
        'black':    CharacterBlack,
        'blue':     CharacterBlue,
        'brown':    CharacterBrown,
        'grey':     CharacterGrey,
        'pink':     CharacterPink,
        'purple':   CharacterPurple,
        'red':      CharacterRed,
        'white':    CharacterWhite
    }[state['color']](state)
