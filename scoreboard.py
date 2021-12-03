import pygame.font
from pygame.sprite import Group
from lifes import Lifes


class Scoreboard:
    """Класс для вывода игровой информации"""

    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчета очков"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройки шрифта для выводы счета
        self.text_color = (249, 211, 66)
        self.font = pygame.font.Font('fonts/Handylinedfont.ttf', 30)

        # Подготовка изображения счетов
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.dur_congratulation_message = 3000  # milliseconds

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение"""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score : {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def print_high_score_msg(self):
        """Выводит поздравление с рекордом"""
        if self.stats.score > self.stats.prev_high_score and not self.stats.broke_highscore:
            self.stats.time_to_blit = pygame.time.get_ticks() + self.dur_congratulation_message
            self.stats.broke_highscore = True
            record_sound = pygame.mixer.Sound('sounds/bit_record.mp3')
            record_sound.set_volume(0.5)
            record_sound.play()

        if self.stats.time_to_blit:
            self.screen.blit(self.congratulation_image, self.congratulation_rect)
            if pygame.time.get_ticks() >= self.stats.time_to_blit:
                self.stats.time_to_blit = None

    def show_score(self):
        """Выводит текущий счет, рекорд и число оставшихся кораблей на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        self.print_high_score_msg()

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        # Рекорд выравнивается по центру верхней стороны
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

        # Поздравление с рекордом
        congratulation = "Congratulations! New High Score."
        self.congratulation_image = self.font.render(congratulation, True, self.text_color)

        # Поздравление выравнивается по центру верхней стороны ниже рекорда
        self.congratulation_rect = self.congratulation_image.get_rect()
        self.congratulation_rect.centerx = self.screen_rect.centerx
        self.congratulation_rect.top = self.score_rect.top + 40

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            with open('highscore.txt', 'w+') as file:
                file.write(f'{self.stats.high_score}')
            self.prep_high_score()

    def prep_level(self):
        """Преобразует уровень в графическое изображение"""
        level_str = "Level : " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Уровень выводится под текущим счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Сообщает количество оставшихся кораблей"""
        self.ships = Group()
        for number in range(self.stats.ships_left):
            life = Lifes(self)
            life.rect.x = 10 + number * life.rect.width
            life.rect.y = 10
            self.ships.add(life)
