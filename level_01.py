import pygame
from nax import SCREEN_HEIGHT, PROJECT_DIR, COLORS
from nax.level import Level
from nax.items import Background, Platform
from nax.enemy import Enemy


class Level01(Level):
    def __init__(self, player):
        super().__init__(player)

        self.background = Background(PROJECT_DIR + '/background.png', [0, 0])
        self.background1_x = 0
        self.background2_x = self.background.image.get_width()

        self.add_platforms([
            # x, y, with, screen_height
            [0, SCREEN_HEIGHT - 15, 100, 15],
            [250, SCREEN_HEIGHT - 15, 550, 15],
            [350, SCREEN_HEIGHT - 85, 350, 15],
            [1000, SCREEN_HEIGHT - 15, 50, 15],
            [1200, SCREEN_HEIGHT - 15, 550, 15],
            [1400, SCREEN_HEIGHT - 85, 50, 15],
            [1550, SCREEN_HEIGHT - 125, 50, 15],
            [1870, SCREEN_HEIGHT - 100, 80, 15],
            [2050, SCREEN_HEIGHT - 15, 20, 15],
            [2150, SCREEN_HEIGHT - 15, 20, 15],
            [2250, SCREEN_HEIGHT - 45, 20, 45],
            [2250, 0, 20, 160],
        ])

        platform = Platform(2500, 0, 20, SCREEN_HEIGHT, 'WHITE')
        platform.is_end = True

        self.platform_list.add(platform)

        self.enemy_list = pygame.sprite.Group()

        enemy = Enemy(300, 200)
        enemy.walls = self.platform_list
        enemy.player = player
        self.enemy_list.add(enemy)

        enemy = Enemy(480, 100)
        enemy.walls = self.platform_list
        enemy.player = player
        self.enemy_list.add(enemy)

        enemy = Enemy(1430, 100, 3)
        enemy.walls = self.platform_list
        enemy.player = player
        self.enemy_list.add(enemy)

    def draw(self, screen):
        """ Draw everything on this level. """

        speed = self.player.change_x / 10
        if speed < .1:
            speed = .1

        self.background1_x -= 1.5 + speed
        self.background2_x -= 1.5 + speed

        screen.fill(COLORS.get('BLACK'))
        screen.blit(self.background.image, (self.background1_x, 0))
        screen.blit(self.background.image, (self.background2_x, 0))

        if self.background1_x <= -1 * self.background.image.get_width():
            self.background1_x = self.background2_x + self.background.image.get_width()

        if self.background2_x <= -1 * self.background.image.get_width():
            self.background2_x = self.background1_x + self.background.image.get_width()

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    @staticmethod
    def get_position_win_x():
        return 1500
