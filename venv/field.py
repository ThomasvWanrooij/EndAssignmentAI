"""

Thomas van Wanrooij (s2153270) & Noa van der Klooster (s2174162)
Artificial Intelligence & Programming
Final Project: 4 in a row
2020-01-21

General structure of the base-game of Connect 4 is based on Keith Galli's example videos.

"""

import pygame
import sys
import math
import numpy
import random
import time

import pyfirmata
from pyfirmata import Arduino, util

# Global variables
count_row = 6
count_column = 7
length_series = 4

empty_space = 0
piece_player = 1
piece_AI = 2
player = 0
AI = 1

color_field = (150, 20, 142)
color_background = (104, 255, 23)
color_player1 = (13, 110, 255)
color_AI = (255, 13, 13)
color_win = (0, 0, 0)

def make_field():
    field = numpy.zeros((count_row, count_column))
    return field


def piece_drop(field, row, column, piece):
    field[row][column] = piece  # Fill board with the set piece


# Check if the top row of specific column is or is not filled
def location_valid(field, column):
    if column is not None:
        return field[count_row - 1][column] == 0  # Returns true if not full, returns false if column is filled all the way
    else:
        return False


# Check, for all rows, return the first case where the coordinate equals 0
def next_free_row(field, column):
    for r in range(count_row):
        if field[r][column] == 0:
            return r


# Flip over the board, so it matches the known game (stacking up from the bottom)
def print_field(field):
    # print(numpy.flip(field, 0))
    pass


def draw_field(field):
    for c in range(count_column):
        for r in range(count_row):
            pygame.draw.rect(screen, color_field,
                             (c * size_squares, r * size_squares + size_squares, size_squares, size_squares))
            pygame.draw.circle(screen, color_background, (
            int(c * size_squares + size_squares / 2), int(r * size_squares + size_squares + size_squares / 2)), radius)

    for c in range(count_column):
        for r in range(count_row):
            if field[r][c] == piece_player:
                pygame.draw.circle(screen, color_player1, (
                int(c * size_squares + size_squares / 2), height - int(r * size_squares + size_squares / 2)), radius)
            elif field[r][c] == piece_AI:
                pygame.draw.circle(screen, color_AI, (
                int(c * size_squares + size_squares / 2), height - int(r * size_squares + size_squares / 2)), radius)
    pygame.display.update()

field = make_field()
print_field(field)  # Call to the flipping function as print of the board
lost_game = False

pygame.init()

size_squares = 110
width = size_squares * count_column
height = size_squares * (count_row + 1)
size = (width, height)
radius = int(size_squares / 2 - 10)

screen = pygame.display.set_mode(size)
draw_field(field)
pygame.display.update()

font = pygame.font.SysFont("courier", 50)
move = random.randint(player, AI)  # Randomly select starting player
depth = 1  # Define the amount of branches the AI will look at. More depth is more difficult

while not lost_game:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

    # Input player
    if move == player:
        column: int = 0
        for x in buttons:  # Check all buttons
            time.sleep(0.001)  # A small delay, helps during initialization of Arduino reading
            column = check_pressed(x)  # value is stored in the column variable for further use

            if column is not None:  # Stop checking next buttons when a value for column has been found
                break

        if location_valid(field, column):
            row = next_free_row(field, column)
            piece_drop(field, row, column, piece_player)

            if win_game(field, piece_player):
                label = font.render("Winner: Player 1!", 1, color_win)

                win = True  # Set play tune for win situation
                play_note()  # Play tune

                screen.blit(label, (60, 10))
                lost_game = True

            move += 1
            move = move % 2  # Move alternates between 0 and 1
            print_field(field)
            draw_field(field)

    # Input AI
    if move == AI and not lost_game:
        column, minimax_score = minimax(field, depth, - math.inf, math.inf, True)

        if location_valid(field, column):
            row = next_free_row(field, column)
            piece_drop(field, row, column, piece_AI)

            if win_game(field, piece_AI):
                label = font.render("Winner: Player 2!", 1, color_win)

                lose = True  # Set play tune for loss situation
                play_note()  # Play tune

                screen.blit(label, (60, 10))
                lost_game = True

            print_field(field)
            draw_field(field)

            move += 1
            move = move % 2  # Move alternates between 0 and 1
