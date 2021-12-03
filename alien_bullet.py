import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """Класс для управления снарядами, выщенными кораблем"""

    def __init__(self, ai_game, x, y):
        """Создает объект снарядов в текущей позиции корабля"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Загрузка изображения пули-лазера
        image = pygame.image.load('images/alien_laser.bmp')
        self.image = pygame.transform.scale(image, (11, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # Позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану"""
        # Обновление позиции снаряда в вещественном формате
        self.y += self.settings.alien_bullet_speed_factor

        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def blitme(self):
        """Рисует пулю в текущей позиции"""
        self.screen.blit(self.image, self.rect)