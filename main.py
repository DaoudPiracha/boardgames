"""
evaluates an instance of the game ConnectFour
"""

from connect import Connect
from connect import IncorrectColumnIndex, ColumnIsFull

if __name__ == '__main__':
    board = Connect(tokens_to_connect=4,
                    connect_board_shape=(6, 8),
                    connect_n_players=2)

    while not board.has_game_ended:

        board.render()
        print(f'Player {board.current_player}, it is your turn!')
        print(f'Please choose a column no. between 0 - {board.n_columns-1}')

        try:
            move = input()
            move = int(move)
            board.step(move=move)

        except ValueError:
            print("please enter an integer")
        except IncorrectColumnIndex:
            print('please enter a valid column no.')
        except ColumnIsFull:
            print('your selected column is full')