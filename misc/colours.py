"""contains colours enum class which contains rgb values for all colours used in the game"""
from enum import Enum


class Colour(tuple, Enum):
    """contains rgb values for all colours used in the game"""
    TITLE_SCREEN = (47, 105, 199)
    GAME_OVER_SCREEN = (208, 53, 65)
    VICTORY_SCREEN = (207, 159, 53)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    OVERGROUND_BACKGROUND = (148, 148, 255)
    PIPES_BACKGROUND = (129, 124, 255)
    BLOCKS_BACKGROUND = (0, 41, 140)
    ENTITY_BACKGROUND = (0, 0, 2)

    LVL_1_BACKGROUND = (130, 130, 130)
    LVL_2_BACKGROUND = (92, 92, 92)
    LVL_3_BACKGROUND = (42, 42, 42)
    LVL_4_BACKGROUND = (0, 0, 0)


