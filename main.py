import pygame

# -- Global constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)

# Screen dimensions
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 320


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # Constructor function
    def __init__(self, x, y, speed):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

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

    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x * self.speed
        self.change_y += y * self.speed

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
            self.change_y += .35

        # if self.change_y > SCREEN_HEIGHT:
        #     pygame.event.post(pygame.QUIT)
        # See if we are on the ground.
        # if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
        #     self.change_y = 0
        #     self.rect.y = SCREEN_HEIGHT - self.rect.height

class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """

    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super().__init__()

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption('Test')

# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()

# Make the walls. (x_pos, y_pos, width, height)
wall_list = pygame.sprite.Group()

# wall = Wall(0, 0, 10, 600)
# wall_list.add(wall)
# all_sprite_list.add(wall)
#
# wall = Wall(10, 0, 790, 10)
# wall_list.add(wall)
# all_sprite_list.add(wall)

GROUND = {
    'HEIGHT': 10
}

PLAYER_SPEED = 6

wall = Wall(0, SCREEN_HEIGHT - GROUND.get('HEIGHT'), 200, GROUND.get('HEIGHT'))
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(250, SCREEN_HEIGHT - GROUND.get('HEIGHT'), 50, GROUND.get('HEIGHT'))
wall_list.add(wall)
all_sprite_list.add(wall)

# Create the player paddle object
player = Player(50, 50, 8)
player.walls = wall_list

# Create background
BackGround = Background('background.png', [0, 0])

all_sprite_list.add(player)

clock = pygame.time.Clock()

done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(1, 0)
            elif event.key == pygame.K_SPACE and player.can_jump:
                player.changespeed(0, -1)
            # elif event.key == pygame.K_DOWN:
            #     player.changespeed(0, 00)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(1, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-1, 0)
            elif event.key == pygame.K_SPACE:
                player.changespeed(0, 1)
                player.can_jump = False
            # elif event.key == pygame.K_DOWN:
            #     player.changespeed(0, -3)

    all_sprite_list.update()

    screen.fill(BLACK)
    screen.blit(BackGround.image, BackGround.rect)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()