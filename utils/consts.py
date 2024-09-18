from enum import Enum


MAX_SUGGESTIONS: int = 5


class Typo(Enum):
    INVALID = -1
    MATCH = 0
    SWITCH = 1
    ADD = 2
    MISS = 3