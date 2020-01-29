import pygame
import sys
import math
import numpy
import random
import time

# Required for communication with Arduino
import pyfirmata
from pyfirmata import Arduino, util

from board import Board
from game import Game

empty_space = 0
piece_player = 1
piece_AI = 2
player = 0
AI = 1
depth = 1


field_1 = Board(6, 7, piece_player, piece_AI)
game_1 = Game(field_1, row, column, piece)
ai = AI(field_1, depth, - math.inf, math.inf, True)
input = Input()
speaker = Sound()

field_1.make_field()
field_1.print_field()
lost_game = False

field_1.draw_field()
pygame.display.update()

font = font = pygame.font.SysFont("courier", 50)
move = random.randint(player, AI)  # Randomly select starting player
depth = 1  # Define the amount of branches the AI will look at. More depth is more difficult

while not lost_game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #Input player
    if move == player:
        column: int = 0
        for x in input.buttons: # Check all buttons
            input.time.sleep(0.001)  # A small delay, helps during initialization of Arduino reading
            column = input.check_pressed(x)  # value is stored in the column variable for further use

            if column is not None:  # Stop checking next buttons when a value for column has been found
                break

        if game_1.location_valid(field_1, column):
            row = game_1.next_free_row(field_1, column)
            game_1.piece_drop(field_1, row, column, piece_player)

            if game_1.win_game(field_1, piece_player):
                label = font.render("Winner: Player 1!", 1, game_1.color_win)

                speaker.set_tune(1)
                speaker.play_note()

                screen.blit(label, (60, 10))
                lost_game = True

            move += 1
            move = move % 2
            field_1.print_field()
            field_1.draw_field()

    if move == AI and not lost_game:
        column, minimax_score = ai.minimax(field_1, depth, - math.inf, True)

        if game_1.location_valid(field, column):
            row = game_1.next_free_row(field_1, column)
            game_1.piece_drop(field_1, row, column, piece_AI)

            if game_1.win_game(field_1, piece_AI):
                label = font.render("Winner: Player 2!", 1, game_1.color_win)

                speaker.set_tune(2)
                speaker.play_note()

                screen.blit(label, (60, 10))
                lost_game = True

            move += 1
            move = move % 2
            field_1.print_field()
            field_1.draw_field()

