import pygame


class Symbol:

    @staticmethod
    def load_symbol(symbol):
        source_directory = 'source/'
        # Handle if symbol image not found or broken, load default image.
        image = pygame.image.load(source_directory + "default.png")
        try:
            image = pygame.image.load(source_directory + symbol + ".png")
        except pygame.error:
            print("Cannot load image:" + symbol + ".png")
        return [
            symbol,
            pygame.transform.scale(
                image, (80, 80)
            )
        ]
