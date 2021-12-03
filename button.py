import pygame


class Button:

    def __init__(self, ai_game):
        """Инициализирует атрибуты кнопки"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Назначение размеров и свойств кнопок
        self.button_image = pygame.image.load('images/play_button.png')
        self.button_image = pygame.transform.scale(self.button_image, (224, 100))
        self.button_image_rect = self.button_image.get_rect()
        self.button_image_rect.centerx = self.screen_rect.centerx
        self.button_image_rect.centery = self.screen_rect.centery - 50

    def draw_button(self):
        # Отображение кнопки
        self.screen.blit(self.button_image, self.button_image_rect)
