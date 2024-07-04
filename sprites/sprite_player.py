""" Contains the general class for the player_group/npcs """
from math import floor

import pygame

from misc.maps import MapId
from misc.constants import *
from sprites.animations import Animations, EntityState
from sprites.sprite_entity import Entity, EntityLayer, EntityGroups, RotationDirection
from sprites.sprite_sheets import SpriteSheetName
from sounds.sounds import SoundName
from time import sleep


class Player(Entity):
    """General class for Player/NPC"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y, EntityGroups.PLAYER, EntityLayer.PERSON, spritesheet_name=SpriteSheetName.PLAYER,
                         sprite_x=209, sprite_y=52, width=30, height=30)
        # player_group is twice as tall as a regular block
        self.speed = P_WALKING_SPEED
        self.dx = self.dy = 0
        self.player_state = EntityState.GROUNDED_RIGHT

        self.animations = self.process_animations(Animations.MAIN_CHARACTER)
        self.animation_loop = 1

        self.is_on_ground = False
        self.jump_counter = 0  # Keeps track of time length of jump, allows jump to last longer than the time taken to
        # run update once
        self.is_jumping = False

        self.death_counter = 20  # This is to aid with the death animation, where for a short period of time the player_group
        # moves upwards

    def update(self):
        """Runs any update to the player_group sprite like a movement and then the subsequent animation. Runs every tick"""
        self.detect_movement()
        self.animate()
        self.gravity()
        self.is_on_ground = False

        if self.rect.y >= self.game.size[0]:
            self.death()

        self.specific_entity_collide()

        self.rect.x += self.dx  # Updates position of player_group
        self.x_collide()

        if self.jump_counter != 0:
            self.jump_counter -= 1
            self.jump_movement()

        self.rect.y += self.dy
        self.y_collide()

        self.dx = self.dy = 0

    def detect_movement(self):
        """Determines whether a movement is happening and potentially changes movement speed, the entity state and runs
        the move() or jump() functions if the appropriate keys have been pressed."""
        key_pressed = pygame.key.get_pressed()  # Creates huge array of each key and a boolean value of whether they
        # were pressed

        if key_pressed[pygame.K_c]:  # RUN
            self.speed = P_RUNNING_SPEED
        else:
            self.speed = P_WALKING_SPEED

        move_key_pressed = key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_RIGHT]
        jump_key_pressed = key_pressed[pygame.K_SPACE] or key_pressed[pygame.K_UP]

        if move_key_pressed:
            if key_pressed[pygame.K_LEFT]:  # GROUNDED_LEFT
                if self.is_jumping:
                    self.player_state = EntityState.JUMP_LEFT
                else:
                    self.player_state = EntityState.GROUNDED_LEFT

            if key_pressed[pygame.K_RIGHT]:  # GROUNDED_RIGHT
                if self.is_jumping:
                    self.player_state = EntityState.JUMP_RIGHT
                else:
                    self.player_state = EntityState.GROUNDED_RIGHT

            self.move()

        if jump_key_pressed:
            self.jump(35)

    def move(self):
        """Actually changes dx value"""
        coordinate_change = self.speed

        if self.player_state in [EntityState.GROUNDED_LEFT, EntityState.JUMP_LEFT]:
            coordinate_change *= -1  # Makes number negative if the person's moving left

        # Camera Movement:
        self.game.move_sprites(-coordinate_change, 0)  # minus is there to move the objects in opposite direction

        if self.game.key_found:
            [_ for _ in self.game.keys_group][0].rect.x += coordinate_change

        setattr(self, "dx", coordinate_change)  # Changes dx value

    # __________________________________________ANIMATION FUNCTIONS__________________________________________
    def process_animations(self, animations_enum: Animations):
        """Takes list of coordinates for a spritesheet and returns pygame sprites"""
        animations = {}

        for player_state in animations_enum.value:
            animation_list = self.get_animation_sprites(animations_enum.value[player_state])
            if type(animation_list) is not list:
                animation_list = [animation_list]
            animations[player_state] = animation_list

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
        animations = self.animations[self.player_state]

        standing_still = (self.dx == 0 and self.dy == 0)

        if standing_still or self.is_jumping or self.player_state == EntityState.DEATH:
            self.image = animations[0]

        else:  # Plays walking/running animation sprites in a loop.
            self.image = animations[1][floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 0

        self.image = pygame.transform.scale(self.image, (self.width * SCALE_UP, self.height * SCALE_UP))  # As these images have not
        # been scaled
        if self.player_state in [EntityState.GROUNDED_LEFT, EntityState.JUMP_LEFT]:
            self.image = pygame.transform.flip(self.image, True, False)

    # __________________________________________COLLISION FUNCTIONS__________________________________________
    def x_collide(self):
        """Detects a horizontal collision and acts on it to stop player_group going through objects/entities."""
        hit_block = pygame.sprite.spritecollide(self, self.game.blocks_group, False)
        hit_pipe = pygame.sprite.spritecollide(self, self.game.pipes_group, False)
        # hit_block[0] will refer to the block hit

        # If collision is horizontal
        if hit_block:
            block = hit_block[0]
            if self.dx > 0:
                self.rect.x = block.rect.left - self.rect.width  # Moves char just to the left of the other object

                # To Reverse Camera Movement:
                self.game.move_sprites(self.speed, 0)
                if self.game.key_found:
                    [_ for _ in self.game.keys_group][0].rect.x -= self.speed

            elif self.dx < 0:
                self.rect.x = block.rect.right  # Moves char just to the right of the other object

                # To Reverse Camera Movement:
                self.game.move_sprites(-self.speed, 0)
                if self.game.key_found:
                    [_ for _ in self.game.keys_group][0].rect.x += self.speed

        if hit_pipe and self.game.key_found:
            pipe = hit_pipe[0]
            if self.dx > 0 and pipe.is_entry_pipe():  # Can only enter pipe that faces left
                self.enter_pipe(pipe)

    def y_collide(self):
        """Detects a vertical collision and acts on it to stop player_group going through objects/entities."""
        hit_block = pygame.sprite.spritecollide(self, self.game.blocks_group, False)
        hit_goal_block = pygame.sprite.spritecollide(self, self.game.goal_blocks_group, False)

        if hit_block:
            self.is_jumping = False
            if self.dy > 0:  # Player hits ground
                if self.player_state == EntityState.JUMP_RIGHT:
                    self.player_state = EntityState.GROUNDED_RIGHT
                elif self.player_state == EntityState.JUMP_LEFT:
                    self.player_state = EntityState.GROUNDED_LEFT

                self.rect.y = hit_block[0].rect.top - self.rect.height  # Moves char just below the other object
                self.is_on_ground = True

                if hit_goal_block:
                    self.finish_level()

            elif self.dy < 0:  # Upwards collision, player_group hits ceiling
                self.rect.y = hit_block[0].rect.bottom  # Moves char just above the other object
                self.jump_counter = 0  # cancels jump

    def specific_entity_collide(self):
        """Collates other entity collision checks"""
        self.enemy_collide()
        self.key_collide()
        self.coin_collide()

    def enemy_collide(self):
        """Determines whether an enemy collision has occurred. Determines whether this is a death for the player_group or for
        the enemy."""
        hit_enemy = pygame.sprite.spritecollide(self, self.game.enemies_group, False)
        # hit_enemy will create a list of sprites in the enemies_group group that have collided with the player_group.
        # It will have an empty list if there are no collisions, hence the "if hit_enemy" statement below will not run
        # hit_enemy[0] will be the enemy that the player_group collides with.

        if hit_enemy:
            enemy = hit_enemy[0]
            if (enemy.rect.y - self.rect.height+5) < self.rect.y and enemy.enemy_state is not EntityState.DEATH:
                self.death()
            else:
                enemy.death()
                self.game.play_sound(SoundName.STOMP)
                self.is_on_ground = True  # Otherwise, jump won't happen
                self.jump(20)  # Smaller jump than usual

    def key_collide(self):
        hit_key = pygame.sprite.spritecollide(self, self.game.keys_group, False)
        if hit_key:
            hit_key[0].picked_up()
            self.game.play_sound(SoundName.KEY_COLLECTED)

    def coin_collide(self):
        hit_coin = pygame.sprite.spritecollide(self, self.game.coins_group, False)
        if hit_coin:
            hit_coin[0].picked_up()
            self.game.play_sound(SoundName.COIN_COLLECTED)
    # __________________________________________JUMP FUNCTIONS__________________________________________
    def gravity(self):
        """Adds 5 to the y position if the player_group is in the air (like actual gravity)"""
        if not self.is_on_ground and self.jump_counter == 0:
            self.dy = 5

    def jump(self, counter):
        """Enacts a jump (from the 'detect_movement' function)"""
        if self.is_on_ground:
            self.is_on_ground = False
            self.is_jumping = True
            self.jump_counter = counter

            if self.player_state == EntityState.GROUNDED_RIGHT:
                self.player_state = EntityState.JUMP_RIGHT
            elif self.player_state == EntityState.GROUNDED_LEFT:
                self.player_state = EntityState.JUMP_LEFT

    def jump_movement(self):
        """Actually adds a value to dy every update function"""
        jump_dy_change = (self.jump_counter / 6) * -1  # needs to be negative as negative y change = going up
        setattr(self, "dy", jump_dy_change)

    # __________________________________________PLAYER LEAVES MAP FUNCTIONS__________________________________________
    def death(self):
        """Player death animation. Changes into death sprite, waits a little, rises a little and then falls off the
        map. All other sprites are paused during this."""
        self.game.pause_music()
        self.game.play_sound(SoundName.PLAYER_DEATH)
        self.player_state = EntityState.DEATH
        self.animate()
        self.game.draw()
        sleep(0.25)
        while self.rect.y < 700:
            if self.death_counter != 0:  # When the player_group moves upwards in the death animation
                self.rect.y -= 3
                self.game.events()
                self.game.draw()
                self.death_counter -= 1
            else:
                self.rect.y += 4
                self.game.events()
                self.game.draw()
        sleep(1)
        self.game.num_lives -= 1
        if self.game.num_lives != 0:
            self.game.overlay.set_lives()
            self.game.current_map_id = self.game.current_map_id.get_first_level_map()
            self.game.load_map()
        else:
            self.game.game_over_screen()
            self.game.num_lives = 7

    def reset_variables(self):
        """If sprite is reused, then these variables need to be reset"""
        self.player_state = EntityState.GROUNDED_RIGHT
        self.death_counter = 20
        self.jump_counter = 0

    # __________________________________________________PIPE FUNCTIONS__________________________________________________
    def enter_pipe(self, pipe):
        """The entering of a pipe by a player. Warped to next map in game"""
        self.pipe_enter_animation(pipe)
        sleep(0.75)
        self.game.current_map_id = self.game.current_map_id.get_next_map()
        self.game.load_map()

    def pipe_enter_animation(self, pipe):
        self.game.play_sound(SoundName.PIPE_ENTER_EXIT)
        """The animation when a player enters a pipe"""
        self.player_state = EntityState.GROUNDED_RIGHT
        self.dx = 0
        self.animate()

        self.rect.y = pipe.rect.y

        desired_player_x = pipe.rect.x+1
        while self.rect.x != desired_player_x:
            self.rect.x += 1
            self.game.events()
            self.game.draw()

    def if_exit_pipe(self):
        """Run at the beginning of a map loading to see if the player is meant to come out of a pipe to get into the new map"""
        hit_pipe = pygame.sprite.spritecollide(self, self.game.pipes_group, False)
        if hit_pipe and not hit_pipe[0].is_entry_pipe():
            self.exit_pipe_animation(hit_pipe[0])

    def exit_pipe_animation(self, pipe):
        """The animation when a player exits a pipe"""
        self.game.play_sound(SoundName.PIPE_ENTER_EXIT)
        self.player_state = EntityState.GROUNDED_RIGHT
        self.dx = 0
        self.animate()

        if pipe.rotation_dir is RotationDirection.DOWN:
            desired_player_y = pipe.rect.y + pipe.rect.height + 1
            while self.rect.y != desired_player_y:
                self.rect.y += 1
                self.game.events()
                self.game.draw()

        if pipe.rotation_dir is RotationDirection.RIGHT:
            desired_player_x = pipe.rect.x + pipe.rect.width + 1
            while self.rect.x != desired_player_x:
                self.rect.x += 1
                self.game.events()
                self.game.draw()

    def finish_level(self):
        self.game.pause_music()
        self.game.play_sound(SoundName.LEVEL_COMPLETE)
        self.game.level_finished = True
        self.player_state = EntityState.GROUNDED_RIGHT
        while self.rect.x < self.game.size[0]:
            self.rect.x += self.speed
            self.animate()
            self.game.draw()
        sleep(5)
        if self.game.current_map_id is not MapId.LEVEL_4_1:
            self.game.current_map_id = self.game.current_map_id.get_next_map()
            self.game.load_map()
        else:
            self.game.playing = False
            self.game.victory_screen()

