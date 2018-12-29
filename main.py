import pygame
import random

pygame.init()
display_width = 500
display_height = 650
game_display = pygame.display.set_mode((display_width, display_height))
rows = 4

class Colors:
    box_color = (205, 193, 181)
    line_color = (187, 173, 160)
    white = (255, 255, 255)
    red = (255, 0 ,0)
    black = (0, 0, 0)
    tile = {
        '2'   : (238, 228, 218),
        '4'   : (237, 224, 200),
        '8'   : (242, 177, 121),
        '16'  : (245, 149, 99 ),
        '32'  : (246, 124, 95 ),
        '64'  : (246, 94 , 59 ),
        '128' : (237, 207, 114),
        '256' : (237, 204, 97 ),
        '512' : (237, 200, 80 ),
        '1024': (237, 197, 63 ),
        '2048': (237, 194, 46 ),
        'inf' : (60,  58,  50 ),
    }


class Board:
    def __init__(self):
        self.box_dim = 420
        self.padding = (display_width - self.box_dim) / 2
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
        if str(num) in Colors.tile.keys():
            tile_color = Colors.tile[str(num)]
        else:
            tile_color = Colors.tile['inf']
        pygame.draw.rect(game_display, tile_color, tile)
        text = self.font.render(str(num), True, Colors.black)
        text_rect = text.get_rect()
        text_rect.center = tile.center
        game_display.blit(text, text_rect)

class Tile:
    def __init__(self, row, col, shift, value):
        self.row = row
        self.col = col
        self.shift = shift
        self.value = value
        self.speed = 0
        self.double = False

class Tiles:
    def __init__(self):
        self.two_probability = 0.9
        self.tile_scale = 12
        self.tiles = [[Tile(row * self.tile_scale, col * self.tile_scale, 0, 0) for col in range(rows)] for row in range(rows)]
        self.random_tile()
        self.random_tile()
        self.transposed = False
        self.updated = True
        self.moved = False
        self.score = 0
        # These variables are used to determine merging of tiles
        self.current_tile = None
        self.shift_amount = 0
        self.prev_tile = None
        self.merged = False

    def transpose(self):
        tmp = []
        for j in range(len(self.tiles)):
            tmp.append([])
            for i in range(len(self.tiles[0])):
                new_tile = Tile(self.tiles[i][j].col, self.tiles[i][j].row, self.tiles[i][j].shift, self.tiles[i][j].value)
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
            self.shift_amount = 0
            self.prev_tile = None
            self.merged = False
            if move_speed < 0:
                for j in range(rows):
                    self.current_tile = self.tiles[i][j]
                    self.check_merge(-self.tile_scale, move_speed)
            else:
                for j in range(rows - 1, -1, -1):
                    self.current_tile = self.tiles[i][j]
                    self.check_merge(self.tile_scale, move_speed)

    def check_merge(self, scale, move_speed):
        if self.current_tile.value == 0:
            self.shift_amount += scale
        elif self.prev_tile:
            if self.current_tile.value == self.prev_tile.value and not self.merged:
                self.shift_amount = self.prev_tile.col + self.prev_tile.shift - self.current_tile.col
                self.merged = True
                self.current_tile.double = True
                self.prev_tile.double = True
            else:
                self.shift_amount = self.prev_tile.col + self.prev_tile.shift - self.current_tile.col - scale
                self.merged = False
        if self.current_tile.value != 0:
            self.current_tile.shift = self.shift_amount
            self.current_tile.speed = self.shift_amount / abs(scale) * abs(move_speed)
            self.prev_tile = self.current_tile
        # check to see if one of tiles has moved so we know to add a new random tile
        if self.current_tile.speed != 0:
            self.moved = True

    def update_matrix(self):
        new_matrix = [[Tile(row * self.tile_scale, col * self.tile_scale, 0, 0) for col in range(rows)] for row in range(rows)]
        for i in range(rows):
            for j in range(rows):
                tile = self.tiles[i][j]
                if tile.value != 0:
                    new_tile = new_matrix[i][int(tile.col / self.tile_scale)]
                    new_tile.value = tile.value
                    if tile.double:
                        new_tile.value *= 2
                        self.score += tile.value
        self.tiles = new_matrix
        if self.moved:
            self.random_tile()
        print(self.score)

    def update(self, tile):
        if tile.shift != 0:
            tile.col += tile.speed
            tile.shift -= tile.speed
            return True
        return False


    def random_tile(self):
        self.moved = False
        random_pool = []
        for i in range(rows):
            for j in range(rows):
                if self.tiles[i][j].value == 0:
                    random_pool.append((i, j))
        choice = random.choice(random_pool)
        if random.random() < self.two_probability:
            self.tiles[choice[0]][choice[1]].value = 2
        else:
            self.tiles[choice[0]][choice[1]].value = 4
        if len(random_pool) == 1:
            print('check for game over')

    def print_tiles(self):
        for i in self.tiles:
            for j in i:
                print('[', j.row, j.col, j.shift, j.value, j.speed, ']', end=' ')
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