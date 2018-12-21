import pygame
from Symbol import Symbol
from Color import Color


class Board:
    turn = 0
    symbol = "x"
    # This sets the WIDTH and HEIGHT of each grid location
    GRID_WIDTH = 80
    GRID_HEIGHT = 80
    # This sets the margin between each cell
    GRID_MARGIN = 5
    board_multiplier = 3

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
    def is_game_won(self, row, column):
        # Checking column
        for i in range(3):
            if self.grid[row][i] != self.symbol:
                break
            if i == 2:
                print(self.symbol + ' wins!')
                return True

        # Checking rows
        for i in range(3):
            if self.grid[i][column] != self.symbol:
                break
            if i == 2:
                print(self.symbol + ' wins!')
                return True

        # Checking diagonal
        if row == column:
            for i in range(3):
                if self.grid[i][i] != self.symbol:
                    break
                if i == 2:
                    print(self.symbol + ' wins!')
                    return True

        # Checking anti-diagonal
        if row + column == 2:
            for i in range(3):
                if self.grid[i][2 - i] != self.symbol:
                    break
                if i == 2:
                    print(self.symbol + ' wins!')
                    return True
        return False

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

    def set_grid(self, row, column, screen):
        if self.grid_is_empty(row, column):
            # Set with new grid change.
            if self.turn == 0:
                self.symbol = "x"
                self.turn = 1
            else:
                self.symbol = "o"
                self.turn = 0
            # Get symbols
            symbols = Symbol.load_symbol(self.symbol)
            self.grid[row][column] = symbols[0]
            screen.blit(
                symbols[1],
                (self.grid_position[row][column][0], self.grid_position[row][column][1]),
            )
        else:
            print('Cannot put grid here.')

