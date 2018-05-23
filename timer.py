import pygame
from time import time
from nax import SCREEN_WIDTH


class Timer:
    def __init__(self):
        self.time_start = None
        self.time_stop = None

    def start(self):
        self.time_start = time()

    def stop(self):
        self.time_stop = time() - self.time_start

    def get_time(self):
        return time() - self.time_start


class GameTimer(Timer):
    def __init__(self):
        super().__init__()

        self.font = pygame.font.SysFont(None, 24)

    def display(self, screen):
        screen.blit(
            self.font.render("%0.2f" % self.get_time(), True, (0, 0, 0)),
            (SCREEN_WIDTH - 150, 35)
        )
