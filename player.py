import pygame
from nax.items import Background
from nax.spritesheet import SpriteSheet
from nax import PROJECT_DIR, SCREEN_HEIGHT, COLORS, OPTIONS
from nax.setting import setting


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # Constructor function
    def __init__(self, x=0, y=0, speed=10):
        # Call the parent's constructor
        super().__init__()

        self.walking_frames_l = []
        self.walking_frames_r = []
        self.distance = 0
        self.is_die = False
        self.is_hit = False
        self.hit_times = 0
        self.lives = 3
        self.hearts = pygame.sprite.Group()

        i = 0
        while i < self.lives:
            self.hearts.add(Background(PROJECT_DIR+"/assets/HUD/hud_heartFull.png", [15 + (i*70), 20]))
            i += 1

        # Make our top-left corner the passed-in location.
        sprite_sheet = SpriteSheet(PROJECT_DIR+"/assets/Player/p1_walk/p1_walk.png")

        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # What direction is the player facing?
        self.direction = "R"

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None
        self.enemy_list = None

        # Custom
        self.speed = speed
        self.can_jump = True
        self.rect.x = x
        self.rect.y = y
        self.has_win = False

    def stop(self):
        self.change_x = 0

    def go_right(self):
        self.change_x += self.speed
        self.direction = "R"

    def go_left(self):
        self.change_x += -1 * self.speed
        self.direction = "L"

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
        # self.distance += self.change_x
        if self.is_hit:
            self.hit_times += 1
            if self.hit_times == 10:
                self.is_hit = False
                self.change_y = 0
                self.change_x = 0
                self.hit_times = 0

        pos = self.rect.x
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        self._calc_hit_walls()
        self._calc_collide_enemies()

    def _calc_hit_walls(self):
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if block.is_end:
                self.has_win = True
                return

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

        if self.change_y > SCREEN_HEIGHT and not setting.is_dev_mode():
            self.is_die = True
            # pygame.event.post(pygame.QUIT)
        # elif self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
        #     self.change_y = 0
        #     self.rect.y = SCREEN_HEIGHT - self.rect.height

    def _calc_collide_enemies(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.enemy_list, False)
        for block in block_hit_list:
            diff = self.rect.x - block.rect.x
            self.is_hit = True
            self.lives -= 1

            if self.lives >= 0:
                self.hearts.remove(self.hearts.sprites()[-1])

            if self.lives == 0 and not setting.is_dev_mode():
                self.is_die = True

            # self.hearts.remove(self.hearts.)
            if (diff > 0):
                self.change_x = 15
                self.change_y = 15
            else:
                self.change_x = -15
                self.change_y = -15

            return

            # self.is_die = True
