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
        self.shift_world()

    def draw(self, screen):
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def add_platforms(self, platforms):
        for platform in platforms:
            self.platform_list.add(Platform(platform[0], platform[1], platform[2], platform[3]))

    def shift_world(self):
        """ When the user moves left/right and we need to scroll everything: """

        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500
            self.player.rect.right = 500
            self.background.rect.x += diff
            for platform in self.platform_list:
                platform.rect.x += -diff
            for enemy in self.enemy_list:
                enemy.rect.x += -diff

        if self.player.rect.left <= 120:
            diff = 120 - self.player.rect.left
            self.player.rect.left = 120
            self.background.rect.x += diff
            for platform in self.platform_list:
                platform.rect.x += diff
            for enemy in self.enemy_list:
                enemy.rect.x += diff
