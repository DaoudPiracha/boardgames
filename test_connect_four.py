from unittest import TestCase
from connect import Connect


class TestSmallBoard(TestCase):
    def setUp(self):
        self.small_game = Connect(connect_board_shape=(4, 4))
        self.large_game = Connect(connect_board_shape=(6, 6))
        self.small_game_rectangular = Connect(connect_board_shape=(4, 6))

        self.small_game.reset()

    def test_initial_board_size(self):
        self.assertEqual(len(self.small_game.board), 4)
        self.assertEqual(len(self.small_game.board[0]), 4)

    def test_initial_board_empty(self):
        empty_small_board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.small_game.board, empty_small_board)

    def test_first_move_placed(self):
        one_move_small_board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 1, 0, 0]
        ]
        self.small_game.update_board(chosen_column=1)
        self.assertEqual(self.small_game.board, one_move_small_board)


    def test_reset(self):
        test_board =  [[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]

        self.small_game.step(0)
        self.small_game.reset()
        self.assertEqual(self.small_game.board, test_board)

    def test_win_vertical_1(self):

        self.small_game.reset()

        for _ in range(3):
            self.small_game.step(move=0)
            self.small_game.step(move=1)

        self.small_game.step(move=0)

        self.assertEqual(self.small_game.has_game_ended, True)
        self.assertEqual(self.small_game.is_game_win(), True)
        self.assertEqual(self.small_game.current_player, 1)

    def test_moves_after_win_not_considered(self):

        self.small_game.reset()

        for _ in range(4):
            self.small_game.step(move=0)
            self.small_game.step(move=1)

        self.assertEqual(self.small_game.has_game_ended, True)
        self.assertEqual(self.small_game.is_game_win(), True)
        self.assertEqual(self.small_game.current_player, 1)

    def test_win_vertical_2(self):
        self.large_game.reset()

        """
        tests the configuration:
               [[1, 0, 0, 0, 0, 0],
                [1, 2, 0, 0, 0, 0],
                [1, 2, 0, 0, 0, 0],
                [1, 2, 0, 0, 0, 0],
                [2, 1, 0, 0, 0, 0],
                [2, 1, 0, 0, 0, 0]]
        """

        # setup
        for _ in range(2):
            self.large_game.step(move=1)
            self.large_game.step(move=0)

        for _ in range(3):
            self.large_game.step(move=0)
            self.large_game.step(move=1)

        # winning move
        self.large_game.step(move=0)

        self.assertEqual(self.large_game.is_game_win(), True)
        self.assertEqual(self.small_game.is_game_tie(), False)


    def test_tie(self):
        self.small_game.reset()

        """
        tests the configuration:
                   [[2, 1, 2, 1],
                    [1, 2, 1, 2],
                    [1, 2, 1, 2],
                    [1, 2, 1, 2]]
        """

        for _ in range(3):
            self.small_game.step(0)
            self.small_game.step(1)
        self.small_game.step(1)
        self.small_game.step(0)

        for _ in range(3):
            self.small_game.step(2)
            self.small_game.step(3)
        self.small_game.step(3)
        self.small_game.step(2)

        self.assertEqual(self.small_game.is_game_tie(), True)
        self.assertEqual(self.small_game.is_game_win(), False)
        self.assertEqual(self.small_game.has_game_ended, True)

    def test_is_game_win_horizontal(self):
        self.small_game.reset()

        for idx in range(4):
            self.small_game.step(idx)
            self.small_game.step(idx)

        self.assertEqual(self.small_game._is_game_win_horizontal(), True)

    def test_is_game_win_vertical(self):
        self.small_game.reset()

        for idx in range(4):
            self.small_game.step(0)
            self.small_game.step(1)

        self.assertEqual(self.small_game._is_game_win_vertical(), True)

    def test_is_game_win_right_diagonal(self):
        self.small_game.reset()

        self.small_game.step(0)
        self.small_game.step(1)
        self.small_game.step(1)
        self.small_game.step(3)
        self.small_game.step(2)
        self.small_game.step(2)
        self.small_game.step(2)
        self.small_game.step(3)
        self.small_game.step(3)
        self.small_game.step(0)
        self.small_game.step(3)

        self.assertEqual(self.small_game._is_game_win_right_diagonal(), True)

    def test_is_game_win_right_diagonal_rectangular_board(self):
        self.small_game_rectangular.reset()

        self.small_game_rectangular.step(0)
        self.small_game_rectangular.step(1)
        self.small_game_rectangular.step(1)
        self.small_game_rectangular.step(3)
        self.small_game_rectangular.step(2)
        self.small_game_rectangular.step(2)
        self.small_game_rectangular.step(2)
        self.small_game_rectangular.step(3)
        self.small_game_rectangular.step(3)
        self.small_game_rectangular.step(0)
        self.small_game_rectangular.step(3)

        self.assertEqual(self.small_game_rectangular._is_game_win_right_diagonal(), True)


    # todo: test on larger game
    def test_is_game_win_left_diagonal(self):
        self.small_game.reset()

        self.small_game.step(3)
        self.small_game.step(2)
        self.small_game.step(2)
        self.small_game.step(0)
        self.small_game.step(1)
        self.small_game.step(1)
        self.small_game.step(1)
        self.small_game.step(0)
        self.small_game.step(0)
        self.small_game.step(3)
        self.small_game.step(0)

        self.assertEqual(self.small_game._is_game_win_left_diagonal(), True)


