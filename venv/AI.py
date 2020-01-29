"""
the AI is a sub-class of the game class, for it to inherit variables for calculations.
Also, in this way, multiple AI's could be run in the same game.
"""


class AI:

    from game import Game

    def __init__(self, field, depth, alpha, beta, maximizing_player):
        self.field = field
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
        self.maximizing_player = maximizing_player

        self.valid_locs = Game.search_valid_loc(field)
        self.is_last = Game.is_last_node(field)

    def minimax(self):
        if depth == 0 or is_last:  # Check if depth is 0, or if the game is over in current position

            if self.is_last:

                if Game.win_game(field, piece_AI):
                    return None, math.inf  # Infinitely high score if AI player wins
                elif Game.win_game(field, player):
                    return None, - math.inf  # Infinitely low score if player wins
                else:
                    # No more possible moves
                    return None, 0
            # If depth is 0
            else:
                return None, pos_score(field, piece_AI)

        if self.maximizing_player:  # Will find the highest evaluation that can be obtained from current game state
            value = - math.inf
            col = random.choice(self.valid_locs)  # Start at random
            for column in self.valid_locs:  # Loop through children of the current position
                row = Game.next_free_row(self.field, column)
                copy_field = self.field.copy()
                piece_drop(copy_field, row, column, piece_AI)
                # Recursive function passing in the child, depth-1 and False puts the turn to the opponent. (who minimizes)
                score_new = minimax(copy_field, self.depth - 1, self.alpha, self.beta, False)[1]

                if score_new > value:  # If newly calculated score is an improvement, pick that
                    value = score_new
                    col = column
                self.alpha = max(self.alpha, value)  # α - β pruning

                if alpha >= beta:
                    break
            return col, value

        else:  # Will find the lowest evaluation that can be obtained from current game state
            # If minimizing player
            value = math.inf
            col = random.choice(valid_locs)
            for column in self.valid_locs:
                row = Game.next_free_row(self.field, column)
                copy_field = self.field.copy()
                piece_drop(copy_field, row, column, piece_player)
                # Recursive function passing in the child, depth-1 and True puts the turn to the player. (who maximizes)
                score_new = minimax(copy_field, self.depth - 1, self.alpha, self.beta, True)[1]

                if score_new < value:  # If newly calculated score is an improvement, pick that
                    value = score_new
                    col = column
                self.beta = min(self.beta, value)  # α - β pruning

                if beta <= alpha:
                    break
            return col, value
















































    #
    # def minimax(field, depth, alpha, beta, maximizing_player):
    #     valid_locs = search_valid_loc(field)
    #     is_last = is_last_node(field)
    #
    #     if depth == 0 or is_last:
    #
    #         if is_last:
    #
    #             if win_game(field, piece_AI):
    #                 return None, math.inf  # Infinitely high score if AI player wins
    #             elif win_game(field, player):
    #                 return None, - math.inf  # Infinitely low score if player wins
    #             else:
    #                 # No more possible moves
    #                 return None, 0
    #         # If depth is 0
    #         else:
    #             return None, pos_score(field, piece_AI)
    #
    #     if maximizing_player:
    #         value = - math.inf
    #         col = random.choice(valid_locs)  # Start at random
    #         for column in valid_locs:
    #             row = next_free_row(field, column)
    #             copy_field = field.copy()
    #             piece_drop(copy_field, row, column, piece_AI)
    #             score_new = minimax(copy_field, depth - 1, alpha, beta, False)[1]  # Recursive algorithm
    #
    #             if score_new > value:  # If newly calculated score is an improvement, pick that
    #                 value = score_new
    #                 col = column
    #             alpha = max(alpha, value)  # α - β pruning
    #
    #             if alpha >= beta:
    #                 break
    #         return col, value
    #
    #     else:
    #         # If minimizing player
    #         value = math.inf
    #         col = random.choice(valid_locs)
    #         for column in valid_locs:
    #             row = next_free_row(field, column)
    #             copy_field = field.copy()
    #             piece_drop(copy_field, row, column, piece_player)
    #             score_new = minimax(copy_field, depth - 1, alpha, beta, True)[1]  # Recursive algorithm
    #
    #             if score_new < value:  # If newly calculated score is an improvement, pick that
    #                 value = score_new
    #                 col = column
    #             beta = min(beta, value)  # α - β pruning
    #
    #             if beta <= alpha:
    #                 break
    #         return col, value
