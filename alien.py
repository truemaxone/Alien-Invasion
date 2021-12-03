import pygame
from pygame.sprite import Sprite
import random


class Alien(Sprite):
    """Класс, представляющий одного пришельца"""

    def __init__(self, ai_game):
        """Инициализирует пришельца и задает его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Загрузка изображения пришельца и назначение атрибута rect.
        self.image = pygame.image.load('images/alien' + str(random.randint(1, 4)) + ".bmp")
        self.image = pygame.transform.scale(self.image, (85, 85))
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в верхнем левом углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции пришельца
        self.x = float(self.rect.x)

        # Создание маски, чтобы коллизии были именно с объектом,а не с rect картинки
        self.mask = pygame.mask.from_surface(self.image)

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Перемещает пришельцев влево или вправо"""
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.x
