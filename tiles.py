from board import Board
from settings import Settings
from tile import Tile
import random


class Tiles:
    def __init__(self):
        self.board = Board()
        self.tiles = self.init_tiles()
        self.shift_amt = 0
        self.moving = False
        self.updated = True
        self.moved = False
        self.transposed = False
        self.starting_tiles = 2
        self.score = 0
        self.init_game()
        self.game_over = False


    def init_game(self):
        tmp = []
        for i in range(Settings.rows):
            for j in range(Settings.rows):
                tmp.append((i, j))
        for i in range(self.starting_tiles):
            choice = random.choice(tmp)
            self.place_random_tile([choice])
            tmp.remove(choice)


    def draw(self):
        self.board.draw()
        self.moving = False
        for i in range(Settings.rows):
            for j in range(Settings.rows):
                tile = self.tiles[i][j]
                if tile.update():
                    self.moving = True
                if tile.value != 0:
                    if self.transposed:
                        self.board.draw_game_tile(tile.col / Settings.tile_scale, tile.row / Settings.tile_scale, tile.value)
                    else:
                        self.board.draw_game_tile(tile.row / Settings.tile_scale, tile.col / Settings.tile_scale, tile.value)
        if not self.moving and not self.updated and self.moved:
            self.update()

        if self.game_over:
            self.board.draw_game_over()

    def init_tiles(self):
        return [[Tile(row * Settings.tile_scale, col * Settings.tile_scale, 0) for col in range(Settings.rows)] for row in range(Settings.rows)]


    def transpose(self):
        self.transposed = not self.transposed
        tmp = []
        for j in range(Settings.rows):
            tmp.append([])
            for i in range(Settings.rows):
                new_tile = Tile(self.tiles[i][j].col, self.tiles[i][j].row, self.tiles[i][j].value)
                tmp[j].append(new_tile)
        self.tiles = tmp

    def slide(self, direction, y_axis):
        if y_axis and not self.transposed:
            self.transpose()
        elif not y_axis and self.transposed:
            self.transpose()

        self.updated = False
        for i in range(Settings.rows):
            self.shift_amt = 0
            for j in range(Settings.rows):
                if direction == -1:
                    current_tile = self.tiles[i][j]
                else:
                    current_tile = self.tiles[i][Settings.rows - 1 - j]

                if current_tile.value == 0:
                    self.shift_amt += Settings.tile_scale
                else:
                    current_tile.new_value = 0
                    current_tile.shift += self.shift_amt * direction
                    current_tile.speed = int(current_tile.shift / Settings.tile_scale)
                    next_unoccupied_column = int(current_tile.col / Settings.tile_scale + current_tile.speed)
                    merged_tile_column = int(current_tile.col / Settings.tile_scale + current_tile.speed + direction)
                    self.check_merge(current_tile, direction, next_unoccupied_column, merged_tile_column)
                if current_tile.speed != 0:
                    self.moved = True

    def check_merge(self, tile, direction, next_unoccupied_column, merged_tile_column):
        if 0 <= merged_tile_column < Settings.rows:
            tile_to_merge = self.tiles[int(tile.row / Settings.tile_scale)][merged_tile_column]
            if tile.value == tile_to_merge.new_value and not tile_to_merge.double:
                tile.shift += direction * Settings.tile_scale
                tile.speed += direction
                self.shift_amt += Settings.tile_scale
                tile_to_merge.double = True
                tile_to_merge.new_value *= 2
                self.score += tile_to_merge.new_value
            else:
                self.tiles[int(tile.row / Settings.tile_scale)][next_unoccupied_column].new_value = tile.value
        else:
            self.tiles[int(tile.row / Settings.tile_scale)][next_unoccupied_column].new_value = tile.value

    def update(self):
        random_pool = []
        self.updated = True
        for i in range(Settings.rows):
            for j in range(Settings.rows):
                self.tiles[i][j].edit(i * Settings.tile_scale, j * Settings.tile_scale, 0, 0, self.tiles[i][j].new_value, 0, False)
                if self.tiles[i][j].value == 0:
                    random_pool.append((i, j))
        self.place_random_tile(random_pool)
        if len(random_pool) == 1:
            self.game_over = self.check_game_over()

    def place_random_tile(self, random_pool):
        self.moved = False
        random_tile = random.choice(random_pool)
        if random.random() < Settings.starting_two_probability:
            val = 2
        else:
            val = 4
        self.tiles[random_tile[0]][random_tile[1]].value = val

    def check_game_over(self):
        for i in range(Settings.rows):
            for j in range(Settings.rows):
                if i == Settings.rows - 1 and j == Settings.rows - 1:
                    return True
                if i != Settings.rows - 1:
                    if self.tiles[i][j].value == self.tiles[i + 1][j].value:
                        return False
                if j != Settings.rows - 1:
                    if self.tiles[i][j].value == self.tiles[i][j + 1].value:
                        return False

    def print_tiles(self):
        for i in self.tiles:
            for j in i:
                print(j.value, end= ' ')
            print()
        print()
