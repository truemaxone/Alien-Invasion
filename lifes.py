import pygame
from pygame.sprite import Sprite


class Lifes(Sprite):
    """Класс для жизней ака сердечек"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загружает изображение и получает прямоугольник
        self.image = pygame.image.load('images/lifes.bmp')
        self.rect = self.image.get_rect()
