import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    """Пoдкласс oбъектoв взрывoв при пoпадании"""
    def __init__(self, x, y, size):
        super().__init__()
        self.images = []
        for num in range(9):
            image = pygame.image.load(f"images/regularExplosion0{num}.bmp")
            if size == 1:
                image = pygame.transform.scale(image, (40, 40))
            if size == 2:
                image = pygame.transform.scale(image, (100, 100))
            if size == 3:
                image = pygame.transform.scale(image, (200, 200))
            # Добавляем в список
            self.images.append(image)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 15
        # Обновление анимации взрыва
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # Анимация закончилась - удалить взрыв
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
