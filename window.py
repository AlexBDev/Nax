import pygame
from nax.game import Game


class Window(object):

    def __init__(self, screen_width=800, screen_height=600):
        pygame.init()
        pygame.display.set_caption('Nax')

        self.screen = pygame.display.set_mode([screen_width, screen_height])
        self.clock = pygame.time.Clock()

        self.game = Game(self.screen)

    def run(self):
        done = False
        restart = False

        while not done:
            for event in pygame.event.get():
                restart = self.game.event(event)

            if restart:
                self.game = Game(self.screen)
                restart = False

            pygame.display.flip()
            self.game.update()
            self.game.draw()
            self.clock.tick(60)


        pygame.quit()
