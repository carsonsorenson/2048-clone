import pygame

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
    def __init__(self, row, col, num):
        self.row = row
        self.col = col
        self.num = num
        self.mult = 0


class Game:
    def __init__(self):
        self.rows = 4
        self.fps = 60
        self.done = False
        self.clock = pygame.time.Clock()
        self.overlay = Board()
        self.dir = (0, 0)
        self.board = []
        self.tile_factor = 100
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.rows):
                tile = Tile(j * 100, i * 100, 0)
                self.board[i].append(tile)
        self.board[3][1] = Tile(300, 100, 64)
        self.board[3][3] = Tile(300, 300, 8)
        self.board[0][2] = Tile(0, 200, 8)

    def game_loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.dir = (1, 0)
                    elif event.key == pygame.K_LEFT:
                        self.dir = (-1, 0)
            if self.dir[0] != 0 or self.dir[1] != 0:
                self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)


    def update(self):
        if self.dir[0] < 0:
            for i in range(self.rows):
                self.board[i][:] = [tile for tile in self.board[i] if tile.num != 0]
                for j in range(len(self.board[i])):
                    tile = self.board[i][j]
                    if tile.mult == 0:
                        tile.mult = (tile.col / self.tile_factor) - j
                    if j < tile.col / self.tile_factor:
                        tile.col += -1 * tile.mult
                    else:
                        tile.col = j * self.tile_factor
        elif self.dir[0] > 0:
            for i in range(self.rows):
                for j in range(self.rows - 1, -1, -1):
                    if self.board[i][j].num == 0:
                        tile = self.board[i].pop(j)
                        self.board




    def draw(self):
        game_display.fill(Colors.white)
        if self.dir[0] != 0 or self.dir[1] != 0:
            self.update()
        self.overlay.draw_box()
        self.overlay.draw_lines()
        for i in self.board:
            for tile in i:
                if tile.num != 0:
                    self.overlay.draw_tile(tile.row / self.tile_factor, tile.col / self.tile_factor, tile.num)

    def terminate(self):
        pygame.quit()
        quit()

def main():
    game = Game()
    game.game_loop()

if __name__ == '__main__':
    main()