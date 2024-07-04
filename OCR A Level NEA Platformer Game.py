"""This file is the one that is to be run to begin the program"""
import pygame
from misc.game import Game

if __name__ == "__main__":
    g = Game()  # creates game object

    while g.running:
        if g.playing:
            g.game_functions()
        else:
            g.events()

    pygame.quit()
