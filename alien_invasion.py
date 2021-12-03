import sys
import random
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien_bullet import AlienBullet
from alien import Alien
from explosion import Explosion

clock = pygame.time.Clock()
fps = 240


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()  # для звука
        self.settings = Settings()

        # Иконка окна с игрой
        icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(icon)

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # Настройки шрифта
        self.text_color = (249, 211, 66)
        self.font = pygame.font.Font('fonts/Handylinedfont.ttf', 30)

        # FULLSCREEN
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # Название окна с игрой
        pygame.display.set_caption('Alien Invasion')

        # Создание экземпляров для хранения статистики и панели результатов
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self._create_fleet()

        # Создание кнопки Play
        self.play_button = Button(self)

    def run_game(self):
        """Запуск одного цикла игры"""

        # Музыка на заставку
        pygame.mixer.music.load('sounds/start_game.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1, 0)

        while True:

            clock.tick(fps)

            # Отслеживание событий с клавиатуры и мыши
            self._check_events()

            # Разделение на части, которые выполняются всегда и те части, которые только при активной игре
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien_bullets()
                self._update_aliens()
                self.explosions.update()
                self.alien_shoot()

            self._update_screen()

            # Отображение последнего прорисованного экрана
            pygame.display.flip()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        button_clicked = self.play_button.button_image_rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Фoнoвая музыка.
            play_track = random.choice(('sounds/music1.mp3', 'sounds/music2.mp3', 'sounds/music3.mp3'))
            pygame.mixer.music.load(play_track)
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1, 0)

            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Указатель мыши скрывается
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        # Движение корабля влево-вправо
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            shoot_sound = pygame.mixer.Sound('sounds/shot.ogg')
            shoot_sound.play()
            shoot_sound.set_volume(0.1)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        # Обновление позиций снарядов
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():  # т.к. эл-ты из списка в цикле for не должны удаляться, перебираем копию
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                self.stats.score -= 10
                if self.stats.score < 0:
                    self.stats.score = 0
                self.sb.prep_score()

        self._check_bullet_alien_collisions()

    def _update_alien_bullets(self):
        # Обновление позиций снарядов
        self.alien_bullets.update()

        # Удаление снарядов, вышедших за край экрана
        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.top > self.settings.screen_height:
                self.alien_bullets.remove(alien_bullet)

        self._check_alien_bullet_ship_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами"""
        # Проверка попаданий в пришельцев
        # При обнаружении попадания удаляет снаряд и пришельца(удаление снарядов и пришельцев, участв.в коллизиях)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True, pygame.sprite.collide_mask)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            for alien, bullet in collisions.items():
                pos = bullet[0].rect.center
                explosion = Explosion(pos[0], pos[1], 2)
                self.explosions.add(explosion)

            explosion_sound1 = pygame.mixer.Sound('sounds/explosion.ogg')
            explosion_sound2 = pygame.mixer.Sound('sounds/explosion2.ogg')
            explosion_sound1.set_volume(0.4)
            explosion_sound2.set_volume(0.4)
            explosions = (explosion_sound1, explosion_sound2)
            random.choice(explosions).play()
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Уничтожение существующих снарядов, повышение скорости и создание нового флота
            pygame.mixer.music.pause()
            next_level_sound = pygame.mixer.Sound('sounds/level_complete.ogg')
            next_level_sound.play()

            self.bullets.empty()
            self.settings.increase_speed()

            # Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()
            self._create_fleet()

            # Экран lvl-up
            self.screen.blit(self.settings.background, self.settings.background_rect)
            self.draw_levelup_page()
            self.alien_bullets.empty()
            sleep(4)

            pygame.mixer.music.unpause()

    def _check_alien_bullet_ship_collisions(self):
        """Обработка коллизий снарядов пришельцев и корабля"""
        # Проверка попаданий в корабль
        # При обнаружении попадания удаляет снаряд и минусует жизнь
        collisions = pygame.sprite.spritecollide(self.ship, self.alien_bullets, True, pygame.sprite.collide_mask)

        if collisions:
            for alien_bullet in collisions:
                explosion = Explosion(alien_bullet.rect.centerx, alien_bullet.rect.centery, 1)
                self.explosions.add(explosion)

            self._ship_hit()

    def alien_shoot(self):
        # фиксируем текущее время
        time_now = pygame.time.get_ticks()
        # выстрел
        if time_now - self.settings.last_alien_shot > self.settings.alien_cooldown and \
                len(self.alien_bullets) < 5 and len(self.aliens) > 0:
            attacking_alien = random.choice(self.aliens.sprites())
            self.alien_bullet = AlienBullet(self, attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            self.alien_bullets.add(self.alien_bullet)
            self.settings.last_alien_shot = time_now
            shoot_sound = pygame.mixer.Sound('sounds/alien_shot2.ogg')
            shoot_sound.play()
            shoot_sound.set_volume(0.08)

    def _update_aliens(self):
        """Проверяет, достиг ли флот края экрана, с последующим обновлением позиций всех пришельцев во флоте"""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens, pygame.sprite.collide_mask):
            self._ship_hit()

        # Проверить, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Создание флота вторжения"""
        # Создание пришельца и вычисление количества пришельцев в ряду
        # Интервал между соседними пришельцами равен ширине пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определяет количество рядов, помещающихся на экране"""
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Обрабатывает столкновения корабля с пришельцем"""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Звук столкновения
            hit_sound = pygame.mixer.Sound('sounds/hit.ogg')
            hit_sound.set_volume(0.25)
            hit_sound.play()

            # Создание нового флота и размещение корабля в центре
            # self._create_fleet()
            # self.ship.center_ship()

        else:
            # Звук взрыва корабля
            explosion_sound = pygame.mixer.Sound('sounds/explosion.ogg')
            explosion_sound.set_volume(0.25)
            explosion_sound.play()

            explosion = Explosion(self.ship.rect.centerx, self.ship.rect.centery, 3)
            self.explosions.add(explosion)

            pygame.mixer.music.load('sounds/game_over.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)

            self.alien_bullets.empty()

            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.stats.game_count -= 1

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break

    def draw_home_page(self):
        home_image = pygame.image.load("images/home.png")
        home_image_rect = home_image.get_rect()
        self.screen.blit(home_image, (self.settings.screen_width / 2 - home_image_rect.width / 2, 0))

    def draw_gameover_page(self):
        game_over_image = pygame.image.load("images/game_over.png")
        game_over_image_rect = game_over_image.get_rect()
        self.screen.blit(game_over_image, (self.settings.screen_width / 2 - game_over_image_rect.width / 2, 0))

    def draw_levelup_page(self):
        level_up_image = pygame.image.load("images/level_up.png")
        self.screen.blit(level_up_image, (0, 0))
        pygame.display.flip()

    def animated_background(self):
        # Анимация фона
        self.screen.blit(self.settings.background, (0, self.settings.start_frame))
        self.screen.blit(self.settings.background,
                         (0, -self.settings.background_rect.height + self.settings.start_frame))

        if self.settings.start_frame == self.settings.background_rect.height:
            self.screen.blit(self.settings.background,
                             (0, -self.settings.background_rect.height + self.settings.start_frame))
            self.settings.start_frame = 0

        self.settings.start_frame += 1

    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран"""

        self.screen.blit(self.settings.background, self.settings.background_rect)
        self.animated_background()

        self.aliens.draw(self.screen)
        self.bullets.draw(self.screen)
        self.alien_bullets.draw(self.screen)
        self.explosions.draw(self.screen)
        self.ship.blitme()

        # Вывод информации о счете
        self.sb.show_score()

        # Кнопка Play отображается в том случает, если игра неактивна
        if not self.stats.game_active:
            if self.stats.game_count == 0:
                self.draw_home_page()

            elif self.stats.game_count == -1:
                self.explosions.update()
                self.draw_gameover_page()


            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
