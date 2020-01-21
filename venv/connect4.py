import pygame
import sys
import math
import numpy
import random

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
    field[row][column] = piece


def location_valid(field, column):
    return field[count_row - 1][column] == 0


def next_free_row(field, column):
    for r in range(count_row):
        if field[r][column] == 0:
            return r


def print_field(field):
    print(numpy.flip(field, 0))


def win_game(field, piece):
    # Check all negative slope diagonals for a win
    for r in range(3, count_row):
        for c in range(count_column - 3):
            if field[r][c] == piece and field[r - 1][c + 1] == piece and field[r - 2][c + 2] == piece and field[r - 3][c + 3] == piece:
                return True

    # Check all positive slope diagonals for a win
    for r in range(count_row - 3):
        for c in range(count_column - 3):
            if field[r][c] == piece and field[r + 1][c + 1] == piece and field[r + 2][c + 2] == piece and field[r + 3][c + 3] == piece:
                return True

    # Check all verticals for a win
    for r in range(count_row - 3):
        for c in range(count_column):
            if field[r][c] == piece and field[r + 1][c] == piece and field[r + 2][c] == piece and field[r + 3][c] == piece:
                return True

    # Check all horizontals for a win
    for r in range(count_row):
        for c in range(count_column - 3):
            if field[r][c] == piece and field[r][c + 1] == piece and field[r][c + 2] == piece and field[r][c + 3] == piece:
                return True


def series_evaluation(series, piece):
    score = 0

    piece_opponent = piece_player
    if piece == piece_player:
        piece_opponent = piece_AI

    if series.count(piece) == 4:
        score += 1000
    elif series.count(piece) == 3 and series.count(empty_space) == 1:
        score += 5
    elif series.count(piece) == 2 and series.count(empty_space) == 2:
        score += 2

    if series.count(piece_opponent) == 3 and series.count(empty_space) == 1:
        score -= 100
    #elif series.count(piece_opponent) == 2 and series.count(empty_space) == 2:
    #    score -= 2
    return score


def pos_score(field, piece):
    score = 0

    # Middle column score
    array_center = [int(i) for i in list(field[:, 3])]
    count_center = array_center.count(piece)
    score += count_center * 3

    # Negative slope diagonal scores
    for r in range(count_row - 3):
        for c in range(count_column - 3):
            series = [field[r + 3 - i][c + i] for i in range(length_series)]
            score += series_evaluation(series, piece)

    # Positive slope diagonal scores
    for r in range(count_row - 3):
        for c in range(count_column - 3):
            series = [field[r + i][c + i] for i in range(length_series)]
            score += series_evaluation(series, piece)

    # Vertical scores
    for c in range(count_column):
        array_column = [int(i) for i in list(field[:, c])]
        for r in range(count_row - 3):
            series = array_column[r:r + length_series]
            score += series_evaluation(series, piece)

    # Horizontal scores
    for r in range(count_row):
        array_row = [int(i) for i in list(field[r, :])]
        for c in range(count_column - 3):
            series = array_row[c:c + length_series]
            score += series_evaluation(series, piece)

    return score


def is_last_node(field):
    return win_game(field, piece_player) or win_game(field, piece_AI) or len(search_valid_loc(field)) == 0


def minimax(field, depth, alpha, beta, maximizing_player):
    valid_locs = search_valid_loc(field)
    is_last = is_last_node(field)
    if depth == 0 or is_last:
        if is_last:
            if win_game(field, piece_AI):
                return (None, 10000000000)
            elif win_game(field, player):
                return (None, -10000000000)
            else:
                # No more possible moves
                return (None, 0)
        # If depth is 0
        else:
            return (None, pos_score(field, piece_AI))

    if maximizing_player:
        value = - math.inf
        col = random.choice(valid_locs)
        for column in valid_locs:
            row = next_free_row(field, column)
            copy_field = field.copy()
            piece_drop(copy_field, row, column, piece_AI)
            score_new = minimax(copy_field, depth - 1, alpha, beta, False)[1]
            if score_new > value:
                value = score_new
                col = column
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return col, value

    else:
        value = math.inf
        col = random.choice(valid_locs)
        for column in valid_locs:
            row = next_free_row(field, column)
            copy_field = field.copy()
            piece_drop(copy_field, row, column, piece_player)
            score_new = minimax(copy_field, depth - 1, alpha, beta, True)[1]
            if score_new < value:
                value = score_new
                col = column
            beta = min(alpha, value)
            if beta <= alpha:
                break
        return col, value


def search_valid_loc(field):
    valid_locs = []
    for column in range(count_column):
        if location_valid(field, column):
            valid_locs.append(column)
    return valid_locs


def next_best_move(field, piece):
    valid_locs = search_valid_loc(field)
    highest_score = -10000
    highest_column = random.choice(valid_locs)
    for column in valid_locs:
        row = next_free_row(field, column)
        current_field = field.copy()
        piece_drop(current_field, row, column, piece)
        score = pos_score(current_field, piece)
        if score > highest_score:
            highest_score = score
            highest_column = column

    return highest_column


def draw_field(field):
    for c in range(count_column):
        for r in range(count_row):
            pygame.draw.rect(screen, color_field, (c * size_squares, r * size_squares + size_squares, size_squares, size_squares))
            pygame.draw.circle(screen, color_background, (int(c * size_squares + size_squares / 2), int(r * size_squares + size_squares + size_squares / 2)), radius)
    for c in range(count_column):
        for r in range(count_row):
            if field[r][c] == piece_player:
                pygame.draw.circle(screen, color_player1, (int(c * size_squares + size_squares / 2), height - int(r * size_squares + size_squares / 2)), radius)
            elif field[r][c] == piece_AI:
                pygame.draw.circle(screen, color_AI, (int(c * size_squares + size_squares / 2), height - int(r * size_squares + size_squares / 2)), radius)
    pygame.display.update()


field = make_field()
print_field(field)
lost_game = False

pygame.init()

size_squares = 90
width = size_squares * count_column
height = size_squares * (count_row + 1)
size = (width, height)
radius = int(size_squares / 2 - 5)

screen = pygame.display.set_mode(size)
draw_field(field)
pygame.display.update()

font = pygame.font.SysFont("courier", 50)
move = player #random.randint(player, AI)
depth = 5

while not lost_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, color_background, (0, 0, width, size_squares))
            x_pos = event.pos[0]
            if move == player:
                pygame.draw.circle(screen, color_player1, (x_pos, int(size_squares / 2)), radius)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, color_background, (0, 0, width, size_squares))

            # Input player
            if move == player:
                x_pos = event.pos[0]
                column = int(math.floor(x_pos / size_squares))
                if location_valid(field, column):
                    row = next_free_row(field, column)
                    piece_drop(field, row, column, piece_player)
                    if win_game(field, piece_player):
                        label = font.render("Winner: Player 1!", 1, color_win)
                        screen.blit(label, (60, 10))
                        lost_game = True

                    move += 1
                    move = move % 2
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
                screen.blit(label, (60, 10))
                lost_game = True

            print_field(field)
            draw_field(field)

            move += 1
            move = move % 2

