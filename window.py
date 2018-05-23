import pygame
from time import sleep
from nax.game import Game
from nax.timer import GameTimer
from nax import COLORS, SCREEN_WIDTH


class Window(object):

    def __init__(self, screen_width=800, screen_height=600):
        pygame.init()
        pygame.display.set_caption('Nax')

        self.screen = pygame.display.set_mode([screen_width, screen_height])
        self.clock = pygame.time.Clock()

        self.game = Game(self.screen)

    def run(self):
        done = False

        while not done:
            for event in pygame.event.get():
                self.game.event(event, done)

            self.game.update()
            self.game.draw()
            self.clock.tick(60)

            pygame.display.flip()

        pygame.quit()
