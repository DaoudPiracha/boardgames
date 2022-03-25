"""
Implements the Connect game, which can be used to play ConnectFour
"""
from board_game import BoardGame

TOP_ROW_IDX = 0
EMPTY_CELL = 0


class Connect(BoardGame):
    """
    Implements the Connect game
    """
    def __init__(self,
                 tokens_to_connect=4,
                 connect_board_shape=(6, 6),
                 connect_n_players=2):

        super().__init__(
            n_players   = connect_n_players,
            board_shape = connect_board_shape
        )
        # make sure game is Valid
        has_enough_cells_for_sequence = (
                connect_board_shape[0] >= tokens_to_connect
                or connect_board_shape[1] >= tokens_to_connect
        )
        if not has_enough_cells_for_sequence:
            raise Exception("Board too Small for Connect Sequence")

        if tokens_to_connect < 4:
            raise Exception("Connect Sequence Too Small")

        self.tokens_to_connect = tokens_to_connect
        self.n_rows = self.board_shape[0]
        self.n_columns = self.board_shape[1]
        self.remaining_cells_in_column = [self.n_rows] * self.n_columns
        self.coordinates_of_last_token = None

    def reset(self):
        super().reset()
        self.remaining_cells_in_column = [self.n_rows] * self.n_columns

    def check_valid_input(self, move):

        if not 0 <= move < self.n_columns:
            raise IncorrectColumnIndex

        if self.remaining_cells_in_column[move] == 0:
            raise ColumnIsFull

    def update_board(self, chosen_column):
        """
        :param chosen_column: int column no. to choose column to drop coin
        :return:
        """
        self.check_valid_input(chosen_column)
        chosen_row = self.remaining_cells_in_column[chosen_column] - 1
        self.board[chosen_row][chosen_column] = self.current_player

        self.remaining_cells_in_column[chosen_column] -= 1
        self.coordinates_of_last_token = (chosen_row, chosen_column)

    def is_game_win(self):
        """
        evaluates row, column, left, right diagonal of last placed token
        to see if any contain winning sequence of tokens
        :return: True
        """
        if not self.coordinates_of_last_token:
            raise ValueError

        return any(
            [self._is_game_win_horizontal(),
             self._is_game_win_vertical(),
             self._is_game_win_left_diagonal(),
             self._is_game_win_right_diagonal()
             ]
        )

    def is_game_tie(self):
        """
        tie if no empty cells left
        :return:
        """
        if all(remaining_cells == 0 for remaining_cells in self.remaining_cells_in_column):
            return True

        return False

    def _is_game_win_horizontal(self):
        """
        checks cells to the left and right of last placed token
        to see if a winning sequence is found
        :return:
        """
        move_row, move_col = self.coordinates_of_last_token
        left_idx = move_col - self.tokens_to_connect + 1

        # move left to right
        for _ in range(self.tokens_to_connect):
            if 0 <= left_idx <= self.n_columns - self.tokens_to_connect:
                connected_tokens = 0
                for token_idx in range(self.tokens_to_connect):
                    current_token = self.board[move_row][left_idx+token_idx]
                    if  current_token == self.current_player:
                        connected_tokens += 1

                if connected_tokens == self.tokens_to_connect:
                    return True

            left_idx += 1
        return False

    def _is_game_win_vertical(self):
        """
        checks cells to above and below of last placed token
        to see if a winning sequence is found
        :return:
        """
        move_row, move_col = self.coordinates_of_last_token

        # move top down
        top_index = move_row - self.tokens_to_connect + 1
        for _ in range(self.tokens_to_connect):
            if 0 <= top_index <= self.n_rows - self.tokens_to_connect:
                connected_tokens = 0
                for token_idx in range(self.tokens_to_connect):
                    current_token = self.board[top_index+token_idx][move_col]
                    if current_token == self.current_player:
                        connected_tokens += 1

                if connected_tokens == self.tokens_to_connect:
                    return True
            top_index += 1
        return False

    def _is_game_win_left_diagonal(self):
        """
         checks cells to above and below in left diagonal containing last placed token
         to see if a winning sequence is found
         :return:
         """

        move_row, move_col = self.coordinates_of_last_token
        top_left_row_idx = move_row - self.tokens_to_connect + 1
        top_left_col_idx = move_col - self.tokens_to_connect + 1

        # move top left to bottom right
        for _ in range(self.tokens_to_connect):
            if (0 <= top_left_row_idx < self.n_rows
            and 0 <= top_left_col_idx < self.n_columns):
                connected_tokens = 0

                for token_idx in range(self.tokens_to_connect):
                    if (0 <= top_left_row_idx + token_idx < self.n_rows
                    and 0 <= top_left_col_idx + token_idx < self.n_columns):
                        current_token = self.board[top_left_row_idx + token_idx][top_left_col_idx + token_idx]
                        if current_token == self.current_player:
                            connected_tokens += 1

                if connected_tokens == self.tokens_to_connect:
                    return True

            # try next sequence on left diagonal
            top_left_row_idx += 1
            top_left_col_idx += 1
        return False

    def _is_game_win_right_diagonal(self):
        """
       checks cells to above and below in right diagonal containing last placed token
       to see if a winning sequence is found
       :return:
       """

        move_row, move_col = self.coordinates_of_last_token
        top_right_row_idx = move_row - self.tokens_to_connect + 1
        top_right_col_idx = move_col + self.tokens_to_connect - 1

        # move top right to bottom left
        for _ in range(self.tokens_to_connect):
            if (0  <= top_right_row_idx < self.n_rows
            and 0  <= top_right_col_idx < self.n_columns):
                connected_tokens = 0

                for token_idx in range(self.tokens_to_connect):
                    if (0<= top_right_row_idx + token_idx < self.n_rows
                    and 0<= top_right_col_idx - token_idx < self.n_columns):
                        current_token = self.board[top_right_row_idx + token_idx][top_right_col_idx - token_idx]
                        if current_token == self.current_player:
                            connected_tokens += 1

                if connected_tokens == self.tokens_to_connect:
                    return True

            # try next sequence on right diagonal
            top_right_row_idx += 1
            top_right_col_idx -= 1
        return False


class IncorrectColumnIndex(Exception):
    pass

class ColumnIsFull(Exception):
    pass
