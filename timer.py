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


class GameTimer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 24)
        self.timer = Timer()

    def start(self):
        self.timer.start()

    def display(self):
        self.screen.blit(
            self.font.render("%0.2f" % self.timer.get_time(), True, (0, 0, 0)),
            (SCREEN_WIDTH - 150, 35)
        )
