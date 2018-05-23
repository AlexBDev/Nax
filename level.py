import abc
import pygame
from nax.items import Platform
from nax import COLORS


class Level(metaclass=abc.ABCMeta):
    def __init__(self, player):
        self.background = None
        self.world_shift = 0
        self.player = player
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()

    def get_sprites(self):
        return self.platform_list

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        screen.fill(COLORS.get('BLUE'))
        screen.blit(self.background, (self.world_shift // 3, 0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def add_platforms(self, platforms):
        for platform in platforms:
            self.platform_list.add(Platform(platform[0], platform[1], platform[2], platform[3]))
