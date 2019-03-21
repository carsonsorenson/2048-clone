import pygame
import re
pygame.init()
from settings import Settings
from menu import Menu
from pregame import Pregame
from tiles import Tiles


def game_loop():
    fps = 60
    clock = pygame.time.Clock()
    game = Tiles()
    menu = Menu()
    pre = Pregame()
    index = 2
    pregame = True
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                handle_keypress(event, game)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if menu.restart_box.collidepoint(pos) and not pregame:
                    done = True
                elif pre.start_game_box.collidepoint(pos) and pregame:
                    set_setttings(index)
                    game = Tiles()
                    pregame = False
                elif pre.left_arrow.collidepoint(pos) and pregame:
                    if index > 0:
                        index -= 1
                elif pre.right_arrow.collidepoint(pos) and pregame:
                    if index < len(Settings.pregame_options) - 1:
                        index += 1
        pygame.display.update()
        Settings.game_display.fill(Settings.theme.background)
        if not pregame:
            game.draw()
            menu.draw(game.score)
        else:
            pre.draw(index)
        clock.tick(fps)


def set_setttings(index):
    rows = Settings.pregame_options[index]
    Settings.rows = int(re.match(r'^.*\((\d*)', rows).group(1))
    Settings.game_line_thickness = 12 - Settings.rows


def handle_keypress(event, game):
    if not game.moving:
        if event.key == pygame.K_LEFT:
            game.slide(-1, False)
        elif event.key == pygame.K_RIGHT:
            game.slide(1, False)
        elif event.key == pygame.K_UP:
            game.slide(-1, True)
        elif event.key == pygame.K_DOWN:
            game.slide(1, True)


def terminate():
    pygame.quit()
    quit()


def main():
    while True:
        game_loop()


if __name__ == '__main__':
    main()