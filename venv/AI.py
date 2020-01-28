"""
the AI is a sub-class of the game class, for it to inherit variables for calculations.
Also, in this way, multiple AI's could be run in the same game.
"""


class AI(game):

    def __init__(self):
        pass

    def minimax(field, depth, alpha, beta, maximizing_player):
        valid_locs = search_valid_loc(field)
        is_last = is_last_node(field)

        if depth == 0 or is_last:

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

        if maximizing_player:
            value = - math.inf
            col = random.choice(valid_locs)  # Start at random
            for column in valid_locs:
                row = next_free_row(field, column)
                copy_field = field.copy()
                piece_drop(copy_field, row, column, piece_AI)
                score_new = minimax(copy_field, depth - 1, alpha, beta, False)[1]  # Recursive algorithm

                if score_new > value:  # If newly calculated score is an improvement, pick that
                    value = score_new
                    col = column
                alpha = max(alpha, value)  # α - β pruning

                if alpha >= beta:
                    break
            return col, value

        else:
            # If minimizing player
            value = math.inf
            col = random.choice(valid_locs)
            for column in valid_locs:
                row = next_free_row(field, column)
                copy_field = field.copy()
                piece_drop(copy_field, row, column, piece_player)
                score_new = minimax(copy_field, depth - 1, alpha, beta, True)[1]  # Recursive algorithm

                if score_new < value:  # If newly calculated score is an improvement, pick that
                    value = score_new
                    col = column
                beta = min(beta, value)  # α - β pruning

                if beta <= alpha:
                    break
            return col, value
