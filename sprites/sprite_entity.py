from math import floor

import pygame
from misc.constants import *
from enum import Enum, auto

from sprites.animations import Animations, EntityState
from sprites.sprite_sheets import SpriteSheetName


class EntityLayer(int, Enum):
    """Identifies the layer the sprite is on (to know which sprites to display over other sprites"""
    BACKGROUND = auto()
    BLOCK = auto()
    PERSON = auto()
    PIPE = auto()
    OVERLAY = auto()


class EntityGroups(list, Enum):
    """Gives information on the type of entity.
    Values are the sprite groups that these entities would be in."""
    BACKGROUND = []
    BLOCK = ["blocks"]
    PIPE = ["pipes", "blocks"]
    PLAYER = ["player"]
    ENEMY = ["enemies"]
    COIN = ["coins"]
    KEY = ["keys"]
    GOAL_BLOCK = ["blocks", "goal_blocks"]
    OVERLAY = ["overlay"]


class RotationDirection(int, Enum):
    """Values used to rotate any sprite as long (as you assume that they are looking left)"""
    LEFT = 0
    DOWN = 90
    RIGHT = 180
    UP = 270


class Entity(pygame.sprite.Sprite):
    """Base class for all entities"""
    unused_instances = []

    def __init__(self, game, x: int, y: int, ent_groups=None, layer: EntityLayer = None, spritesheet_name: str = None,
                 sprite_x: int = None, sprite_y: int = None, width: int = None,
                 height: int = None):  # Default variables
        # are to not flip out the program with the alternate constructors below, which are only used for children nodes

        self.game = game  # So that the entity can have access to the game at all times
        self._layer = layer.value  # The player_group and the background for example will be on different layers, so it knows
        # which sprite to put over the other.

        self.width = width
        self.height = height

        rem_groups = self.load_rem_groups(ent_groups.value)
        self.groups = tuple([self.game.all_sprites_group] + rem_groups)
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.spritesheet = game.spritesheets[spritesheet_name]
        self.sprite_coordinates = [sprite_x, sprite_y]

        self.get_sprite(x, y)

    def get_sprite(self, x, y, rotation_dir: RotationDirection = None):
        """Gets the image and creates the object sprite."""
        self.image = self.get_image(self.sprite_coordinates[0], self.sprite_coordinates[1])
        self.image = pygame.transform.scale(self.image, (self.width * SCALE_UP, self.height * SCALE_UP))
        if rotation_dir is not None:
            self.image = self.image = pygame.transform.rotate(self.image, rotation_dir)

        # Rect stores the position of the entity, img is just how it appears on screen.
        self.rect = self.image.get_rect()
        self.rect.x = x * BLOCK_SIZE_X * SCALE_UP
        self.rect.y = y * BLOCK_SIZE_Y * SCALE_UP

    def get_image(self, x: int, y: int):
        """ In order to shorten long statement (self.spritesheet.get_specific_sprite(x, y, self.width, self.height)"""
        return self.spritesheet.get_specific_sprite(x, y, self.width, self.height)

    def load_rem_groups(self, rem_groups):
        """Uses the strings from the 'EntityGroups' class, retrieves the appropriate groups from the game class returns
        an array with all the groups."""
        arr = []
        for group_name in rem_groups:
            arr.append(getattr(self.game, group_name + "_group"))
        return arr

    def show_on_screen(self, new_x: int, new_y: int):
        """When an unused sprite which has been removed off the screen is being shown again."""
        self.game.all_sprites_group.add(self)  # If it's in the all sprites group, then the sprite will be drawn/updated
        self.unused_instances.remove(self)  # The sprite is now being used.
        self.reset_variables()  # All entities have this, only player and enemy ones actually do something
        self.change_coordinates(new_x, new_y)

    def remove_from_screen(self):
        """Alternative to self.kill(), it removes the sprite from the all_sprites group, which stops the sprite from
        being drawn and updated, and adds it to the unused instances array, so it can be reused again later on."""
        self.game.all_sprites_group.remove(self)
        self.change_coordinates(0, 0)  # In case it could have interfered with something
        self.unused_instances.append(self)

    def change_coordinates(self, new_x: int, new_y: int):
        """Used mainly when an instance of a class is being reused, as it needs new coordinates to be set."""
        self.rect.x = new_x * BLOCK_SIZE_X * SCALE_UP
        self.rect.y = new_y * BLOCK_SIZE_X * SCALE_UP

    @classmethod
    def find_unused_instance(cls):
        """To be used with every child class of entity, not entity itself."""
        for instance in cls.unused_instances:
            if isinstance(instance, cls):
                return instance
        return False

    @classmethod
    def create_instance(cls, game, x, y, rotation_dir: RotationDirection = None):
        """The constructor variable for every child class of entity. Checks if an instance of the variable is available
        i.e. has been created but is not being displayed on screen, if so, this unused instance is retrieved, otherwise
        it creates a new instance."""
        instance_found = cls.find_unused_instance()
        if instance_found:
            instance_found.show_on_screen(x, y)

            if rotation_dir is not None:  # for pipes or other rotatable objects.
                instance_found.get_sprite(x, y, rotation_dir)
                instance_found.set_rotation_dir(rotation_dir)

            return instance_found

        if rotation_dir is None:
            return cls(game, x, y)  # if unused instance is not found then a new instance is created.
        return cls(game, x, y, rotation_dir)  # for pipes or other rotatable objects.

    def reset_variables(self):
        """If sprite is reused, then these variables need to be reset. This is a placeholder function for any children
        that want to use it"""
        pass

    def set_rotation_dir(self, rotation_dir):
        """This is a placeholder function. Actually used for pipes or other rotatable objects."""
        pass


