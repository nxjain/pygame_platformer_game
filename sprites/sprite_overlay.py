from misc.constants import BLOCK_SIZE_X, SCALE_UP
from sprites.sprite_entity import Entity, EntityGroups, EntityLayer
from sprites.sprite_sheets import SpriteSheetName

num_lives_overlay_help = {1: [16, 0],
                          2: [32, 0],
                          3: [48, 0],
                          4: [0, 16],
                          5: [16, 16],
                          6: [32, 16],
                          7: [48, 16]}


class PlayerHeadOverlay(Entity):
    """Displays the player's head as part of the 'number of lives' overlay"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y, EntityGroups.OVERLAY, EntityLayer.OVERLAY, spritesheet_name=SpriteSheetName.PLAYER,
                         sprite_x=190, sprite_y=48, width=16, height=16)


class XSymbolOverlay(Entity):
    """Displays an X symbol that means 'number of lives'"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y, EntityGroups.OVERLAY, EntityLayer.OVERLAY,
                         spritesheet_name=SpriteSheetName.LIVES_COUNT,
                         sprite_x=0, sprite_y=0, width=16, height=16)


class NumLivesOverlay(Entity):
    """Displays the number of lives"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y, EntityGroups.OVERLAY, EntityLayer.OVERLAY,
                         spritesheet_name=SpriteSheetName.LIVES_COUNT,
                         sprite_x=48, sprite_y=16, width=16, height=16)

    def set_lives(self):
        self.sprite_coordinates = num_lives_overlay_help[self.game.num_lives]
        self.get_sprite(self.rect.x, self.rect.y)


class Overlay:
    """Combines three overlay objects into one."""
    def __init__(self, game, x, y):
        self.player_head = PlayerHeadOverlay(game, x, y)
        self.x_symbol = XSymbolOverlay(game, x + 1, y)
        self.num_lives = NumLivesOverlay(game, x + 2, y)
        self.set_lives()

    def get_arr(self):
        return [self.player_head, self.x_symbol, self.num_lives]

    def set_lives(self):
        self.num_lives.set_lives()

    def change_pos(self, x, y):
        self.player_head.rect.x = x * BLOCK_SIZE_X * SCALE_UP
        self.player_head.rect.y = self.x_symbol.rect.y = self.num_lives.rect.y = y * BLOCK_SIZE_X * SCALE_UP
        self.x_symbol.rect.x = (x + 1) * BLOCK_SIZE_X * SCALE_UP
        self.num_lives.rect.x = (x + 2) * BLOCK_SIZE_X * SCALE_UP

    def during_level(self):
        self.change_pos(0, 0)

    def during_level_loading_screen(self):
        self.change_pos(9.5, 9)
