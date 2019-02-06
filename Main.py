from Screen import Screen
from Board import Board
from Player import Player
from Color import Color

import pygame

pygame.init()


def set_screen():
    WINDOW_SIZE = [255, 255]
    title = "Tic Tac Toe"
    screen = Screen(WINDOW_SIZE, title)
    screen = screen.setup_screen(Color.BLACK)
    clock = pygame.time.Clock()
    return screen, clock


def set_player(choice, screen):
    player = Player('player', choice)
    if choice == 'x':
        computer = Player('computer', 'o')
    else:
        computer = Player('computer', 'x')

    board = Board(screen, player, computer)
    if player.get_symbol() == 'x':
        board.set_current_player(player)
    else:
        board.set_current_player(computer)

    return player, computer, board


# def set_Board(screen, player, computer):
#     board = Board(screen, player, computer)
#     if player.get_symbol() == 'x':
#         board.set_current_player(player)
#     else:
#         board.set_current_player(computer)
#     return board


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def make_button(screen, message, x, y, width, height, passive, active, status, choice=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active, (x, y, width, height))
        if click[0] == 1 and choice is not None:
            if status == 'intro':
                main_loop(choice)
                return False
            elif status == 'outro':
                game_intro()
            else:
                pygame.quit()
                quit()

    else:
        pygame.draw.rect(screen, passive, (x, y, width, height))

    smallText = pygame.font.Font('freesansbold.ttf', 30)
    textSurf, textRect = text_objects(message, smallText, Color.WHITE)
    textRect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(textSurf, textRect)
    return True


def game_intro():
    [screen, clock] = set_screen()
    button_X = True
    button_O = True
    while button_X and button_O:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(Color.WHITE)
        largeText = pygame.font.Font('freesansbold.ttf', 25)
        TextSurf, TextRect = text_objects("Choose X or O!", largeText, Color.BLACK)
        TextRect.center = (125, 60)
        screen.blit(TextSurf, TextRect)

        button_X = make_button(screen, 'X', 64, 150, 50, 50, Color.LIGHT_RED, Color.RED, 'intro', 'x')
        button_O = make_button(screen, 'O', 135, 150, 50, 50, Color.LIGHT_BLUE, Color.BLUE, 'intro', 'o')

        pygame.display.update()
        clock.tick(15)


def game_outro():
    [screen, clock] = set_screen()
    while True:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(Color.WHITE)
        largeText = pygame.font.Font('freesansbold.ttf', 25)
        TextSurf, TextRect = text_objects("Game Over!", largeText, Color.BLACK)
        TextRect.center = (125, 60)
        screen.blit(TextSurf, TextRect)

        make_button(screen, 'Reset', 34, 150, 80, 50, Color.LIGHT_GREEN, Color.GREEN, 'outro', 'Yes')
        make_button(screen, 'Quit', 135, 150, 80, 50, Color.LIGHT_RED, Color.RED, 'quit', 'No')

        pygame.display.update()
        clock.tick(15)


# -------- Main Program Loop -----------
def main_loop(choice):
    # Game setting
    [screen, clock] = set_screen()
    [player, computer, board] = set_player(choice, screen)
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
                    game_outro()
                elif board.get_current_player().get_id() == 'computer':
                    best_move = board.do_minimax(board.get_grid(), len(board.get_empty_grid_cell()),
                                                 computer.get_symbol())
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
                game_outro()

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


# Flow of the game
def main():
    while True:
        game_intro()
        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        response = input('Reset the game? (y/n)')
        if response == 'n':
            pygame.quit()
            break


# Prevent other function to be run before main
if __name__ == '__main__':
    main()
