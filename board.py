import pygame
from settings import Settings
import math

class Board:
    def __init__(self):
        self.tile_dim = Settings.game_dimension / Settings.rows
        self.game_over_font = pygame.font.SysFont('calibri', 50)
        self.large_font = pygame.font.SysFont('calibri', int(self.tile_dim / 2.5))
        self.medium_font = pygame.font.SysFont('calibri', int(self.tile_dim / 3))
        self.small_font = pygame.font.SysFont('calibri', int(self.tile_dim / 3.5))

    def draw(self):
        self.draw_game_board()
        self.draw_game_lines()

    def draw_game_board(self):
        game_board_rect = pygame.Rect(Settings.game_left, Settings.game_top, Settings.game_dimension, Settings.game_dimension)
        pygame.draw.rect(Settings.game_display, Settings.theme.box_color, game_board_rect)

    def draw_game_lines(self):
        for i in range(Settings.rows + 1):
            offset = self.tile_dim * i
            # horizontal lines
            start_pos = (Settings.game_left, Settings.game_top + offset)
            end_pos = (Settings.game_right, Settings.game_top + offset)
            pygame.draw.line(Settings.game_display, Settings.theme.line_color, start_pos, end_pos, Settings.game_line_thickness)
            # vertical lines
            start_pos = (Settings.game_left + offset, Settings.game_top - (Settings.game_line_thickness / 2) + 1)
            end_pos = (Settings.game_left + offset, Settings.game_bottom + (Settings.game_line_thickness / 2))
            pygame.draw.line(Settings.game_display, Settings.theme.line_color, start_pos, end_pos, Settings.game_line_thickness)

    def draw_game_tile(self, x, y, value):
        x_pos = self.tile_dim * y + Settings.game_left + (Settings.game_line_thickness / 2) + 1
        y_pos = self.tile_dim * x + Settings.game_top + (Settings.game_line_thickness / 2) + 1
        tile = pygame.Rect(x_pos, y_pos, self.tile_dim - Settings.game_line_thickness, self.tile_dim - Settings.game_line_thickness)
        if str(value) in Settings.theme.tile.keys():
            tile_color = Settings.theme.tile[str(value)]
        else:
            tile_color = Settings.theme.tile['inf']
        pygame.draw.rect(Settings.game_display, tile_color, tile)
        length = math.log10(value)
        if length <= 2:
            tile_value = self.large_font.render(str(value), True, Settings.theme.black)
        elif length <= 5:
            tile_value = self.medium_font.render(str(value), True, Settings.theme.black)
        else:
            tile_value = self.small_font.render(str(value), True, Settings.theme.black)
        tile_rect = tile_value.get_rect()
        tile_rect.center = tile.center
        Settings.game_display.blit(tile_value, tile_rect)

    def draw_game_over(self):
        background = pygame.Surface((Settings.game_over_dimension, Settings.game_over_dimension))
        background.set_alpha(Settings.game_over_alpha)
        background.fill(Settings.theme.background)
        game_over_text = self.game_over_font.render('Game Over', True, Settings.theme.black)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = pygame.Rect(Settings.game_over_left, Settings.game_over_top, Settings.game_over_dimension, Settings.game_over_dimension).center
        Settings.game_display.blit(background, (Settings.game_over_left, Settings.game_over_top))
        Settings.game_display.blit(game_over_text, game_over_rect)