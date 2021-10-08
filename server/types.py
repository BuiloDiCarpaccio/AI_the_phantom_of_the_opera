from dataclasses import dataclass
from typing import List


@dataclass
class CharacterType:
    color:      str
    position:   int
    power:      bool
    suspect:    bool

@dataclass
class GameStateType:
    active_character_cards:     List[CharacterType]
    blocked:                    List[int]
    characters:                 List[CharacterType]
    exit:                       int
    num_tour:                   int
    position_carlotta:          int
    shadow:                     int

@dataclass
class QuestionType:
    data:           list
    game_state:     GameStateType
    question:       str
