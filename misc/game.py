"""Game class to store all the variables, sprites, maps, as this allows me to run pygame update functions (like draw all
 sprites onto the screen) to all sprites every tick (which is required)"""
from time import sleep

import pygame

from misc.maps import MapId
from misc.constants import *
from misc.colours import Colour
from misc.button import Button
from sounds.sounds import play_music, play_sound, pause_music, MusicName, SoundName
from sprites.sprite_sheets import load_overworld_spritesheets
from sprites.all_sprites import Block, Underground, InvisibleWall, Player, Snake, Pipe, Ground, Key, Brick,\
    Shroom, Bee, Rabbit, EnemyDisappearingBlock, GoalDisappearingBlock, Coin, RotationDirection, GoalLandingBlock,\
    Overlay


class Game:
    """Contains the entire game and all variables and main pygame related functions like draw that continuously display
    all sprites every tick"""
    def __init__(self):
        pygame.init()  # starts pygame module and allows all its functions to work.
        self.size = STARTING_SCREEN_SIZE
        self.screen = pygame.display.set_mode(STARTING_SCREEN_SIZE, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("courier.ttf", 32)
        pygame.display.set_caption("OCR NEA Dungeons Platformer Game")
        self.spritesheets = load_overworld_spritesheets()

        self.map_ids = [Id for Id in MapId]
        self.current_map_id = MapId.LEVEL_1_1
        self.background_colour = Colour.BLACK

        self.all_sprites_group = pygame.sprite.LayeredUpdates()
        self.blocks_group = pygame.sprite.LayeredUpdates()
        self.pipes_group = pygame.sprite.LayeredUpdates()
        self.enemies_group = pygame.sprite.LayeredUpdates()
        self.player_group = pygame.sprite.LayeredUpdates()
        self.coins_group = pygame.sprite.LayeredUpdates()
        self.keys_group = pygame.sprite.LayeredUpdates()
        self.goal_blocks_group = pygame.sprite.LayeredUpdates()
        self.overlay_group = pygame.sprite.LayeredUpdates()

        self.running = True
        self.playing = False

        self.num_lives = 7
        self.overlay = Overlay(self, 0, 0)

        self.key_found = self.coins_collected = self.no_more_enemies = self.level_finished = False

        self.title_screen()

    def events(self):
        """To always run no matter what to catch events like closing the program which are only specific to the game as
        a whole"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = self.running = False
            elif event.type == pygame.VIDEORESIZE:  # Moves camera so everything is in the middle.
                dx = self.screen.get_size()[0] - self.size[0]  # self.screen.get_size()[0] is the new width,
                # self.size[0] is the old width
                dy = self.screen.get_size()[1] - self.size[1]  # same here but with height

                self.size = self.screen.get_size()  # sets the size variable equal to the current size.
                self.move_sprites(dx / 2, dy / 2)

    def update(self):
        """Runs all update functions for all sprites which updates them during the game.
        Only used while 'self.playing = True'."""
        self.all_sprites_group.update()

    def draw(self):
        """Draws all the sprites onto the screen, which has to be done every tick.
        Only used while 'self.playing = True'."""
        self.screen.fill(self.background_colour)
        self.all_sprites_group.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def game_functions(self):
        """Runs 'events', 'update' and 'draw' functions which need to be run every second to update the screen and catch
        hold of events like closing the program which are only specific to the game as a whole"""
        self.events()
        self.update()
        self.draw()

    # _________________________________________________SCREEN FUNCTIONS_________________________________________________
    def display_text(self, words, title_x = None, title_y = None, shifted_up = False, shifted_up_2 = False):
        title = self.font.render(words, True, Colour.WHITE)
        if title_x is None:
            title_x = (self.size[0] - title.get_size()[0]) // 2

        if title_y is None and shifted_up:
            title_y = (self.size[1] - title.get_size()[1]*8) // 2
        if title_y is None and shifted_up_2:
            title_y = (self.size[1] - title.get_size()[1] * 6) // 2
        elif title_y is None:
            title_y = (self.size[1] - title.get_size()[1]) // 2
        title_rect = title.get_rect(x=title_x, y=title_y)  # This stores the title's position

        self.screen.blit(title, title_rect)

    def title_screen(self):
        """Run to create and stay on intro screen until the 'Play' button is clicked. """
        self.screen.fill(Colour.TITLE_SCREEN)
        self.display_text("OCR NEA Dungeons Platformer Game", shifted_up=True)
        self.display_text("By Nehal Jain", shifted_up_2=True)

        play_button = Button(x=275, y=400, width=150, height=100, fg_colour=Colour.WHITE,
                             bg_colour=Colour.BLACK, content="Play", fontsize=32)

        rules_button = Button(x=275, y=520, width=150, height=100, fg_colour=Colour.WHITE,
                              bg_colour=Colour.BLACK, content="Rules", fontsize=32)

        self.screen.blit(play_button.image, play_button.rect)
        self.screen.blit(rules_button.image, rules_button.rect)
        self.clock.tick(FPS)
        pygame.display.update()

        self.pause_music()
        play_music(MusicName.TITLE_THEME)
        self.current_map_id = MapId.LEVEL_1_1

        while self.running:
            self.events()

            # Both of these variables are needed to determine whether the button itself has been clicked.
            mouse_pos = pygame.mouse.get_pos()
            mouse_is_pressed = pygame.mouse.get_pressed()  # Returns a list [l_click, r_click, m_click] and shows
            # whether it has been clicked or not.

            if play_button.is_pressed(mouse_pos, mouse_is_pressed):
                self.load_map()
                break  # ends intro_screen while loop

            if rules_button.is_pressed(mouse_pos, mouse_is_pressed):
                self.rules_screen()
                break  # ends intro_screen while loop

    def game_over_screen(self):
        """Run when self.num_lives = 0"""
        self.screen.fill(Colour.GAME_OVER_SCREEN)
        self.display_text("GAME OVER", shifted_up=True)
        self.display_text("Better Luck Next Time!", shifted_up_2=True)

        play_button = Button(x=225, y=300, width=250, height=100, fg_colour=Colour.WHITE,
                             bg_colour=Colour.BLACK, content="Play Again?", fontsize=32)

        self.screen.blit(play_button.image, play_button.rect)
        self.clock.tick(FPS)
        pygame.display.update()

        self.play_sound(SoundName.GAME_OVER)

        while self.running:
            self.events()

            # Both of these variables are needed to determine whether the button itself has been clicked.
            mouse_pos = pygame.mouse.get_pos()
            mouse_is_pressed = pygame.mouse.get_pressed()  # Returns a list [l_click, r_click, m_click] and shows
            # whether it has been clicked or not.

            if play_button.is_pressed(mouse_pos, mouse_is_pressed):
                sleep(1)
                self.title_screen()
                break  # ends intro_screen while loop

    def victory_screen(self):
        """Run when the player beats the game"""
        self.screen.fill(Colour.VICTORY_SCREEN)
        play_music(SoundName.GAME_COMPLETE)
        self.display_text("WELL DONE YOU WIN!!", shifted_up=True)
        self.display_text("Thanks for playing my game :)", shifted_up_2=True)

        play_button = Button(x=225, y=300, width=250, height=100, fg_colour=Colour.WHITE,
                             bg_colour=Colour.BLACK, content="Play Again?", fontsize=32)

        self.screen.blit(play_button.image, play_button.rect)
        self.clock.tick(FPS)
        pygame.display.update()

        while self.running:
            self.events()

            # Both of these variables are needed to determine whether the button itself has been clicked.
            mouse_pos = pygame.mouse.get_pos()
            mouse_is_pressed = pygame.mouse.get_pressed()  # Returns a list [l_click, r_click, m_click] and shows
            # whether it has been clicked or not.

            if play_button.is_pressed(mouse_pos, mouse_is_pressed):
                self.title_screen()
                break  # ends intro_screen while loop

    def level_load_screen(self):
        pause_music()

        self.screen.fill(Colour.BLACK)
        self.clock.tick(FPS)

        self.display_text(self.current_map_id.get_level_name(), shifted_up_2=True)
        self.overlay.during_level_loading_screen()
        self.overlay_group.draw(self.screen)

        pygame.display.update()
        sleep(2)

    def rules_screen(self):
        rules_image = pygame.image.load("img/rules.png")
        rules_image = pygame.transform.scale(rules_image, self.size)
        self.screen.blit(rules_image, (0,0))

        back_button = Button(x=20, y=20, width=100, height=50, fg_colour=Colour.WHITE,
                             bg_colour=Colour.VICTORY_SCREEN, content="Back", fontsize=32)
        controls_button = Button(x=self.size[0] - 170, y=20, width=160, height=50, fg_colour=Colour.WHITE,
                                 bg_colour=Colour.VICTORY_SCREEN, content="Controls", fontsize=32)

        self.screen.blit(back_button.image, back_button.rect)
        self.screen.blit(controls_button.image, controls_button.rect)
        self.clock.tick(FPS)
        pygame.display.update()

        while self.running:
            self.events()
            mouse_pos = pygame.mouse.get_pos()
            mouse_is_pressed = pygame.mouse.get_pressed()

            if back_button.is_pressed(mouse_pos, mouse_is_pressed):
                self.title_screen()
                break  # ends intro_screen while loop

            elif controls_button.is_pressed(mouse_pos, mouse_is_pressed):
                self.controls_screen()
                break  # ends intro_screen while loop

    def controls_screen(self):
        controls_image = pygame.image.load("img/controls.png")
        controls_image = pygame.transform.scale(controls_image, self.size)
        self.screen.blit(controls_image, (0, 0))

        back_button = Button(x=300, y=600, width=100, height=50, fg_colour=Colour.WHITE,
                             bg_colour=Colour.TITLE_SCREEN, content="Back", fontsize=32)

        self.screen.blit(back_button.image, back_button.rect)
        self.clock.tick(FPS)
        pygame.display.update()

        while self.running:
            self.events()
            mouse_pos = pygame.mouse.get_pos()
            mouse_is_pressed = pygame.mouse.get_pressed()

            if back_button.is_pressed(mouse_pos, mouse_is_pressed):
                self.rules_screen()
                break  # ends intro_screen while loop


    # ________________________________________________LOAD MAP FUNCTIONS________________________________________________
    def load_map(self):
        """Loads a map"""
        if self.current_map_id.is_first_map():  # If new level loading as opposed to new map
            self.level_load_screen()
            play_music(self.current_map_id.get_background_music())

        self.background_colour = self.current_map_id.get_background_colour()
        self.playing = True
        self.empty_screen()
        self.create_map()
        self.centre_character()

        player = [_ for _ in self.player_group][0]
        player.if_exit_pipe()

        self.key_found = not self.is_group_on_screen(self.keys_group)  # True if there is no key, False if there is (as
        # it needs to be found)
        self.no_more_enemies = not self.is_group_on_screen(self.enemies_group)
        self.coins_collected = not self.is_group_on_screen(self.coins_group)

        self.level_finished = False

        self.overlay.during_level()

    def empty_screen(self):
        """Empties screen of any sprites to get ready for next map loading"""
        for entity in self.all_sprites_group:
            if entity not in self.overlay_group:
                entity.remove_from_screen()

    def create_map(self):
        """Creates the map from the blueprints given in the 'maps.py' file."""
        for y, row, in enumerate(self.current_map_id.get_map()):
            for x, item, in enumerate(row):
                if item == "b":
                    Block.create_instance(self, x, y)
                if item == "B":
                    Brick.create_instance(self, x, y)

                elif item == "G":
                    Ground.create_instance(self, x, y)
                elif item == "U":
                    Underground.create_instance(self, x, y)

                elif item == "d":
                    EnemyDisappearingBlock.create_instance(self, x, y)
                elif item == "D":
                    GoalDisappearingBlock.create_instance(self, x, y)
                elif item == "g":
                    GoalLandingBlock.create_instance(self, x, y)
                elif item == "I":
                    InvisibleWall.create_instance(self, x, y)
                elif item == "P":
                    Player.create_instance(self, x, y)
                elif item == "q":
                    Block.create_instance(self,x, y)

                elif item == "K":
                    Key.create_instance(self, x, y)
                elif item == "C":
                    Coin.create_instance(self, x, y)

                elif item == "s":
                    Snake.create_instance(self, x, y)
                elif item == "S":
                    Shroom.create_instance(self, x, y)
                elif item == "z":
                    Bee.create_instance(self, x, y)
                elif item == "R":
                    Rabbit.create_instance(self, x, y)

                elif item == "v":  # facing up
                    Pipe.create_instance(self, x, y, RotationDirection.UP)
                elif item == "V":  # facing down
                    Pipe.create_instance(self, x, y, RotationDirection.DOWN)
                elif item == "h":  # facing left
                    Pipe.create_instance(self, x, y, RotationDirection.LEFT)
                elif item == "H":  # facing right
                    Pipe.create_instance(self, x, y, RotationDirection.RIGHT)

    # __________________________________________________MISC. FUNCTIONS_________________________________________________
    def is_group_on_screen(self, group):
        """Sees if there are any members of group on the screen"""
        all_members = [_ for _ in group]
        for member in all_members:
            if member in self.all_sprites_group:
                return True
        return False

    def move_sprites(self, x, y):
        for sprite in self.all_sprites_group:
            if sprite not in self.overlay_group:
                sprite.rect.x += x
                sprite.rect.y += y

    def centre_character(self):
        """Run whenever a map is newly loaded to centre the character in the camera view"""
        player = [_ for _ in self.player_group][0]  # retrieves player_group sprite

        desired_x = self.size[0] // 2 - (player.rect.width / SCALE_UP)  # I only want to change x as I don't want
        # vertical camera movement, only lateral camera movement.

        # Moves all sprites accordingly until player_group is in right place
        while player.rect.x != desired_x:
            if player.rect.x < desired_x:
                self.move_sprites(1, 0)
            else:
                self.move_sprites(-1, 0)

    # __________________________________________________MUSIC FUNCTIONS_________________________________________________

    def pause_music(self):
        """For other sprites to be able to pause music."""
        pause_music()

    def play_sound(self, sound):
        play_sound(sound)


