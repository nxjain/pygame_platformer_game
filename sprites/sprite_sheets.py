"""Contains all spritesheets"""
import pygame
from misc.colours import Colour
from enum import Enum, auto


class SpriteSheet:
    """Contains info about spritesheet. Example file_location: 'img/main_character.png'."""
    def __init__(self, file_location, bg_colour=Colour.BLACK):
        self.sheet = pygame.image.load(file_location).convert()
        self.name = file_location[4:-4]  # To remove "img/" from the beginning of the file_name and ".png" from the end
        self.bg_colour = bg_colour  # To remove a background colour of the image and make that part transparent.

    def get_specific_sprite(self, x, y, width, height):
        """Searches sprite sheet for desired sprite image using x,y coordinates of top left corner of sprite and its
        width and height. Retrieves this sprite image and makes its background colour transparent. Returns sprite to
        presumably the entity class the spritesheet is of (e.g returns the player_group sprite to the player_group class)."""
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(self.bg_colour)
        return sprite

    def __repr__(self):
        return f"SpriteSheet.{self.name.upper()}"


class SpriteSheetName(Enum):
    """This enum is originally used to help create the sprite sheets, and then used to refer to them. It stores the
    parameters required for the SpriteSheet function initialisation. The key is the file name of the sprite sheet and
    the value is the background colour for the sprite sheet. Each sprite entity will store a 'SpriteSheetName' enum to
    refer to their sprite sheet."""
    BLOCKS = auto()
    INVISIBLE_WALL = auto()
    PLAYER = auto()
    SNAKE_ENEMY = auto()
    ASSEMBLED_STRUCTURES = auto()
    PIPES = auto()
    KEY = auto()
    ENEMIES = auto()
    ROTATING_COIN = auto()
    LIVES_COUNT = auto()

    def get_filename(self):
        return "img/" + self.name.lower() + ".png"

    def get_background_col(self):
        return background_colours[self]

    def __repr__(self):
        return "SpriteSheetName." + self.name + ":" + str(self.get_background_col().value)


def load_overworld_spritesheets():
    """Goes through the "SpriteSheetName" enum, creates spritesheet objects for all of them and then puts them all in
    one dictionary which will be passed onto the 'game' class"""
    file_names = [name for name in SpriteSheetName]
    spritesheets = {}
    for f_name in file_names:  # f_name is a SpriteSheetName enum
        spritesheets[f_name] = SpriteSheet(f_name.get_filename(), f_name.get_background_col())
    return spritesheets


background_colours = {SpriteSheetName.PLAYER: Colour.ENTITY_BACKGROUND,
                      SpriteSheetName.BLOCKS: Colour.ENTITY_BACKGROUND,
                      SpriteSheetName.INVISIBLE_WALL: Colour.BLACK,
                      SpriteSheetName.SNAKE_ENEMY: Colour.ENTITY_BACKGROUND,
                      SpriteSheetName.ASSEMBLED_STRUCTURES: Colour.OVERGROUND_BACKGROUND,
                      SpriteSheetName.PIPES: Colour.PIPES_BACKGROUND,
                      SpriteSheetName.KEY: Colour.ENTITY_BACKGROUND,
                      SpriteSheetName.ENEMIES: Colour.ENTITY_BACKGROUND,
                      SpriteSheetName.ROTATING_COIN: Colour.ENTITY_BACKGROUND,
                      SpriteSheetName.LIVES_COUNT: Colour.ENTITY_BACKGROUND}
