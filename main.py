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


class Game:
    def __init__(self):
        self.rotate = False
        self.flip = False
        self.speed = -10
        self.rows = 4
        self.fps = 60
        self.done = False
        self.clock = pygame.time.Clock()
        self.overlay = Board()
        self.dir = (0, 0)
        self.tile_factor = 100
        self.board = [[[j * 100, i * 100, 0, 0] for i in range(self.rows)] for j in range(self.rows)]
        self.board[3][3][3] = 16
        self.board[3][1][3] = 8
        self.board[1][2][3] = 4

    def rotate_matrix(self):
        for i in range(self.rows):
            self.board[i][:] = self.board[i][::-1]

    def rows_to_cols(self):
        tmp = []
        for i in range(self.rows):
            tmp.append([row[i] for row in self.board])
        self.board = tmp


    def game_loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if self.rotate:
                        self.rotate_matrix()
                        self.rotate = False
                    if self.flip:
                        self.rows_to_cols()
                        self.flip = False

                    if event.key == pygame.K_RIGHT:
                        self.rotate_matrix()
                        self.rotate = True
                        self.dir = (1, 0)
                    elif event.key == pygame.K_LEFT:
                        self.dir = (-1, 0)
                    elif event.key == pygame.K_UP:
                        self.rows_to_cols()
                        self.dir = (0, -1)
                        self.flip = True
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)


    def update(self):
        for i in range(self.rows):
            for j in range(self.rows):
                self.board[i][j][0] = i * 100
                self.board[i][j][1] = j * 100
        for i in range(self.rows):
            self.board[i][:] = [value for value in self.board[i] if value[3] != 0]
            for j in range(len(self.board[i])):
                if j != self.board[i][j][1] / self.tile_factor:
                    self.board[i][j][2] = self.speed * ((self.board[i][j][1] / self.tile_factor) - j)
            for j in range(self.rows - len(self.board[i])):
                self.board[i].append([i * 100, len(self.board[i]) * 100, 0, 0])

    def move(self):
        for i in range(self.rows):
            for j in range(self.rows):
                if self.board[i][j][1] / self.tile_factor > j:
                    self.board[i][j][1] += self.board[i][j][2]
                elif self.board[i][j][1] / self.tile_factor < j:
                    self.board[i][j][1] = j * self.tile_factor
                    self.board[i][j][2] = 0



    def draw(self):
        game_display.fill(Colors.white)
        self.overlay.draw_box()
        self.overlay.draw_lines()
        self.move()
        if self.dir[0] != 0 or self.dir[1] != 0:
            self.update()
            self.dir = (0, 0)
        for i in range(self.rows):
            for j in range(self.rows):
                if self.board[i][j][3] != 0:
                    x = self.board[i][j][0] / 100
                    y = self.board[i][j][1] / 100
                    value = self.board[i][j][3]
                    if self.rotate:
                        self.overlay.draw_tile(x, self.rows - 1 - y, value)
                    elif self.flip:
                        self.overlay.draw_tile(y, x, value)
                    else:
                        self.overlay.draw_tile(x, y, value)

    def terminate(self):
        pygame.quit()
        quit()

def main():
    game = Game()
    game.game_loop()

if __name__ == '__main__':
    main()