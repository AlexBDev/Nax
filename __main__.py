import pygame
from sys import argv
from nax import SCREEN_WIDTH, SCREEN_HEIGHT
from nax.window import Window
from nax.setting import setting


if 2 <= len(argv):
    setting.game_mode = argv[1]

win = Window(SCREEN_WIDTH, SCREEN_HEIGHT)
win.run()
