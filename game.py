import pygame
from nax.player import Player
from nax.level_01 import Level01
from nax.items import Background
from nax import PROJECT_DIR


class Game():
    def __init__(self, screen_height):
        self.platforms = Level01([
            # x, y, with, screen_height
            [0, screen_height - 15, 200, 15],
            [250, screen_height - 15, 550, 15],
            [350, screen_height - 85, 350, 15],
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
