import pygame
from nax import COLORS

# Screen dimensions
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 320


class Enemy(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # Constructor function
    def __init__(self, x, y, speed=10):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(COLORS.get('BLACK'))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None

        # Custom
        self.speed = speed
        self.can_jump = True

    def stop(self):
        self.change_x = 0

    def go_right(self):
        self.change_x += self.speed

    def go_left(self):
        self.change_x += -1 * self.speed

    def jump(self, x):
        """ Change the speed of the player. """
        self.change_y += x * self.speed

    def update(self):
        """ Move the player. """
        # Gravity
        self._calc_grav()

        # The game exit, when player fall into the void
        if self.rect.y > SCREEN_HEIGHT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Move left/right
        self.rect.x += self.change_x
        self._calc_hit_walls()

    def _calc_hit_walls(self):
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0
            self.can_jump = True

    def _calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 1.35

        # if self.change_y > SCREEN_HEIGHT:
        #     pygame.event.post(pygame.QUIT)
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
