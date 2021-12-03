import pygame


class Settings:
    """Класс для хранения всех настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализирует статические настройки игры"""
        # Параметры экрана
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 0, 0)

        self.background = pygame.image.load('images/background2.jpg')
        self.background_rect = self.background.get_rect()
        self.start_frame = 0

        # Параметры снаряда
        self.bullets_allowed = 5

        # Настройки корабля
        self.ship_limit = 3

        # Насторйки прищельцев
        self.fleet_drop_speed = 10

        # Параметры выстрелов пришельцев
        self.alien_cooldown = 1500  # milliseconds
        self.last_alien_shot = pygame.time.get_ticks()

        # Темп ускорения игры
        self.speedup_scale = 1.1

        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Иницализирует настройки, изменяющиеся в ходе игры"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_bullet_speed_factor = 1.5
        self.alien_speed_factor = 1.0

        # fleet_direction = 1 обозначает движение вправо, а -1 - влево
        self.fleet_direction = 1

        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости игры и стоимости пришельцев"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_bullet_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
