import pygame


class BaseSettings:
    # colors
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 128)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    SNAKE_GREEN = (81, 110, 17)
    LIGHTGREEN = (142, 192, 17)
    ROTTEN = (122, 65, 0)

    # screen size
    WIDTH = 720
    HEIGHT = 480

    # refresh rate
    fps_controller = pygame.time.Clock()


game_window = pygame.display.set_mode((BaseSettings.WIDTH, BaseSettings.HEIGHT))
