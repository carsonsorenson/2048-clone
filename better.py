import pygame
import random

pygame.init()
display_width = 450
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))
rows = 4

class Colors:
    box_color = (205, 193, 181)
    line_color = (187, 173, 160)
    white = (255, 255, 255)
    red = (255, 0 ,0)
    black = (0, 0, 0)


class Board:
    def __init__(self):
        self.box_dim = 400
        self.padding = 25
        self.line_thickness = 10
        self.top = display_height - self.box_dim - self.padding
        self.bottom = display_height - self.padding
        self.left = self.padding
        self.right = display_width - self.padding
        self.tile_dim = self.box_dim / rows
        self.font = pygame.font.SysFont('Arial', 25)

    def draw_box(self):
        overlay_rect = pygame.Rect(self.left, self.top, self.box_dim, self.box_dim)
        pygame.draw.rect(game_display, Colors.box_color, overlay_rect)

    def draw_lines(self):
        for i in range(rows + 1):
            offset = self.tile_dim * i
            #horizontal lines
            start_pos = (self.left, self.top + offset)
            end_pos = (self.right, self.top + offset)
            pygame.draw.line(game_display, Colors.line_color, start_pos, end_pos, self.line_thickness)

            #vertical lines
            start_pos = (self.left + offset, self.top - (self.line_thickness / 2) + 1)
            end_pos = (self.left + offset, self.bottom + (self.line_thickness / 2))
            pygame.draw.line(game_display, Colors.line_color, start_pos, end_pos, self.line_thickness)

    def draw_tile(self, x, y, num):
        x_pos = self.tile_dim * y + self.left + (self.line_thickness / 2) + 1
        y_pos = self.tile_dim * x + self.top + (self.line_thickness / 2) + 1
        tile = pygame.Rect(x_pos, y_pos, self.tile_dim - self.line_thickness, self.tile_dim - self.line_thickness)
        pygame.draw.rect(game_display, Colors.white, tile)
        text = self.font.render(str(num), True, Colors.black)
        text_rect = text.get_rect()
        text_rect.center = tile.center
        game_display.blit(text, text_rect)

class Tile:
    def __init__(self, row, col, row_shift, col_shift, value):
        self.row = row
        self.col = col
        self.row_shift = row_shift
        self.col_shift = col_shift
        self.value = value
        self.speed = 0

class Tiles:
    def __init__(self):
        self.tile_scale = 100
        self.tiles = [[Tile(row * self.tile_scale, col * self.tile_scale, 0, 0, 0) for col in range(rows)] for row in range(rows)]
        self.random_tile()
        self.transposed = False
        self.updated = True

    def transpose(self):
        tmp = []
        for j in range(len(self.tiles)):
            tmp.append([])
            for i in range(len(self.tiles[0])):
                new_tile = Tile(self.tiles[i][j].col, self.tiles[i][j].row, self.tiles[i][j].col_shift, self.tiles[i][j].row_shift, self.tiles[i][j].value)
                tmp[j].append(new_tile)
        self.tiles = tmp

    def check_transpose(self, direction):
        if direction == 'LEFT' or direction == 'RIGHT':
            if self.transposed:
                self.transpose()
                self.transposed = False
        elif direction == 'UP' or direction == 'DOWN':
            if not self.transposed:
                self.transpose()
                self.transposed = True

    def slide(self, move_speed, direction):
        self.updated = False
        self.check_transpose(direction)
        for i in range(rows):
            zero_count = 0
            if move_speed < 0:
                for j in range(rows):
                    tile = self.tiles[i][j]
                    if tile.value == 0:
                        zero_count += 1
                    else:
                        self.tiles[i][j].col_shift = -(zero_count * self.tile_scale)
                        self.tiles[i][j].speed = zero_count * move_speed
            else:
                for j in range(rows - 1, -1, -1):
                    if self.tiles[i][j].value == 0:
                        zero_count += 1
                    else:
                        self.tiles[i][j].col_shift = zero_count * self.tile_scale
                        self.tiles[i][j].speed = zero_count * move_speed
        self.print_tiles()

    def update_matrix(self):
        new_matrix = [[Tile(row * self.tile_scale, col * self.tile_scale, 0, 0, 0) for col in range(rows)] for row in range(rows)]
        for i in range(rows):
            for j in range(rows):
                tile = self.tiles[i][j]
                if tile.value != 0:
                    new_tile = new_matrix[i][int(tile.col / self.tile_scale)]
                    new_tile.value = tile.value
        self.tiles = new_matrix

    def update(self, tile):
        if tile.col_shift != 0:
            tile.col += tile.speed
            tile.col_shift -= tile.speed
            return True
        return False


    def random_tile(self):
        self.tiles[0][3].value = 2
        self.tiles[0][1].value = 2
        self.tiles[1][2].value = 4
        self.tiles[2][1].value = 8
        self.tiles[2][2].value = 8
        self.tiles[3][0].value = 2
        self.tiles[3][1].value = 2
        self.tiles[3][2].value = 2

    def print_tiles(self):
        for i in self.tiles:
            for j in i:
                print('[', j.row, j.col, j.row_shift, j.col_shift, j.value, j.speed, ']', end=' ')
            print()


class Game:
    def __init__(self):
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.game_board = Tiles()
        self.speed = 1
        self.moving = False

    def draw(self):
        game_display.fill(Colors.white)
        self.board.draw_box()
        self.board.draw_lines()
        self.moving = False
        for i in range(rows):
            for j in range(rows):
                tile = self.game_board.tiles[i][j]
                if self.game_board.update(tile):
                    self.moving = True
                if tile.value != 0:
                    if self.game_board.transposed:
                        self.board.draw_tile(tile.col / self.game_board.tile_scale, tile.row / self.game_board.tile_scale, tile.value)
                    else:
                        self.board.draw_tile(tile.row / self.game_board.tile_scale, tile.col / self.game_board.tile_scale, tile.value)
        if not self.moving and not self.game_board.updated:
            self.game_board.update_matrix()
            self.game_board.updated = True

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event)
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)

    def handle_keypress(self, event):
        if not self.moving:
            if event.key == pygame.K_LEFT:
                self.game_board.slide(-self.speed, 'LEFT')
            elif event.key == pygame.K_RIGHT:
                self.game_board.slide(self.speed, 'RIGHT')
            elif event.key == pygame.K_UP:
                self.game_board.slide(-self.speed, 'UP')
            elif event.key == pygame.K_DOWN:
                self.game_board.slide(self.speed, 'DOWN')


    def terminate(self):
        pygame.quit()
        quit()

def main():
    game = Game()
    game.game_loop()

if __name__ == '__main__':
    main()