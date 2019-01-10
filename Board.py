import pygame
from Symbol import Symbol
from Color import Color


class Board:
    # set initial symbol
    symbol = "x"
    # This sets the WIDTH and HEIGHT of each grid location
    GRID_WIDTH = 80
    GRID_HEIGHT = 80
    # This sets the margin between each cell
    GRID_MARGIN = 5
    board_multiplier = 3
    streak_win_condition = 3
    current_player = 'player'

    def __init__(self, screen):
        self.grid = [[""] * self.board_multiplier for n in range(self.board_multiplier)]
        self.grid_position = [[""] * self.board_multiplier for m in range(self.board_multiplier)]
        # Draw the grid
        for row in range(self.board_multiplier):
            for column in range(self.board_multiplier):
                pygame.draw.rect(
                    screen,
                    Color.WHITE,
                    [
                        (self.GRID_MARGIN + self.GRID_WIDTH) * column
                        + self.GRID_MARGIN,
                        (self.GRID_MARGIN + self.GRID_HEIGHT) * row + self.GRID_MARGIN,
                        self.GRID_WIDTH,
                        self.GRID_HEIGHT,
                    ],
                )
                self.grid_position[row][column] = [
                    ((self.GRID_MARGIN + self.GRID_WIDTH) * column + self.GRID_MARGIN),
                    ((self.GRID_MARGIN + self.GRID_HEIGHT) * row + self.GRID_MARGIN),
                ]

    def evaluate(self, state):
        """
        Function to heuristic evaluation of state.
        :param state: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        if self.wins(state, 'o'):
            score = +1
        elif self.wins(state, 'x'):
            score = -1
        else:
            score = 0

        return score

    def wins(self, state, player):
        """
        This function tests if a specific player wins. Possibilities:
        * Three rows    [X X X] or [O O O]
        * Three cols    [X X X] or [O O O]
        * Two diagonals [X X X] or [O O O]
        :param state: the state of the current board
        :param player: a human or a computer
        :return: True if the player wins
        """
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    def game_over(self, state):
        """
        This function test if the human or computer wins
        :param state: the state of the current board
        :return: True if the human or computer wins
        """
        return self.wins(state, 'o') or self.wins(state, 'x')

    # Check the win condition
    def check_game_won(self, row, column, symbol):
        # Checking column
        for i in range(self.streak_win_condition):
            if self.grid[row][i] != symbol:
                break
            if i == 2:
                print(symbol + ' wins!')
                return symbol

        # Checking rows
        for i in range(self.streak_win_condition):
            if self.grid[i][column] != symbol:
                break
            if i == 2:
                print(symbol + ' wins!')
                return symbol

        # Checking diagonal
        if row == column:
            for i in range(self.streak_win_condition):
                if self.grid[i][i] != symbol:
                    break
                if i == 2:
                    print(symbol + ' wins!')
                    return symbol

        # Checking anti-diagonal
        if row + column == 2:
            for i in range(self.streak_win_condition):
                if self.grid[i][2 - i] != symbol:
                    break
                if i == 2:
                    print(symbol + ' wins!')
                    return symbol

        return None

    def is_full(self):
        for i in range(self.board_multiplier):
            for j in range(self.board_multiplier):
                if self.grid[i][j] == '':
                    return False
        return True

    def grid_is_empty(self, row, column):
        return bool(self.grid[row][column] == '')

    def get_grid(self):
        return self.grid

    def get_empty_grid_cell(self):
        cells = []

        for x in range(self.board_multiplier):
            for y in range(self.board_multiplier):
                if self.grid[x][y] == '':
                    cells.append([x, y])

        return cells

    def set_grid(self, row, column, screen):
        if self.grid_is_empty(row, column):
            # save symbol that is used to be paint.
            symbol = self.symbol

            # Set with new grid change.
            # Get symbols
            symbols = Symbol.load_symbol(self.symbol)
            self.grid[row][column] = symbols[0]
            # Draw grid.
            screen.blit(
                symbols[1],
                (self.grid_position[row][column][0], self.grid_position[row][column][1]),
            )
            self.change_player()
            if self.symbol == "x":
                self.symbol = "o"
            else:
                self.symbol = "x"

            self.check_game_won(row, column, symbol)

            return symbol
        else:
            print('Cannot put grid here.')

    def set_current_player(self, player):
        self.current_player = player

    def get_current_player(self):
        return self.current_player

    def change_player(self):
        if self.current_player == "computer":
            self.current_player = "player"
        else:
            self.current_player = "computer"

    def do_minimax(self, game_board, depth, player):
        if player == 'o':
            best_move = [-1, -1, -1000]
        else:
            best_move = [-1, -1, +1000]

        if depth == 0 or self.game_over(game_board):
            score = self.evaluate(game_board)
            return [-1, -1, score]

        for val in self.get_empty_grid_cell():
            x = val[0]
            y = val[1]
            game_board[x][y] = player
            if player == 'o':
                next_player = 'x'
            else:
                next_player = 'o'
            score = self.do_minimax(game_board, depth - 1, next_player)
            game_board[x][y] = ''
            score[0] = x
            score[1] = y

            if player == 'o':
                if score[2] > best_move[2]:
                    best_move = score

            else:
                if score[2] < best_move[2]:
                    best_move = score

        return best_move
