class Tile:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.shift = 0
        self.speed = 0
        self.double = False
        self.new_value = 0

    def update(self):
        if self.shift != 0:
            self.col += self.speed
            self.shift -= self.speed
            return True
        return False

    def edit(self, row, col, shift, speed, value, new_value, double):
        self.row = row
        self.col = col
        self.shift = shift
        self.speed = speed
        self.value = value
        self.new_value = new_value
        self.double = double
