import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс для управления снарядами, выщенными кораблем"""

    def __init__(self, ai_game):
        """Создает объект снарядов в текущей позиции корабля"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Загрузка изображения пули-лазера
        image = pygame.image.load('images/bullet_laser3.bmp')
        self.image = pygame.transform.scale(image, (11, 50))
        self.rect = self.image.get_rect()

        # Создание снаряда в позиции (0,0) и назначение правильной позиции
        self.rect.midtop = ai_game.ship.rect.midtop

        # Позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану"""
        # Обновление позиции снаряда в вещественном формате
        self.y -= self.settings.bullet_speed_factor

        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def blitme(self):
        """Рисует пулю в текущей позиции"""
        self.screen.blit(self.image, self.rect)
