#  This class handles the algorithms that run the game


class Game(field):

    def __init__(self):
        pass

    def win_game(self, field, piece):
        # Check all negative slope diagonals for a win
        for r in range(3, count_row):
            for c in range(count_column - 3):
                if self.field[r][c] == self.piece and self.field[r - 1][c + 1] == self.piece and \
                        self.field[r - 2][c + 2] == self.piece and self.field[r - 3][c + 3] == self.piece:
                    return True

        # Check all positive slope diagonals for a win
        for r in range(count_row - 3):
            for c in range(count_column - 3):
                if self.field[r][c] == self.piece and self.field[r + 1][c + 1] == self.piece and \
                        self.field[r + 2][c + 2] == self.piece and self.field[r + 3][c + 3] == self.piece:
                    return True

        # Check all verticals for a win
        for r in range(count_row - 3):
            for c in range(count_column):
                if self.field[r][c] == self.piece and self.field[r + 1][c] == self.piece and self.field[r + 2][c] == \
                        self.piece and self.field[r + 3][c] == self.piece:
                    return True

        # Check all horizontals for a win
        for r in range(count_row):
            for c in range(count_column - 3):
                if field[r][c] == self.piece and self.field[r][c + 1] == self.piece and self.field[r][c + 2] == \
                        self.piece and self.field[r][c + 3] == self.piece:
                    return True

    # Evaluation based on heuristics
    def series_evaluation(self, series, piece):
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
