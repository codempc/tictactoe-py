from Screen import Screen
from Board import Board

import pygame
# import ctypes

# Define the screen specs
WINDOW_SIZE = [255, 255]
title = "Tic Tac Toe"
screen = Screen(WINDOW_SIZE, title)
screen = screen.setup_screen()

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

symbol = "x"

# Setup Board
board = Board(screen)

# def display_message(title, message):
#     # MessageBox = ctypes.windll.user32.MessageBoxW
#     # MessageBox(None, message, title, 0)
#     # confirm('text', 'button', ['title'])

# Loop until the user clicks the close button.
done = False

# -------- Main Program Loop -----------
while not done:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif symbol == "o":
            [row, column] = board.do_minimax(0)
            symbol = board.set_grid(row, column, screen)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (Board.GRID_WIDTH + Board.GRID_MARGIN)
            row = pos[1] // (Board.GRID_HEIGHT + Board.GRID_MARGIN)

            symbol = board.set_grid(row, column, screen)

            is_game_won = board.is_game_won(row, column, symbol)
            done = bool(is_game_won)

            if board.is_full() and is_game_won is None:
                done = True
                print('Draw!')

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
