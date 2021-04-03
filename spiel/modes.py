from enum import Enum, unique


@unique
class Mode(str, Enum):
    SLIDE = "slide"
    DECK = "deck"
