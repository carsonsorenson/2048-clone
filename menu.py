import pygame
from settings import Settings

class Menu:
    def __init__(self):
        self.score_box = pygame.Rect(Settings.menu_left, Settings.menu_pos, 150, Settings.menu_height)
        self.restart_box = pygame.Rect(Settings.menu_left + self.score_box.width + Settings.menu_gap, Settings.menu_pos, 85, Settings.menu_height)

    def draw(self, score):
        self.draw_score(score)
        self.draw_restart()

    def draw_score(self, score):
        pygame.draw.rect(Settings.game_display, Settings.theme.box_color, self.score_box)
        score_text = Settings.menu_font.render('Score: ' + str(score), True, Settings.theme.black)
        score_rect = score_text.get_rect()
        score_rect.center = self.score_box.center
        Settings.game_display.blit(score_text, score_rect)

    def draw_restart(self):
        pygame.draw.rect(Settings.game_display, Settings.theme.box_color, self.restart_box)
        restart_text = Settings.menu_font.render('Restart', True, Settings.theme.black)
        restart_rect = restart_text.get_rect()
        restart_rect.center = self.restart_box.center
        Settings.game_display.blit(restart_text, restart_rect)
