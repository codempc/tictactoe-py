from Screen import Screen
from Board import Board
from Player import Player

import pygame
# import ctypes

# Setup of the game
def setup():
    # Define the screen specs
    WINDOW_SIZE = [255, 255]
    title = "Tic Tac Toe"
    screen = Screen(WINDOW_SIZE, title)
    screen = screen.setup_screen()

    # Initial Setup Board (Including Players)
    choice = input('Do you want to choose x or o')
    player = Player('player', choice)
    if choice == 'x':
        computer = Player('computer', 'o')
    else:
        computer = Player('computer', 'x')
    board = Board(screen, player, computer)

    # If user choose x, user goes first and vice versa.
    if choice == 'x':
        board.set_current_player(player)
    else:
        board.set_current_player(computer)

    return screen, board, player, computer


# -------- Main Program Loop -----------
def main_loop():
    # Game setting
    [screen, board, player, computer] = setup()
    clock = pygame.time.Clock()
    done = False
    is_game_done = False

    while not done:

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:  # If user clicked close
             done = True  # Flag that we are done so we exit this loop
            elif not is_game_done:
                if board.is_full() and is_game_done is None:
                    print('Draw!')
                    done = True

                elif board.get_current_player().get_id() == 'computer':
                    best_move = board.do_minimax(board.get_grid(), len(board.get_empty_grid_cell()), computer.get_symbol())
                    column = best_move[0]
                    row = best_move[1]
                    is_game_done = board.set_grid(column, row, screen, computer)

                elif board.get_current_player().get_id() == 'player' and event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // (Board.GRID_WIDTH + Board.GRID_MARGIN)
                    row = pos[1] // (Board.GRID_HEIGHT + Board.GRID_MARGIN)

                    is_game_done = board.set_grid(row, column, screen, player)

            else:
                done = True

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

# Flow of the game
def main():
    while True:
        main_loop()
        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        response = input('Reset the game? (y/n)')
        if response == 'n':
            pygame.quit()
            break

# Prevent other function to be run before main
if __name__ == '__main__':
    main()