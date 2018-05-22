import pygame

from nax import PROJECT_DIR
from nax.items import Wall, Background
from nax.player import Player
from nax.level_01 import Level01
from nax import COLORS

class Window(object):

    def __init__(self, screen_width=800, screen_height=600):
        # Call this function so the Pygame library can initialize itself
        pygame.init()

        # Create an 800x600 sized screen
        self.screen = pygame.display.set_mode([screen_width, screen_height])

        # Set the title of the window
        pygame.display.set_caption('Nax')

        self.platforms = Level01([
            # x, y, with, screen_height
            [0, screen_height - 15, 200, 15],
            [250, screen_height - 15, 550, 15],
            [1200, screen_height - 15, 550, 15]
        ])

        # Create the player paddle object
        self.player = Player(50, 50, 15)
        self.platform_sprites = self.platforms.get_sprites()
        self.player.walls = self.platforms.get_sprites()

        # Create background
        self.BackGround = Background(PROJECT_DIR + '/background.png', [0, 0])

        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.player)
        self.all_sprite_list.add(self.platform_sprites)

        self.clock = pygame.time.Clock()

    def run(self):
        done = False

        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.changespeed(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.player.changespeed(1, 0)
                    elif event.key == pygame.K_SPACE and self.player.can_jump:
                        self.player.changespeed(0, -1)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.changespeed(1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.player.changespeed(-1, 0)
                    elif event.key == pygame.K_SPACE:
                        self.player.changespeed(0, 1)
                        self.player.can_jump = False

            if self.player.rect.right >= 500:
                diff = self.player.rect.right - 500
                self.player.rect.right = 500
                for wall in self.platform_sprites:
                    wall.rect.x += -diff

            if self.player.rect.left <= 120:
                diff = 120 - self.player.rect.left
                self.player.rect.left = 120
                for wall in self.platform_sprites:
                    wall.rect.x += diff

            self.all_sprite_list.update()

            self.screen.fill(COLORS.get('BLACK'))
            self.screen.blit(self.BackGround.image, self.BackGround.rect)

            self.all_sprite_list.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()