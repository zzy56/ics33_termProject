from enum import Enum

class pokerHandsType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULLHOUSE = 7
    FOUR_OF_A_KIND = 8
    ROYAL_FLUSH = 9