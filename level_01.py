import pygame
from nax import SCREEN_HEIGHT, PROJECT_DIR, COLORS
from nax.level import Level
from nax.items import Background


class Level01(Level):
    def __init__(self, player):
        super().__init__(player)

        self.background = Background(PROJECT_DIR + '/background.png', [0, 0])

        self.add_platforms([
            # x, y, with, screen_height
            [0, SCREEN_HEIGHT - 15, 200, 15],
            [250, SCREEN_HEIGHT - 15, 550, 15],
            [350, SCREEN_HEIGHT - 85, 350, 15],
            [1000, SCREEN_HEIGHT - 15, 50, 15],
            [1200, SCREEN_HEIGHT - 15, 550, 15]
        ])

        self.enemy_list = pygame.sprite.Group()

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(COLORS.get('BLACK'))
        screen.blit(self.background.image, (self.world_shift // 3, 0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    @staticmethod
    def get_position_win_x():
        return 1500
