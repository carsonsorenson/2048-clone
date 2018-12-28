import pygame
import random

pygame.init()
display_width = 450
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))

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
        self.rows = 4
        self.top = display_height - self.box_dim - self.padding
        self.bottom = display_height - self.padding
        self.left = self.padding
        self.right = display_width - self.padding
        self.tile_dim = self.box_dim / self.rows
        self.font = pygame.font.SysFont('Arial', 25)

    def draw_box(self):
        overlay_rect = pygame.Rect(self.left, self.top, self.box_dim, self.box_dim)
        pygame.draw.rect(game_display, Colors.box_color, overlay_rect)

    def draw_lines(self):
        for i in range(self.rows + 1):
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
    def __init__(self, row, col, speed, value):
        self.row = row
        self.col = col
        self.speed = speed
        self.value = value
        self.shift = 0

class Tiles:
    def __init__(self):
        self.tile_scale = 100
        self.rows = 4
        self.tiles = [[Tile(row * self.tile_scale, col * self.tile_scale, 0, 0) for col in range(self.rows)] for row in range(self.rows)]
        self.random_tile()
        self.transposed = False
        self.moving = False
        self.speed = 0
        self.tile_placed = False

    def transpose(self):
        self.transposed = True
        tmp = []
        for j in range(len(self.tiles)):
            tmp.append([])
            for i in range(len(self.tiles[0])):
                new_tile = Tile(self.tiles[i][j].col, self.tiles[i][j].row, self.tiles[i][j].speed, self.tiles[i][j].value)
                tmp[j].append(new_tile)
        self.tiles = tmp

    def check_merge(self, row, move_speed):
        if move_speed < 0:
            for i in range(1, len(row)):
                if row[i - 1].value == row[i].value and row[i - 1].value != 0:
                    row[i].shift = -(i + row[i - 1].shift)
                else:
                    row[i].shift = row[i-1].shift
                row[i].speed += (row[i].shift * abs(move_speed))
        else:
            for i in range(len(row) - 2, -1, -1):
                if row[i + 1].value == row[i].value and row[i + 1].value != 0:
                    row[i].shift = (len(row) - 1 - i) - row[i + 1].shift
                else:
                    row[i].shift = row[i+1].shift
                row[i].speed += (row[i].shift * abs(move_speed))


    def move(self, move_speed):
        self.speed = move_speed
        for i in range(self.rows):
            # Delete all the zeroes in the row
            self.tiles[i] = [tile for tile in self.tiles[i] if tile.value != 0]
            # Push new zero tiles to the end if moving left, push to front if moving to the right
            if move_speed < 0:
                for j in range(self.rows - len(self.tiles[i])):
                    new_tile = Tile(i * self.tile_scale, len(self.tiles[i]) * self.tile_scale, 0, 0)
                    self.tiles[i].append(new_tile)
            else:
                for j in range(self.rows - len(self.tiles[i])):
                    new_tile = Tile(i * self.tile_scale, (self.rows - 1 - len(self.tiles[i])) * self.tile_scale, 0, 0)
                    self.tiles[i].insert(0, new_tile)
            # Assign a speed the tile will move at
            for j in range(self.rows):
                self.tiles[i][j].speed = (j - (self.tiles[i][j].col / self.tile_scale)) * abs(move_speed)
            self.check_merge(self.tiles[i], move_speed)
        self.print_tiles()

    def tile_reset(self):
        if self.speed > 0:
            for i in range(self.rows - 1, -1, -1):
                for j in range(self.rows -1, -1, -1):
                    tile = self.tiles[i][j]
                    if tile.shift != 0:
                        new_tile = self.tiles[i][j + tile.shift]
                        new_tile.value = tile.value * 2
                        tile.value = 0
                        tile.shift = 0
        else:
            for i in range(self.rows):
                for j in range(self.rows):
                    tile = self.tiles[i][j]
                    if tile.shift != 0:
                        new_tile = self.tiles[i][j + tile.shift]
                        new_tile.value = tile.value * 2
                        tile.value = 0
                        tile.shift = 0


    def update(self):
        self.moving = False
        for i in range(self.rows):
            for j in range(self.rows):
                tile = self.tiles[i][j]
                col = tile.col / self.tile_scale
                row = tile.row / self.tile_scale
                target_col = j
                if tile.shift != 0:
                    target_col += tile.shift
                if not self.transposed:
                    if col < target_col and tile.speed > 0:
                        self.moving = True
                        tile.col += tile.speed
                    elif col > target_col and tile.speed < 0:
                        self.moving = True
                        tile.col += tile.speed
                    else:
                        tile.col = j * self.tile_scale
                        tile.speed = 0
                else:
                    if row < i and tile.speed > 0:
                        self.moving = True
                        tile.row += tile.speed
                    elif row > i and tile.speed < 0:
                        self.moving = True
                        tile.row += tile.speed
                    else:
                        tile.row = i * self.tile_scale
                        tile.speed = 0
        if not self.moving:
            if not self.tile_placed:
                self.random_tile()
            self.tile_reset()


    def random_tile(self):
        self.tile_placed = True
        random_pool = []
        for i in range(self.rows):
            for j in range(self.rows):
                if self.tiles[i][j].value == 0:
                    random_pool.append((i, j))
        choice = random.choice(random_pool)
        self.tiles[choice[0]][choice[1]].value = 2

    def print_tiles(self):
        for i in self.tiles:
            for j in i:
                print('[', j.row, j.col, j.speed, j.value, j.shift, ']', end=' ')
            print()


class Game:
    def __init__(self):
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.game_board = Tiles()
        self.rows = 4
        self.speed = 1

    def draw(self):
        game_display.fill(Colors.white)
        self.board.draw_box()
        self.board.draw_lines()
        self.game_board.update()
        for i in range(self.rows):
            for j in range(self.rows):
                tile = self.game_board.tiles[i][j]
                if tile.value != 0:
                    self.board.draw_tile(tile.row / self.game_board.tile_scale, tile.col / self.game_board.tile_scale, tile.value)

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
        if not self.game_board.moving:
            self.game_board.tile_placed = False
            if event.key == pygame.K_LEFT:
                self.game_board.move(-self.speed)
                self.game_board.transposed = False
            elif event.key == pygame.K_RIGHT:
                self.game_board.move(self.speed)
                self.game_board.transposed = False
            elif event.key == pygame.K_UP:
                self.game_board.transpose()
                self.game_board.move(-self.speed)
                self.game_board.transpose()
            elif event.key == pygame.K_DOWN:
                self.game_board.transpose()
                self.game_board.move(self.speed)
                self.game_board.transpose()


    def terminate(self):
        pygame.quit()
        quit()

def main():
    game = Game()
    game.game_loop()

if __name__ == '__main__':
    main()