import pygame
from nax.level import Level
from nax.items import Wall


class Level01(Level):

    def __init__(self, platforms):
        self.platform_list = pygame.sprite.Group()

        for platform in platforms:
            self.platform_list.add(Wall(platform[0], platform[1], platform[2], platform[3]))

    def get_sprites(self):
        return self.platform_list

    @staticmethod
    def get_position_win_x():
        return 1500
