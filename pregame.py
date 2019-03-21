import pygame
from settings import Settings


class Pregame:
    def __init__(self):
        self.start_game_box = pygame.Rect(Settings.pregame_left, 350, Settings.pregame_width, Settings.pregame_height)
        self.left_arrow = pygame.Rect(Settings.pregame_left, 250, Settings.arrow_width, Settings.pregame_height)
        self.right_arrow = pygame.Rect(Settings.pregame_left + Settings.pregame_width - Settings.arrow_width, 250, Settings.arrow_width, Settings.pregame_height)
        self.options = pygame.Rect(Settings.pregame_left + Settings.arrow_width, 250, Settings.pregame_width - (Settings.arrow_width * 2), Settings.pregame_height)
        self.arr_pos = 2

    def draw(self, index):
        self.arr_pos = index
        self.draw_start_game()
        self.draw_size_options()

    def draw_start_game(self):
        pygame.draw.rect(Settings.game_display, Settings.theme.box_color, self.start_game_box)
        start_text = Settings.menu_font.render('Start Game', True, Settings.theme.black)
        start_rect = start_text.get_rect()
        start_rect.center = self.start_game_box.center
        Settings.game_display.blit(start_text, start_rect)

    def draw_size_options(self):
        if self.arr_pos != 0:
            pygame.draw.rect(Settings.game_display, Settings.theme.background, self.left_arrow)
            left_arrow_text = Settings.menu_font.render('<', True, Settings.theme.black)
            left_rect = left_arrow_text.get_rect()
            left_rect.center = self.left_arrow.center
            Settings.game_display.blit(left_arrow_text, left_rect)
        if self.arr_pos != len(Settings.pregame_options) - 1:
            pygame.draw.rect(Settings.game_display, Settings.theme.background, self.right_arrow)
            right_arrow_text = Settings.menu_font.render('>', True, Settings.theme.black)
            right_rect = right_arrow_text.get_rect()
            right_rect.center = self.right_arrow.center
            Settings.game_display.blit(right_arrow_text, right_rect)
        pygame.draw.rect(Settings.game_display, Settings.theme.box_color, self.options)
        option_text = Settings.menu_font.render(Settings.pregame_options[self.arr_pos], True, Settings.theme.black)
        option_rect = option_text.get_rect()
        option_rect.center = self.options.center
        Settings.game_display.blit(option_text, option_rect)
