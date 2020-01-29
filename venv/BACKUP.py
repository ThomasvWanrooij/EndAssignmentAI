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

# Required for communication with Arduino
import pyfirmata
from pyfirmata import Arduino, util

# Set port
port = "COM5"
ard = pyfirmata.Arduino(port)

# Set button pins
b0 = ard.get_pin("d:2:i").pin_number  # Digital pin 2, Output
b1 = ard.get_pin("d:3:i").pin_number  # Digital pin 3, Output
b2 = ard.get_pin("d:4:i").pin_number  # Digital pin 4, Output
b3 = ard.get_pin("d:5:i").pin_number  # Digital pin 5, Output
b4 = ard.get_pin("d:6:i").pin_number  # Digital pin 6, Output
b5 = ard.get_pin("d:7:i").pin_number  # Digital pin 7, Output
b6 = ard.get_pin("d:8:i").pin_number  # Digital pin 8, Output

buttons = [b0, b1, b2, b3, b4, b5, b6]  # Load buttons into array for easy looping

n1 = ard.get_pin("d:9:p").pin_number  # Digital pin 9, Input

# Instance of Iterator reads and handles data from Arduino over the serial port,
# it keeps the boards pin values up to date
iterator = pyfirmata.util.Iterator(ard)
iterator.start()

# Global variables4
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

# Set to false at the start of the game, for sound selection
win = False
lose = False


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


def win_game(field, piece):
    # Check all negative slope diagonals for a win
    for r in range(3, count_row):
        for c in range(count_column - 3):
            if field[r][c] == piece and field[r - 1][c + 1] == piece and field[r - 2][c + 2] == piece and field[r - 3][
                c + 3] == piece:
                return True

    # Check all positive slope diagonals for a win
    for r in range(count_row - 3):
        for c in range(count_column - 3):
            if field[r][c] == piece and field[r + 1][c + 1] == piece and field[r + 2][c + 2] == piece and field[r + 3][
                c + 3] == piece:
                return True

    # Check all verticals for a win
    for r in range(count_row - 3):
        for c in range(count_column):
            if field[r][c] == piece and field[r + 1][c] == piece and field[r + 2][c] == piece and field[r + 3][
                c] == piece:
                return True

    # Check all horizontals for a win
    for r in range(count_row):
        for c in range(count_column - 3):
            if field[r][c] == piece and field[r][c + 1] == piece and field[r][c + 2] == piece and field[r][
                c + 3] == piece:
                return True


# Evaluation based on heuristics
def series_evaluation(series, piece):
    score = 0

    piece_opponent = piece_player
    if piece == piece_player:
        piece_opponent = piece_AI

    if series.count(piece) == 4:  # Four in a row
        score += 1000
    elif series.count(piece) == 3 and series.count(empty_space) == 1:  # Three in a row
        score += 5
    elif series.count(piece) == 2 and series.count(empty_space) == 2:  # Two in a row
        score += 2

    if series.count(piece_opponent) == 3 and series.count(empty_space) == 1:  # Opponent has three in a row
        score -= 100
    elif series.count(piece_opponent) == 2 and series.count(empty_space) == 2:  # Opponent has two in a row
        score -= 2
    return score


# Check all horizontal, vertical and diagonal possibilities for a win
def pos_score(field, piece):
    score = 0

    # Middle column score
    array_center = [int(i) for i in list(field[:, 3])]
    count_center = array_center.count(piece)
    score += count_center * 3

    # Vertical scores
    for c in range(count_column):
        array_column = [int(i) for i in list(field[:, c])]
        for r in range(count_row - 3):  # Range is set this way because top 3 rows can't connect four new discs
            series = array_column[r:r + length_series]
            score += series_evaluation(series, piece)

    # Horizontal scores
    for r in range(count_row):
        array_row = [int(i) for i in list(field[r, :])]
        for c in range(count_column - 3):  # Range is set this way because right 3 columns can't connect four new discs
            series = array_row[c:c + length_series]
            score += series_evaluation(series, piece)

    # Positive slope diagonal scores
    for r in range(count_row - 3):  # Set of four diagonal discs (positive slope) can only start in bottom left
        for c in range(count_column - 3):
            series = [field[r + i][c + i] for i in range(length_series)]
            score += series_evaluation(series, piece)

    # Negative slope diagonal scores
    for r in range(count_row - 3):  # Set of four diagonal discs (negative slope) can only start in bottom right
        for c in range(count_column - 3):
            series = [field[r + 3 - i][c + i] for i in range(length_series)]
            score += series_evaluation(series, piece)

    return score