class Key(Entity):
    """A key entity sprite"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y, EntityGroups.KEY, EntityLayer.PERSON, spritesheet_name=SpriteSheetName.KEY,
                         sprite_x=6, sprite_y=8, width=BLOCK_SIZE_X, height=BLOCK_SIZE_Y)

    def picked_up(self):
        self.game.key_found = True
        self._layer = EntityLayer.PIPE  # Want to put it in front of everything
        self.rect.x = 0
        self.rect.y = 33


class Pipe(Entity):
    """v/V/h/H: A pipe sprite object"""
    def __init__(self, game, x, y, rotation_dir: RotationDirection = RotationDirection.LEFT):
        super().__init__(game, x, y, EntityGroups.PIPE, EntityLayer.PIPE, spritesheet_name=SpriteSheetName.PIPES,
                         sprite_x=2, sprite_y=42, width=BLOCK_SIZE_X * 4, height=BLOCK_SIZE_Y * 2)
        self.rotation_dir = rotation_dir
        self.get_sprite(x, y, rotation_dir)

    def is_entry_pipe(self) -> bool:
        return self.rotation_dir is RotationDirection.LEFT

    def set_rotation_dir(self, new_rotation_dir) -> None:
        self.rotation_dir = new_rotation_dir


class Coin(Entity):
    """C: A coin object"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y, EntityGroups.COIN, EntityLayer.PERSON, spritesheet_name=SpriteSheetName.ROTATING_COIN,
                         sprite_x=6, sprite_y=6, width=6, height=6)
        self.animations = self.get_animation_sprites(Animations.COIN.value[EntityState.GROUNDED_LEFT])
        self.animation_loop = 1

    def get_animation_sprites(self, coordinates_list: list):
        """Takes each list and applies get_sprite function onto each x,y coordinate pairs and returns the list in the
        same format and size as it was before"""
        new_list = []
        x_coord = None

        for item in range(len(coordinates_list)):
            if type(coordinates_list[item]) is list:  # If we've encountered a pair of coordinates or more, as opposed
                # to just a single coordinate.
                new_list.append(self.get_animation_sprites(coordinates_list[item]))  # Recursively calls algorithm until
                # the for loop is iterating through a pair of coordinates and not a multidimensional list

            else:  # This is when the algorithm is iterating through a pair of coordinates and coordinates_list[item] is
                # an x/y coordinate
                if x_coord is None:  # If this is true then coordinates_list[item] = the x coordinate.
                    x_coord = coordinates_list[item]
                else:  # Otherwise, coordinates_list[item] = the y coordinate.
                    new_list.append(self.get_image(x_coord, coordinates_list[item]))
        if len(new_list) == 1:  # This is during the recursive stage when new_list = [SurfaceObj], but I want the
            # SurfaceObj by itself so the next line takes it out of the list.
            new_list = new_list[0]
        return new_list

    def update(self):
        self.animate()

    def picked_up(self):
        self.remove_from_screen()
        self.game.coins_collected = not self.game.is_group_on_screen(self.game.coins_group)

    def animate(self):
        """Selects sprites to display for whatever the player_group is doing. If moving there is an animation loop played"""
        self.image = self.animations[floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= len(self.animations):
            self.animation_loop = 0

        self.image = pygame.transform.scale(self.image, (self.width * SCALE_UP, self.height * SCALE_UP))



