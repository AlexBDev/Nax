import pygame
from time import sleep
from nax.game import Game
from nax.timer import GameTimer
from nax import COLORS, SCREEN_WIDTH


class Window(object):

    def __init__(self, screen_width=800, screen_height=600):
        # Call this function so the Pygame library can initialize itself
        pygame.init()

        # Create an 800x600 sized screen
        self.screen = pygame.display.set_mode([screen_width, screen_height])

        # Set the title of the window
        pygame.display.set_caption('Nax')

        self.game = Game()
        self.clock = pygame.time.Clock()
        self.timer = GameTimer(self.screen)

    def run(self):
        done = False
        self.timer.start()

        while not done:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    done = True

                elif self.game.is_player_win():
                    self.game.display_win_screen(self.screen)
                    sleep(5)
                    done = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.game.player.go_left()
                    elif event.key == pygame.K_RIGHT:
                        self.game.player.go_right()
                    elif event.key == pygame.K_SPACE and self.game.player.can_jump:
                        self.game.player.jump(-1)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.game.player.stop()
                    elif event.key == pygame.K_RIGHT:
                        self.game.player.stop()
                    elif event.key == pygame.K_SPACE:
                        self.game.player.jump(1)
                        self.game.player.can_jump = False

            if self.game.player.rect.right >= 500:
                diff = self.game.player.rect.right - 500
                self.game.player.rect.right = 500
                for wall in self.game.platform_sprites:
                    wall.rect.x += -diff

            if self.game.player.rect.left <= 120:
                diff = 120 - self.game.player.rect.left
                self.game.player.rect.left = 120
                for wall in self.game.platform_sprites:
                    wall.rect.x += diff

            self.game.all_sprite_list.update()

            self.screen.fill(COLORS.get('BLACK'))
            self.screen.blit(self.game.BackGround.image, self.game.BackGround.rect)
            self.timer.display()

            self.game.all_sprite_list.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()