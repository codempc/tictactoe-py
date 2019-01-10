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

    # Check the win condition
    def is_game_won(self, row, column, symbol):
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

        return [best_move[0], best_move[1]]

        # this.getEmptyCells(gameBoard).forEach((cell) = > {
        #     const
        # x = cell[0];
        # const
        # y = cell[1];
        # gameBoard[x][y] = player;
        # const
        # nextPlayer = player == = 'x' ? 'o': 'x'
        # const
        # score = this.minimax(gameBoard, depth - 1, nextPlayer);
        # gameBoard[x][y] = null;
        # score[0] = x;
        # score[1] = y;
        #
        # if (player === 'o') {
        # if (score[2] > bestMove[2])
        # bestMove = score;
        # }
        # else {
        # if (score[2] < bestMove[2])
        # bestMove = score;
        # }
        # });
        # if depth == 0 or self.is_full():
