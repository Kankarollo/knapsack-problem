from enum import Enum


class ParentSelection(Enum):
    Roulette = 1
    SUS = 2
    Tournament = 3
    Rank = 4
    Random = 5


class MutationSelection(Enum):
    Flip = 1
    Swap = 2
    Scramble = 3
    Inversion = 4
