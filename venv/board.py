class Board:

    import numpy
    import pygame
    color_field = (150, 20, 142)
    color_background = (104, 255, 23)
    color_player1 = (13, 110, 255)
    color_AI = (255, 13, 13)
    color_win = (0, 0, 0)

    def __init__(self, count_row, count_column, piece_player, piece_AI):
        self.count_row = count_row
        self.count_column = count_column

        self.piece_player = piece_player
        self.piece_AI = piece_AI

        self.field = Board.numpy.zeros((self.count_row, self.count_column))

        self.size_squares = 110
        self.width = self.size_squares * self.count_column
        self.height = self.size_squares * (self.count_row + 1)
        self.size = (self.width, self.height)
        self.radius = int(self.size_squares / 2 - 10)
        self.screen = Board.pygame.display.set_mode(self.size)

    def make_field(self):
        return self.field

    def print_field(self):
        print(Board.numpy.flip(self.field, 0))

    def draw_field(self):

        for c in range(self.count_column):
            for r in range(self.count_row):
                Board.pygame.draw.rect(self.screen, Board.color_field,
                                 (c * self.size_squares, r * self.size_squares + self.size_squares, self.size_squares, self.size_squares))
                Board.pygame.draw.circle(self.screen, Board.color_background, (
                    int(c * self.size_squares + self.size_squares / 2), int(r * self.size_squares + self.size_squares + self.size_squares / 2)), self.radius)

        for c in range(self.count_column):
            for r in range(self.count_row):
                if self.field[r][c] == self.piece_player:
                    Board.pygame.draw.circle(self.screen, Board.color_player1, (
                        int(c * self.size_squares + self.size_squares / 2), self.height - int(r * self.size_squares + self.size_squares / 2)), self.radius)
                elif self.field[r][c] == self.piece_AI:
                    Board.pygame.draw.circle(self.screen, Board.color_AI, (
                        int(c * self.size_squares + self.size_squares / 2), self.height - int(r * self.size_squares + self.size_squares / 2)), self.radius)
        Board.pygame.display.update()