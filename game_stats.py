class GameStats:
    """Отслеживание статистики для игры Alien Invasion"""
    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.ships_left = self.settings.ship_limit

        # Игра запускается в неактивном состоянии
        self.time_to_blit = None
        self.broke_highscore = False
        self.game_active = False

        # Рекорд не должен сбрасываться
        self.level = 1
        self.score = 0
        self.game_count = 0  # -1 - проигрыш

        try:
            with open('highscore.txt', 'r') as file:
                self.prev_high_score = int(file.read())
        except FileNotFoundError:
            with open('highscore.txt', 'w+') as f:
                f.write('0')
            self.prev_high_score = 0

        self.high_score = self.prev_high_score

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.time_to_blit = None
        self.broke_highscore = False
        self.game_count = 0