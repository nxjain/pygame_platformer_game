import pygame.sprite

from sprites.sprite_entity import Entity, EntityGroups, EntityLayer
from sprites.sprite_sheets import SpriteSheetName
from misc.constants import BLOCK_SIZE_Y, BLOCK_SIZE_X


class GenericBlock(Entity):
    """A block entity sprite"""

    def __init__(self, game, x, y, sprite_x, sprite_y):
        super().__init__(game, x, y, EntityGroups.BLOCK, EntityLayer.BLOCK, spritesheet_name=SpriteSheetName.BLOCKS,
                         sprite_x=sprite_x, sprite_y=sprite_y, width=BLOCK_SIZE_X, height=BLOCK_SIZE_Y)


class Block(GenericBlock):
    """b: A normal block entity sprite"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y, sprite_x=68, sprite_y=34)


class Brick(GenericBlock):
    """B: A normal brick entity sprite"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y, sprite_x=34, sprite_y=17)


class Ground(GenericBlock):
    """G: A ground entity sprite"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y, sprite_x=102, sprite_y=17)


class Underground(GenericBlock):
    """U: Goes under the ground entity sprite"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y, sprite_x=136, sprite_y=17)


class InvisibleWall(Entity):
    """I: An invisible block entity sprite"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y, EntityGroups.BLOCK, EntityLayer.BLOCK,
                         spritesheet_name=SpriteSheetName.INVISIBLE_WALL,
                         sprite_x=1, sprite_y=31, width=BLOCK_SIZE_X, height=BLOCK_SIZE_Y)


class EnemyDisappearingBlock(GenericBlock):
    """d: A block that disappears when all the enemies in the room have been killed."""
    def __init__(self, game, x, y):
        super().__init__(game, x, y, sprite_x=0, sprite_y=34)

    def update(self):
        if self.game.no_more_enemies:
            self.remove_from_screen()


class GoalDisappearingBlock(GenericBlock):
    """D: A block that disappears when all the enemies in the room have been killed."""
    def __init__(self, game, x, y):
        super().__init__(game, x, y, sprite_x=34, sprite_y=34)

    def update(self):
        if self.game.no_more_enemies and self.game.coins_collected and self.game.key_found:
            self.remove_from_screen()

class GoalLandingBlock(Entity):
    """g: A block that disappears when all the enemies in the room have been killed."""
    def __init__(self, game, x, y):
        super().__init__(game, x, y, EntityGroups.GOAL_BLOCK, EntityLayer.BLOCK, spritesheet_name=SpriteSheetName.BLOCKS,
                         sprite_x=17, sprite_y=34, width=BLOCK_SIZE_X, height=BLOCK_SIZE_Y)