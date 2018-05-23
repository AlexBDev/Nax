import abc
import pygame
from nax.items import Platform


class Level(metaclass=abc.ABCMeta):
    def __init__(self):
        self.platform_list = pygame.sprite.Group()

    def get_sprites(self):
        return self.platform_list

    def add_platforms(self, platforms):
        for platform in platforms:
            self.platform_list.add(Platform(platform[0], platform[1], platform[2], platform[3]))
