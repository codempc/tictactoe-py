import pygame
from Color import Color


class Screen:
    def __init__(self, size, title):
        self.size = size
        self.title = title

    def setup_screen(self):
        pygame.display.set_caption(self.title)
        screen = pygame.display.set_mode(self.size)
        screen.fill(Color.BLACK)
        return screen
