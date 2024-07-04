""" Contains the general class for the player_group/npcs """
from math import floor

import pygame

from misc.constants import *
from sprites.animations import Animations, EntityState
from sprites.sprite_entity import Entity, EntityLayer, EntityGroups
from sprites.sprite_sheets import SpriteSheetName
from enum import Enum, auto

class EnemyType(Enum):
    SNAKE = auto()
    SHROOM = auto()
    RABBIT = auto()
    BEE = auto()

    def get_spritesheet_name(self):
        return enemy_information[self][0]

    def get_animations_data(self):
        return enemy_information[self][1]

enemy_information = {EnemyType.SNAKE: [SpriteSheetName.SNAKE_ENEMY, Animations.SNAKE],
                     EnemyType.SHROOM: [SpriteSheetName.ENEMIES, Animations.SHROOM],
                     EnemyType.RABBIT: [SpriteSheetName.ENEMIES, Animations.RABBIT],
                     EnemyType.BEE: [SpriteSheetName.ENEMIES, Animations.BEE]}


class Enemy(Entity):
    """General class for enemies_group"""
    def __init__(self, game, x: int, y: int, enemy_type: EnemyType, width: int, height: int):
        super().__init__(game, x, y, EntityGroups.ENEMY, EntityLayer.PERSON, spritesheet_name=enemy_type.get_spritesheet_name(),
                         sprite_x=0, sprite_y=0, width=width, height=height)
        # player_group is twice as tall as a regular block

        self.speed = E_WALKING_SPEED  # a constant that is slower than the player_group walking speed
        self.dx = self.dy = 0
        self.enemy_state = EntityState.GROUNDED_LEFT

        self.animations = self.process_animations(enemy_type.get_animations_data())
        self.animation_loop = 1

        self.is_on_ground = False

        self.death_counter = 20

    def update(self):
        """Runs any update to the player_group sprite like a movement and then the subsequent animation. Runs every tick"""
        if self.enemy_state is not EntityState.DEATH:
            self.is_on_ground = False
            self.move()
            self.animate()
            self.gravity()

            if self.rect.y >= self.game.size[0]:
                self.death()

            self.rect.x += self.dx  # Updates position of player_group
            self.x_collide()

            self.rect.y += self.dy
            self.y_collide()

            self.dx = self.dy = 0
        else:
            if self.death_counter != 0:
                self.death_counter -= 1
            else:
                self.remove_from_screen()
                self.game.no_more_enemies = not self.game.is_group_on_screen(self.game.enemies_group)

    def move(self):
        """Actually changes dx value"""
        coordinate_change = self.speed

        if self.enemy_state == EntityState.GROUNDED_LEFT:
            coordinate_change *= -1  # Makes number negative if the person's moving left

        setattr(self, "dx", coordinate_change)  # Changes dx value

    # __________________________________________ANIMATION FUNCTIONS__________________________________________
    def process_animations(self, animations_enum: Animations):
        """Takes list of coordinates for a spritesheet and returns pygame sprites"""
        animations = {}

        for enemy_state in animations_enum.value:
            animation_list = self.get_animation_sprites(animations_enum.value[enemy_state])
            if type(animation_list) is not list:
                animation_list = [animation_list]
            animations[enemy_state] = animation_list

        return animations

    def get_animation_sprites(self, coordinates_list: list):
        """Helper function for process animations: takes each list and applies get_sprite function onto each x,y
        coordinate pairs and returns the list in the same format and size as it was before"""
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

    def animate(self):
        """Selects sprites to display for whatever the player_group is doing. If moving there is an animation loop played"""
        animations = self.animations[self.enemy_state]

        if self.enemy_state is not EntityState.DEATH:
            self.image = animations[floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= len(animations):
                self.animation_loop = 0

        else:
            self.image = animations[0]

        self.image = pygame.transform.scale(self.image, (self.width * SCALE_UP, self.height * SCALE_UP))  # As these images have not
        # been scaled
        if self.enemy_state is EntityState.GROUNDED_LEFT and self.spritesheet.name != "enemies":
            self.image = pygame.transform.flip(self.image, True, False)

        if self.enemy_state is EntityState.GROUNDED_RIGHT and self.spritesheet.name == "enemies":
            self.image = pygame.transform.flip(self.image, True, False)

    # __________________________________________COLLISION FUNCTIONS__________________________________________
    def x_collide(self):
        """Detects a horizontal collision and acts on it to stop player_group going through objects/entities."""
        hit_block = pygame.sprite.spritecollide(self, self.game.blocks_group, False)
        # hit_block[0] will refer to the block hit

        # If collision is horizontal
        if hit_block:
            if self.dx > 0:
                self.rect.x = hit_block[0].rect.left - self.rect.width  # Moves char just to the left of the other object
                self.enemy_state = EntityState.GROUNDED_LEFT  # Changes direction

            elif self.dx < 0:
                self.rect.x = hit_block[0].rect.right  # Moves char just to the right of the other object
                self.enemy_state = EntityState.GROUNDED_RIGHT  # Changes direction

    def y_collide(self):
        """Detects a vertical collision and acts on it to stop player_group going through objects/entities."""
        hit_block = pygame.sprite.spritecollide(self, self.game.blocks_group, False)

        if hit_block:
            if self.dy > 0:  # Player hits ground
                self.rect.y = hit_block[0].rect.top - self.rect.height  # Moves char just below the other object
                self.is_on_ground = True

            elif self.dy < 0:  # Upwards collision, enemy hits ceiling (just in case)
                self.rect.y = hit_block[0].rect.bottom  # Moves char just above the other object

    # __________________________________________MISC FUNCTIONS__________________________________________
    def gravity(self):
        """Adds 5 to the y position if the player_group is in the air (like actual gravity)"""
        if not self.is_on_ground:
            self.dy = 5

    def death(self):
        """Sets enemy state into the death state which changes its sprite image to the death one and sets off the
        death timer in the update function."""
        self.enemy_state = EntityState.DEATH
        self.animate()

    def reset_variables(self):
        """If sprite is reused, then these variables need to be reset"""
        self.enemy_state = EntityState.GROUNDED_LEFT

class Snake(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, EnemyType.SNAKE, width=16, height=16)

class Shroom(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, EnemyType.SHROOM, width=11, height=13)

class Rabbit(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, EnemyType.RABBIT, width=12, height=13)

class Bee(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, EnemyType.BEE, width=12, height=8)