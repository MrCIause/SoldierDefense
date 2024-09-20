import pygame
from map import GameMap
from player import Player
from enemy import Enemy
from plane import Plane
from heart import Heart
from settings import WIDTH, HEIGHT, FPS
from StartGame import StartGame
from RestartMenu import RestartMenu

def draw_text(text, font, color, surface, x, y):
    """Отображает текст на экране с заданным шрифтом и цветом"""
    textobj = font.render(text, True, color)  # Создание объекта изображения текста
    textrect = textobj.get_rect()  # Получение прямоугольника, описывающего изображение текста
    textrect.center = (x, y)  # Центрирование текста по заданным координатам
    surface.blit(textobj, textrect)  # Отображение текста на поверхности в заданных координатах

class Game:
    def __init__(self, screen):
        """Инициализация игры"""
        self.screen = screen  # Установка экрана для отображения игры
        self.clock = pygame.time.Clock()  # Инициализация часов pygame для управления FPS
        self.running = True  # Флаг работы игры
        self.show_start_menu = True  # Флаг отображения стартового меню
        self.start_game = StartGame(screen)  # Создание экземпляра стартового меню
        self.restart_menu = None  # Меню перезапуска пока не создано
        self.map = GameMap(self.screen)  # Создание игровой карты
        self.player = Player(100, HEIGHT - 150 - 50)  # Создание игрока
        self.enemies = []  # Список врагов
        self.planes = []  # Список самолетов
        self.hearts = []  # Список сердец (для восстановления здоровья игрока)
        self.bullets = []  # Список пуль игрока
        self.wave_number = 1  # Номер текущей волны
        self.enemies_per_wave = 1  # Количество врагов в первой волне
        self.enemies_spawned = 0  # Количество заспауненных врагов в текущей волне
        self.enemies_to_kill = 0  # Количество врагов, которых нужно уничтожить в текущей волне
        self.spawn_delay = 1.5  # Задержка между спаунами врагов в секундах
        self.last_spawn_time = 0  # Время последнего спауна врага
        self.plane_spawned = False  # Флаг для однократного спауна самолета за 3 раунда
        self.enemy_positions = []  # Список позиций врагов
        self.spawn_wave()  # Инициализация первой волны


    def reset_game(self):
        """Сброс игры в начальное состояние"""
        self.map = GameMap(self.screen)  # Создание новой игровой карты
        self.player = Player(100, HEIGHT - 150 - 50)  # Создание нового игрока
        self.enemies = []  # Очистка списка врагов
        self.planes = []  # Очистка списка самолетов
        self.hearts = []  # Очистка списка сердец
        self.bullets = []  # Очистка списка пуль игрока
        self.wave_number = 1  # Сброс номера текущей волны
        self.enemies_per_wave = 1  # Сброс количества врагов в первой волне
        self.enemies_spawned = 0  # Сброс количества заспауненных врагов
        self.enemies_to_kill = 0  # Сброс количества врагов для уничтожения в текущей волне
        self.spawn_delay = 1.5  # Сброс задержки между спаунами врагов
        self.last_spawn_time = 0  # Сброс времени последнего спауна врага
        self.plane_spawned = False  # Сброс флага спауна самолета
        self.enemy_positions = []  # Сброс списка позиций врагов
        self.spawn_wave()  # Инициализация первой волны

    def spawn_wave(self):
        """Подготовка к спауну новой волны врагов"""
        self.enemies_spawned = 0  # Сброс количества заспауненных врагов
        self.enemies_to_kill = self.enemies_per_wave  # Установка количества врагов для уничтожения в текущей волне
        self.last_spawn_time = pygame.time.get_ticks() / 1000  # Получение текущего времени в секундах
        self.enemy_positions = []  # Список для отслеживания позиций врагов
        for i in range(self.enemies_per_wave): # Итерация по количеству врагов в текущей волне
            self.try_spawn_enemy(self.last_spawn_time)

    def try_spawn_enemy(self, current_time):
        """Проверка, можно ли спаунить нового врага, и спаун, если это возможно"""
        if self.enemies_spawned < self.enemies_per_wave and (current_time - self.last_spawn_time >= self.spawn_delay):
            side = 'left' if self.enemies_spawned % 2 == 0 else 'right'  # Выбор стороны спауна врага (лево/право)
            self.spawn_enemy_from_side(side)  # Спаун врага с выбранной стороны
            self.last_spawn_time = current_time  # Обновление времени последнего спауна врага
            self.enemies_spawned += 1

    def spawn_enemy(self):
        """Спаун одного врага"""
        enemy = Enemy(WIDTH + 100, HEIGHT - 150 - 50, self.player.x)  # Создание врага
        self.enemies.append(enemy)  # Добавление врага в список врагов

    def spawn_enemy_from_side(self, side):
        """Спаун врага с определенной стороны (лево/право)"""
        x_position = -100 if side == 'left' else WIDTH + 100  # Вычисление позиции по x в зависимости от стороны
        enemy = Enemy(x_position, HEIGHT - 150 - 50, self.player.x)  # Создание врага

        # Ensure enemies do not spawn too close to each other
        min_distance = 100  # Минимальное расстояние между врагами
        for pos in self.enemy_positions:
            while abs(pos - enemy.x) < min_distance:
                if side == 'left':
                    enemy.x -= min_distance
                else:
                    enemy.x += min_distance

        self.enemy_positions.append(enemy.x)  # Track the position of the newly spawned enemy
        self.enemies.append(enemy)  # Добавление врага в список врагов

    def spawn_plane(self):
        """Спаун самолета"""
        plane = Plane(50)  # Создание самолета (можно адаптировать положение по y по необходимости)
        self.planes.append(plane)  # Добавление самолета в список самолетов
        self.plane_spawned = True  # Установка флага, чтобы самолет спаунился только один раз за 3 раунда

    def run(self):
        """Основной игровой цикл"""
        while self.running:  # Основной игровой цикл, работает пока флаг running установлен в True
            dt = self.clock.tick(FPS) / 1000  # Получение времени, прошедшего с последнего кадра в секундах
            self.events()  # Обработка событий (например, нажатий клавиш)
            if self.show_start_menu:  # Если отображается стартовое меню
                self.start_game.draw()  # Отрисовка стартового меню
                pygame.display.flip()  # Обновление экрана
                if self.start_game.is_start_clicked():  # Если нажата кнопка начала игры
                    self.show_start_menu = False  # Скрыть стартовое меню
                    self.reset_game()  # Сбросить игру к начальному состоянию
            elif self.player.is_dead and self.player.current_image == len(self.player.death_images) - 1:
                self.show_restart_menu()  # Показать меню перезапуска после смерти игрока
            else:
                self.update(dt)  # Обновление состояния игры
                self.draw()  # Отрисовка игры

    def events(self):
        """Обработка событий (например, нажатий клавиш)"""
        for event in pygame.event.get():  # Получение всех событий pygame
            if event.type == pygame.QUIT:  # Если пользователь закрыл окно игры
                self.running = False  # Установка флага running в False (завершение игрового цикла)

            if event.type == pygame.KEYDOWN and not self.show_start_menu and not self.player.is_dead:
                # Если была нажата клавиша и игра не в стартовом меню и игрок не мертв
                if event.key == pygame.K_UP:
                    self.player.jump()  # Вызов метода прыжка у игрока
                if event.key == pygame.K_SPACE:
                    self.player.shoot()  # Вызов метода выстрела у игрока

        keys = pygame.key.get_pressed()  # Получение состояния всех клавиш на клавиатуре
        if not self.show_start_menu and not self.player.is_dead:  # Если игра не в стартовом меню и игрок не мертв
            if keys[pygame.K_LEFT]:
                self.player.move_left()  # Движение игрока влево
            elif keys[pygame.K_RIGHT]:
                self.player.move_right()  # Движение игрока вправо
            else:
                self.player.stop()  # Остановка движения игрока

    def update(self, dt):
        """Обновление состояния игры"""
        self.player.update(dt, self.map.platforms, self.hearts)  # Обновление состояния игрока
        enemies_alive = 0  # Количество живых врагов

        for enemy in self.enemies:  # Итерация по всем врагам
            enemy.target_x = self.player.x  # Установка целевой координаты x для врага
            enemy.update(dt)  # Обновление состояния врага

            for fireball in list(enemy.fireballs):  # Итерация по копии списка огненных шаров врага
                if fireball.get_rect().colliderect(self.player.get_rect()):  # Если произошло столкновение огненного шара с игроком
                    enemy.fireballs.remove(fireball)  # Удаление огненного шара из списка врага
                    self.player.take_damage(1)  # Нанесение урона игроку

            for bullet in list(self.player.bullets):  # Итерация по копии списка пуль игрока
                if bullet.get_rect().colliderect(enemy.get_rect()):  # Если произошло столкновение пули с врагом
                    if bullet in self.player.bullets:  # Проверка, что пуля все еще в списке игрока
                        self.player.bullets.remove(bullet)  # Удаление пули из списка игрока
                    enemy.take_damage(1)  # Нанесение урона врагу

            if enemy.is_alive or enemy.is_dying:  # Если враг жив или находится в состоянии умирания
                enemies_alive += 1  # Увеличение счетчика живых врагов

        self.map.update(self.player.x)  # Обновление карты (перемещение при необходимости)

        for bullet in list(self.player.bullets):  # Итерация по копии списка пуль игрока
            bullet.update()  # Обновление состояния пули
            if bullet.x > WIDTH or bullet.x < 0:  # Если пуля вышла за пределы экрана по x
                if bullet in self.player.bullets:  # Проверка, что пуля все еще в списке игрока
                    self.player.bullets.remove(bullet)  # Удаление пули из списка игрока

        # Обновление и удаление самолетов
        for plane in list(self.planes):  # Итерация по копии списка самолетов
            heart = plane.update(dt)  # Обновление состояния самолета и получение возможного сердца
            if heart:  # Если вернулось сердце (не None)
                self.hearts.append(heart)  # Добавление сердца в список сердец
            if plane.off_screen(WIDTH):  # Если самолет вышел за пределы экрана
                plane.stop_flying_sound()  # Остановка звука полета самолета
                self.planes.remove(plane)  # Удаление самолета из списка
            else:
                plane.start_flying_sound()  # Запуск звука полета самолета

        # Обновление сердец
        for heart in self.hearts:  # Итерация по всем сердцам
            heart.update(dt, self.map.platforms)  # Обновление состояния сердца и передача платформ для проверки столкновений

        # Удаление мертвых врагов
        self.enemies = [enemy for enemy in self.enemies if enemy.is_alive or enemy.is_dying]

        # Проверка завершения волны
        current_time = pygame.time.get_ticks() / 1000  # Получение текущего времени в секундах
        self.try_spawn_enemy(current_time)  # Попытка спауна нового врага, если это возможно

        if enemies_alive == 0 and self.enemies_spawned == self.enemies_per_wave:
            # Если все враги уничтожены и спауненны все враги текущей волны
            self.wave_number += 1  # Увеличение номера волны
            self.enemies_per_wave += 1  # Увеличение количества врагов в следующей волне
            self.spawn_delay = max(0.35, self.spawn_delay - 0.1)  # Уменьшение задержки спауна, но не менее 0.5 секунд
            self.spawn_wave()  # Инициализация следующей волны
            self.plane_spawned = False  # Сброс флага спауна самолета для новой волны

        # Спаун самолета каждые 3 волны
        if self.wave_number % 4 == 0 and not self.plane_spawned:
            self.spawn_plane()  # Спаун самолета

    def show_restart_menu(self):
        """Отображение меню перезапуска игры"""
        if not self.restart_menu:  # Если меню перезапуска еще не создано
            self.restart_menu = RestartMenu(self.screen, self.wave_number)  # Создание меню перезапуска

        self.restart_menu.draw()  # Отрисовка меню перезапуска
        pygame.display.flip()  # Обновление экрана
        if self.restart_menu.is_restart_clicked():  # Если была нажата кнопка перезапуска
            self.show_start_menu = False  # Скрыть стартовое меню
            self.reset_game()  # Сбросить игру к начальному состоянию

    def draw(self):
        """Отрисовка всех элементов игры на экране"""
        self.map.draw()  # Отрисовка карты
        self.player.draw(self.screen)  # Отрисовка игрока
        for enemy in self.enemies:  # Итерация по всем врагам и их отрисовка
            enemy.draw(self.screen)

        for plane in self.planes:  # Итерация по всем самолетам и их отрисовка
            plane.draw(self.screen)

        for heart in self.hearts:  # Итерация по всем сердцам и их отрисовка
            heart.draw(self.screen)

        # Отображение номера волны
        font = pygame.font.Font(None, 74)  # Задание шрифта для текста
        text = f"Wave {self.wave_number -1}"  # Текст для отображения номера волны
        draw_text(text, font, (255, 255, 255), self.screen, WIDTH // 2, 50)  # Вызов функции для отрисовки текста

        pygame.display.flip()  # Обновление экрана
