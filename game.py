import pygame
from nax.player import Player
from nax.enemy import Enemy
from nax.level_01 import Level01
from nax.items import Background
from nax import PROJECT_DIR


class Game():
    def __init__(self, screen_height):
        self.level = Level01()

        # position_enemies = [25, screen_height - 15]
        # self.enemy = Enemy(150, 15)

        # Create the player paddle object
        self.player = Player(50, 50, 15)
        self.platform_sprites = self.level.get_sprites()
        self.player.walls = self.level.get_sprites()
        # self.enemy.walls = self.level.get_sprites()

        # Create background
        self.BackGround = Background(PROJECT_DIR + '/background.png', [0, 0])

        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.player)
        self.all_sprite_list.add(self.platform_sprites)
        # self.all_sprite_list.add(self.enemy)

    def is_player_win(self):
        return self.player.distance >= self.level.get_position_win_x()
