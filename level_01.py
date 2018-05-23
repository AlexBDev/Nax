import pygame
from nax import SCREEN_HEIGHT
from nax.level import Level


class Level01(Level):
    def __init__(self):
        super().__init__()

        self.add_platforms([
            # x, y, with, screen_height
            [0, SCREEN_HEIGHT - 15, 200, 15],
            [250, SCREEN_HEIGHT - 15, 550, 15],
            [350, SCREEN_HEIGHT - 85, 350, 15],
            [1000, SCREEN_HEIGHT - 15, 50, 15],
            [1200, SCREEN_HEIGHT - 15, 550, 15]
        ])

    @staticmethod
    def get_position_win_x():
        return 1500
