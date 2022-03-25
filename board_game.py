"""Base class for 2-D multiplayer turn based board games
"""
from itertools import cycle
from abc import ABC, abstractmethod


class BoardGame(ABC):
    def __init__(self, n_players=2, board_shape=None):
        """
        :param n_players: int number of players
        :param board_shape: tuple containing board dimensions
        """
        self.n_players = n_players
        self.has_game_ended = False
        self.board_shape = board_shape
        self.board = self._create_empty_board(self.board_shape)
        self.players = cycle(range(1, n_players+1))
        self.current_player = next(self.players)

    def _create_empty_board(self, board_shape):
        if board_shape:
            rows, columns = board_shape
            _grid = [[0 for _ in range(columns)] for _ in range(rows)]
            return _grid

    def update_game_state(self):

        if self.is_game_tie():
            print("We have a tie!")
            self.has_game_ended = True
            self.render()

        if self.is_game_win():
            print(f'We have a winner! Congratulations Player {self.current_player}')
            self.has_game_ended = True
            self.render()

        if not self.has_game_ended:
            self.current_player = next(self.players)

    def step(self, move):
        """
        takes player input and computes next step for game
        :return: updated game state
        """
        if not self.has_game_ended:
            self.update_board(move)
            self.update_game_state()


    def render(self):
        if self.board:
            for row in self.board:
                print(row)

    def reset(self):
        self.board = self._create_empty_board(self.board_shape)
        self.players = cycle(range(1, self.n_players + 1))
        self.current_player = next(self.players)
        self.has_game_ended = False

    @abstractmethod
    def update_board(self, move):
        pass

    @abstractmethod
    def is_game_tie(self) -> bool:
        pass

    @abstractmethod
    def is_game_win(self) -> bool:
        pass
