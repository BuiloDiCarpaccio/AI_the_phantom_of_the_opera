from enum import Enum


class CharacterStatus(Enum):
    NOT_AVAILABLE   = 1
    AVAILABLE       = 2
    NOT_ACTIVATED   = 3
    ACTIVATED       = 4
    MANDATORY       = 5

class InternalQuestion(Enum):
    PICK_CARD                       = 1
    ACTIVATE_PRE_MOVEMENT_POWER     = 2
    ACTIVATE_POST_MOVEMENT_POWER    = 3
    MOVE                            = 4
    MOVE_BLACK                      = 5
    MOVE_BLUE                       = 6
    MOVE_BROWN                      = 7
    MOVE_GREY                       = 8
    MOVE_PINK                       = 9
    MOVE_PURPLE                     = 10
    MOVE_RED                        = 11
    ATTRACT                         = 12
    ENTRANCE_BLOCKED                = 13
    EXIT_BLOCKED                    = 14
    ROOM_SHADOW                     = 15
    EXCHANGE                        = 16
    DRAW                            = 17
    TAKE_AWAY                       = 18
    END_GAME                        = 19
    NOTHING                         = 20