def is_last_node(field):
    return win_game(field, piece_player) or win_game(field, piece_AI) or len(search_valid_loc(field)) == 0


def minimax(field, depth, alpha, beta, maximizing_player):
    valid_locs = search_valid_loc(field)
    is_last = is_last_node(field)

    if depth == 0 or is_last:  # Check if depth is 0, or if the game is over in current position

        if is_last:

            if win_game(field, piece_AI):
                return None, math.inf  # Infinitely high score if AI player wins
            elif win_game(field, player):
                return None, - math.inf  # Infinitely low score if player wins
            else:
                # No more possible moves
                return None, 0
        # If depth is 0
        else:
            return None, pos_score(field, piece_AI)

    if maximizing_player:   # Will find the highest evaluation that can be obtained from current game state
        value = - math.inf
        col = random.choice(valid_locs)  # Start at random
        for column in valid_locs:   # Loop through children of the current position
            row = next_free_row(field, column)
            copy_field = field.copy()
            piece_drop(copy_field, row, column, piece_AI)
            # Recursive function passing in the child, depth-1 and False puts the turn to the opponent. (who minimizes)
            score_new = minimax(copy_field, depth - 1, alpha, beta, False)[1]

            if score_new > value:  # If newly calculated score is an improvement, pick that
                value = score_new
                col = column
            alpha = max(alpha, value)  # α - β pruning

            if alpha >= beta:
                break
        return col, value

    else:   # Will find the lowest evaluation that can be obtained from current game state
        # If minimizing player
        value = math.inf
        col = random.choice(valid_locs)
        for column in valid_locs:
            row = next_free_row(field, column)
            copy_field = field.copy()
            piece_drop(copy_field, row, column, piece_player)
            # Recursive function passing in the child, depth-1 and True puts the turn to the player. (who maximizes)
            score_new = minimax(copy_field, depth - 1, alpha, beta, True)[1]

            if score_new < value:  # If newly calculated score is an improvement, pick that
                value = score_new
                col = column
            beta = min(beta, value)  # α - β pruning

            if beta <= alpha:
                break
        return col, value


def search_valid_loc(field):
    valid_locs = []
    for column in range(count_column):
        if location_valid(field, column):
            valid_locs.append(column)
    return valid_locs


# def next_best_move(field, piece):
#     valid_locs = search_valid_loc(field)
#     highest_score = -10000
#     highest_column = random.choice(valid_locs)
#     for column in valid_locs:
#         row = next_free_row(field, column)
#         current_field = field.copy()
#         piece_drop(current_field, row, column, piece)
#         score = pos_score(current_field, piece)
#
#         if score > highest_score:
#             highest_score = score
#             highest_column = column
#
#     return highest_column


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


def play_note():
    notes_click = [2.5, 0, 5, 0]  # Sequence of voltages for click
    notes_win = [5, 0, 5, 2.5, 0, 5, 0, 5, 0]  # Sequence of voltages for win (player)
    notes_lose = [5, 5, 5, 4, 4, 4, 2, 2, 2, 2, 0]  # Sequence of voltages for loss (player)
    noteDurations = [1 / 12]  # All notes have same duration, but this can be changed by adding more possible durations
    pauseBetweenNotes = noteDurations[0] * 1.30  # This value seemed to sound best

    if win:
        for i in notes_win:  # Pick from win sequence
            time.sleep(pauseBetweenNotes)
            ard.digital[n1].write(i)  # Write to Arduino pin 9
    elif lose:
        for i in notes_lose:  # Pick from loss sequence
            time.sleep(pauseBetweenNotes)
            ard.digital[n1].write(i)  # Write to Arduino pin 9
    else:
        for i in notes_click:  # Pick from click sequence
            time.sleep(pauseBetweenNotes)
            ard.digital[n1].write(i)  # Write to Arduino pin 9


# Check if digital pin is read FALSE (when pressed)
def check_pressed(pin_num):
    pressed = ard.digital[pin_num].read()

    if pressed == 0:
        play_note()  # Play default sound upon click

        # Return corresponding column value for the specific button (directly related to button)
        if pin_num == b0:
            return 0
        elif pin_num == b1:
            return 1
        elif pin_num == b2:
            return 2
        elif pin_num == b3:
            return 3
        elif pin_num == b4:
            return 4
        elif pin_num == b5:
            return 5
        elif pin_num == b6:
            return 6
    else:
        return None


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
