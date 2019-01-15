import pygame
from Color import Color

class Screen:
    def __init__(self, size, title):
        self.size = size
        self.title = title

    def setup_screen(self, color):
        pygame.display.set_caption(self.title)
        screen = pygame.display.set_mode(self.size)
        screen.fill(color)
        return screen

    # def text_objects(self, text, font):
    #         textSurface = font.render(text, True, Color.BLACK)
    #         return textSurface, textSurface.get_rect()