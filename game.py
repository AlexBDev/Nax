import pygame
from nax.player import Player
from nax.level_01 import Level01
from nax import PROJECT_DIR, COLORS
from nax.timer import GameTimer
from time import sleep
from nax.setting import setting
from os.path import exists


class Game():
    def __init__(self, screen):

        self.high_score = 'Any'
        if not exists(PROJECT_DIR+'/scores.data'):
            with open(PROJECT_DIR + '/scores.data', 'a') as file:
                file.close()

        with open(PROJECT_DIR+'/scores.data', 'r') as content_file:
            content = content_file.read()
            scores = []
            for score in content.split("\n"):
                if score.strip():
                    scores.append(float(score))

            if len(scores):
                self.high_score = sorted(scores, key=float)[0]

        self.screen = screen
        self.timer = GameTimer()
        self.player = Player(0, 0, 15)
        self.level = Level01(self.player)
        self.platform_sprites = self.level.get_sprites()
        self.player.walls = self.platform_sprites
        self.player.enemy_list = self.level.enemy_list
        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.player)
        self.timer.start()
        pygame.mixer.music.load(PROJECT_DIR + "/assets/music.mp3")
        pygame.mixer.music.play(-1)

    def event(self, event):
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.go_left()
            elif event.key == pygame.K_RIGHT:
                self.player.go_right()
            elif event.key == pygame.K_SPACE and self.player.can_jump:
                self.player.jump(-1)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.player.stop()
            elif event.key == pygame.K_RIGHT:
                self.player.stop()
            elif event.key == pygame.K_SPACE:
                self.player.jump(1)
                if not setting.is_dev_mode():
                    self.player.can_jump = False

        return False

    def update(self):

        for enemy in self.level.enemy_list:
            if enemy.is_die:
                self.level.enemy_list.remove(enemy)

        self.all_sprite_list.update()
        self.level.update()

        if self.player.has_win:
            self._save_score()
            self.display_win_screen(self.screen)
            sleep(.5)
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        if self.player.is_die:
            self.display_die_screen()
            sleep(.5)
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _save_score(self):
        file = open(PROJECT_DIR+'/scores.data', 'a')
        file.write("%0.2f" % self.timer.get_time() + "\n")
        file.close()

    def draw(self):
        self.level.draw(self.screen)
        # self.screen.blit(self.player.hearts.image)
        self.all_sprite_list.draw(self.screen)
        self.player.hearts.draw(self.screen)
        self.timer.display(self.screen)
        self.display_high_score_screen()

    def is_player_win(self):
        return self.player.distance >= self.level.get_position_win_x()

    def display_die_screen(self):
        font = pygame.font.SysFont(None, 48)
        text = font.render('You die', True, COLORS.get('RED'), None)
        text_rect = text.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx
        text_rect.centery = self.screen.get_rect().centery
        self.screen.blit(text, text_rect)
        self.all_sprite_list.draw(self.screen)
        pygame.display.flip()

    def display_win_screen(self, screen):
        font = pygame.font.SysFont(None, 48)
        text = font.render('You win mofos !', True, COLORS.get('WHITE'), None)
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery
        screen.blit(text, text_rect)
        self.all_sprite_list.draw(screen)
        pygame.display.flip()

    def display_high_score_screen(self):
        font = pygame.font.SysFont(None, 18)
        text = font.render('HIGH SCORE : '+str(self.high_score), True, COLORS.get('BLACK'), None)
        text_rect = text.get_rect()
        text_rect.centerx = 75
        text_rect.centery = 100
        self.screen.blit(text, text_rect)
        self.all_sprite_list.draw(self.screen)
        pygame.display.flip()
