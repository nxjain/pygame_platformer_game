from enum import Enum, auto


class EntityState(Enum):
    """Describes which state the player_group is in to help the program decide which movement to undertake and which
    animations to play"""
    GROUNDED_LEFT = auto()
    GROUNDED_RIGHT = auto()

    JUMP_LEFT = auto()
    JUMP_RIGHT = auto()

    DEATH = auto()


class Animations(Enum):
    """Stores the x,y coordinates for the sprites. For the grounded sprites, the second item in the array contains the
    walking animations to create a loop."""
    SNAKE = {EntityState.GROUNDED_LEFT: [[0, 0], [16, 0], [32, 0]],
             EntityState.GROUNDED_RIGHT: [[0, 0], [16, 0], [32, 0]],
             EntityState.DEATH: [97, 0]}

    MAIN_CHARACTER = {EntityState.GROUNDED_LEFT: [[30, 0], [[90, 0], [120, 0], [150, 0]]],
                      EntityState.GROUNDED_RIGHT: [[30, 0], [[90, 0], [120, 0], [150, 0]]],
                      EntityState.JUMP_RIGHT: [30, 30],
                      EntityState.JUMP_LEFT: [30, 30],
                      EntityState.DEATH: [190, 0]}

    SHROOM = {EntityState.GROUNDED_LEFT: [[1, 0], [17, 0]],
              EntityState.GROUNDED_RIGHT: [[1, 0], [17, 0]],
              EntityState.DEATH: [1, 0]}

    RABBIT = {EntityState.GROUNDED_LEFT: [[0, 16], [16, 16]],
              EntityState.GROUNDED_RIGHT: [[0, 16], [16, 16]],
              EntityState.DEATH: [0, 16]}

    BEE = {EntityState.GROUNDED_LEFT: [[0, 33], [16, 33]],
           EntityState.GROUNDED_RIGHT: [[0, 33], [16, 33]],
           EntityState.DEATH: [0, 33]}

    COIN = {EntityState.GROUNDED_LEFT: [[1, 1], [9, 1], [17, 1], [25, 1], [33, 1], [41, 1], [49, 1], [57, 1]]}
