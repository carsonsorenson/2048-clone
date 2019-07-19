import pygame
import theme


class Settings:
    #entire window
    display_width = 500
    display_height = 650
    game_display = pygame.display.set_mode((display_width, display_height))
    rows = 4
    theme = theme.Light()

    #game window
    game_dimension = 420
    game_padding = (display_width - game_dimension) / 2
    game_line_thickness = 10

    #positions of game window
    game_top = display_height - game_dimension - game_padding
    game_bottom = display_height - game_padding
    game_left = game_padding
    game_right = display_width - game_padding

    #Tile settings
    starting_two_probability = 0.9
    tile_scale = 10

    #Game over positions
    game_over_left = game_left - game_line_thickness / 2
    game_over_top = game_top - game_line_thickness / 2
    game_over_dimension = game_dimension + game_line_thickness + 1
    game_over_alpha = 185

    #Menu options
    menu_font = pygame.font.SysFont('calibri', 20)
    menu_height = 40
    menu_pos = 110
    menu_left = 35
    menu_gap = 20

    #Pregame Menu options
    pregame_width = 250
    pregame_height = 40
    pregame_left = (display_width / 2) - (pregame_width / 2)
    arrow_width = 30
    pregame_options = {0: 'Tiny(2x2)', 1: 'Small(3x3)', 2: 'Classic(4x4)', 3: 'Big(5x5)', 4: 'Huge(6x6)', 5: 'Giant(8x8)'}
