# player.py
import pygame  # Импорт библиотеки Pygame для работы с графикой и звуком
import os  # Импорт модуля os для работы с файловой системой
from Bullet import Bullet  # Импорт класса Bullet из файла Bullet.py
from settings import WIDTH, HEIGHT, PLATFORM_HEIGHT  # Импорт констант WIDTH, HEIGHT, PLATFORM_HEIGHT из файла settings.py

class Player:
    def __init__(self, x, y):
        self.x = x  # Установка начальной координаты X игрока
        self.y = y  # Установка начальной координаты Y игрока
        self.velocity = 5  # Установка скорости перемещения игрока
        self.jump_power = 21  # Установка силы прыжка
        self.gravity = 1  # Установка значения гравитации
        self.is_jumping = False  # Флаг состояния - игрок в процессе прыжка
        self.is_falling = False  # Флаг состояния - игрок в процессе падения
        self.jump_speed = 0  # Скорость текущего прыжка
        self.platform_height = PLATFORM_HEIGHT  # Высота платформы, на которой стоит игрок
        self.is_dead = False  # Флаг состояния - игрок мёртв

        # Загрузка изображений для состояний анимации игрока
        self.idle_images = [
            pygame.image.load(os.path.join('assets', 'images', 'soldierIdle', 'idle1.png')),
            pygame.image.load(os.path.join('assets', 'images', 'soldierIdle', 'idle2.png'))
        ]
        self.run_images = [
            pygame.image.load(os.path.join('assets', 'images', 'soldierWalk', 'run1.png')),
            pygame.image.load(os.path.join('assets', 'images', 'soldierWalk', 'run2.png')),
            pygame.image.load(os.path.join('assets', 'images', 'soldierWalk', 'run3.png')),
            pygame.image.load(os.path.join('assets', 'images', 'soldierWalk', 'run4.png')),
            pygame.image.load(os.path.join('assets', 'images', 'soldierWalk', 'run5.png')),
            pygame.image.load(os.path.join('assets', 'images', 'soldierWalk', 'run6.png'))
        ]
        self.jump_image = pygame.image.load(os.path.join('assets', 'images', 'soldierJump', 'jump.png'))
        self.fall_image = pygame.image.load(os.path.join('assets', 'images', 'soldierJump', 'fall.png'))
        self.death_images = [
            pygame.image.load(os.path.join('assets', 'images', 'soldierDeath', 'Death1.png')),
            pygame.image.load(os.path.join('assets', 'images', 'soldierDeath', 'Death2.png')),
            pygame.image.load(os.path.join('assets', 'images', 'soldierDeath', 'Death3.png')),
            pygame.image.load(os.path.join('assets', 'images', 'soldierDeath', 'Death4.png')),
            pygame.image.load(os.path.join('assets', 'images', 'soldierDeath', 'Death5.png')),
            pygame.image.load(os.path.join('assets', 'images', 'soldierDeath', 'Death6.png'))
        ]

        # Изменение размера изображений для анимации
        self.idle_images = [pygame.transform.scale(img, (img.get_width() // 2.1, img.get_height() // 2.1)) for img in self.idle_images]
        self.run_images = [pygame.transform.scale(img, (img.get_width() // 2.1, img.get_height() // 2.1)) for img in self.run_images]
        self.jump_image = pygame.transform.scale(self.jump_image, (
            self.jump_image.get_width() // 2.1, self.jump_image.get_height() // 2.1))
        self.fall_image = pygame.transform.scale(self.fall_image, (
            self.fall_image.get_width() // 2.1, self.fall_image.get_height() // 2.1))
        self.death_images = [pygame.transform.scale(img, (img.get_width() // 2.1, img.get_height() // 2.1)) for img in self.death_images]

        self.current_image = 0  # Текущее изображение для анимации
        self.animation_time = 0.1  # Время анимации
        self.current_time = 0  # Текущее время
        self.is_running = False  # Флаг состояния - игрок в движении
        self.direction = 0  # Направление движения (-1 - влево, 1 - вправо)
        self.facing_right = True  # Флаг направления - игрок смотрит вправо
        self.bullets = []  # Список пуль, выпущенных игроком

        # Звук стрельбы
        self.shoot_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'shootingSound.mp3'))
        self.shoot_sound.set_volume(0.5)

        # Звук смерти
        self.death_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'ManDeath.mp3'))
        self.death_sound.set_volume(0.5)

        self.last_shot_time = 0  # Время последнего выстрела
        self.shoot_interval = 0.25  # Интервал между выстрелами

        self.max_health = 6  # Максимальное количество здоровья игрока
        self.current_health = self.max_health  # Текущее количество здоровья игрока

    def update(self, dt, platforms, hearts, collision_ground=True):
        self.current_time += dt  # Обновление времени для анимации игрока и пуль в секундах (dt - время в секундах с момента последнего обновления)

        if self.is_dead: # Если игрок мёртв
            self.handle_death_animation(dt)  # Обработка анимации смерти
            return

        if self.current_time >= self.animation_time: # Если время анимации истекло
            self.current_time = 0 # Обнуление времени анимации
            if self.is_running: # Если игрок бежит
                self.current_image = (self.current_image + 1) % len(self.run_images) # Переключение изображения для анимации бега
            else: # Если игрок стоит
                self.current_image = (self.current_image + 1) % len(self.idle_images) # Переключение изображения для анимации покоя

        self.x += self.direction * self.velocity  # Изменение координаты X в зависимости от направления движения
        self.x = max(0, min(self.x, WIDTH - self.idle_images[0].get_width()))  # Ограничение движения игрока по X

        self.apply_gravity(platforms, collision_ground)  # Применение гравитации к игроку и проверка столкновений с платформами
        self.check_heart_collision(hearts)  # Проверка коллизий с сердцами на уровне

        for bullet in self.bullets: # Итерация по списку пуль игрока
            bullet.update()  # Обновление состояния пуль
            if bullet.x > WIDTH or bullet.x < 0: # Если пуля вышла за пределы экрана по X
                self.bullets.remove(bullet)  # Удаление пули, если она вышла за пределы экрана

    def handle_death_animation(self, dt):
        death_animation_time = 0.2  # Время анимации смерти
        self.current_time += dt # Обновление времени для анимации смерти в секундах
        if self.current_time >= death_animation_time: # Если время анимации смерти истекло
            self.current_time = 0 # Обнуление времени анимации
            if self.current_image < len(self.death_images) - 1:
                self.current_image += 1  # Переключение изображения для анимации смерти

    def apply_gravity(self, platforms, collision_ground): # Применение гравитации к игроку и проверка столкновений с платформами
        if self.is_jumping: # Если игрок прыгает
            self.y -= self.jump_speed  # Изменение координаты Y при прыжке
            self.jump_speed -= self.gravity  # Изменение скорости прыжка под воздействием гравитации
            if self.jump_speed < -self.jump_power: # Если скорость прыжка меньше силы прыжка
                self.is_jumping = False # Прекращение прыжка
                self.is_falling = True # Начало падения

        if self.is_falling: # Если игрок падает
            self.y += self.gravity  # Изменение координаты Y при падении
            collision = False # Флаг столкновения с платформой
            if not collision and collision_ground and self.y >= HEIGHT - self.platform_height - self.get_rect().height: # Если игрок касается земли и не столкнулся с платформой ранее
                self.y = HEIGHT - self.platform_height - self.get_rect().height # Установка координаты Y на уровне земли
                self.is_falling = False # Прекращение падения

    def check_heart_collision(self, hearts): # Проверка коллизий с сердцами на уровне игрока
        player_rect = self.get_rect() # Получение прямоугольника, описывающего положение игрока
        for heart in list(hearts):  # Итерация по копии списка сердец
            if player_rect.colliderect(heart.get_rect()): # Если игрок столкнулся с сердцем
                hearts.remove(heart)  # Удаление сердца при коллизии
                self.current_health = self.max_health  # Восстановление здоровья до максимального значения

    def draw(self, screen): # Отрисовка игрока на экране
        global image
        if self.is_dead: # Если игрок мёртв
            image = self.death_images[self.current_image]  # Отрисовка изображения при смерти
        elif self.is_jumping: # Если игрок прыгает
            image = self.jump_image  # Отрисовка изображения при прыжке
        elif self.is_falling: # Если игрок падает
            image = self.fall_image  # Отрисовка изображения при падении
        elif self.is_running: # Если игрок бежит
            if 0 <= self.current_image < len(self.run_images): # Если текущее изображение в пределах диапазона изображений для анимации бега
                image = self.run_images[self.current_image]  # Отрисовка изображения при беге
            else: # Если текущее изображение выходит за пределы диапазона изображений для анимации бега
                image = self.run_images[0] # Отрисовка первого изображения для анимации бега
        else: # Если игрок стоит
            if 0 <= self.current_image < len(self.idle_images): # Если текущее изображение в пределах диапазона изображений для анимации покоя
                image = self.idle_images[0]  # Отрисовка изображения в состоянии покоя

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)  # Отражение изображения при повороте влево

        screen.blit(image, (self.x, self.y))  # Отображение изображения игрока на экране

        for bullet in self.bullets:
            bullet.draw(screen)  # Отрисовка пуль

        self.draw_health_bar(screen)  # Отрисовка полоски здоровья

    def move_left(self):
        if not self.is_dead:
            self.is_running = True  # Игрок начинает бег влево
            self.direction = -1  # Установка направления движения влево
            self.facing_right = False  # Установка направления взгляда влево

    def move_right(self):
        if not self.is_dead:
            self.is_running = True  # Игрок начинает бег вправо
            self.direction = 1  # Установка направления движения вправо
            self.facing_right = True  # Установка направления взгляда вправо

    def stop(self):
        if not self.is_dead:
            self.is_running = False  # Остановка бега
            self.direction = 0  # Обнуление направления движения

    def jump(self):
        if not self.is_dead and not self.is_jumping and not self.is_falling:
            self.is_jumping = True  # Игрок начинает прыжок
            self.jump_speed = self.jump_power  # Установка скорости прыжка

    def shoot(self):
        if not self.is_dead:
            current_time = pygame.time.get_ticks() / 1000
            if not self.is_running and (current_time - self.last_shot_time >= self.shoot_interval):
                bullet_x = self.x + self.idle_images[0].get_width() if self.facing_right else self.x
                bullet_y = self.y + self.idle_images[0].get_height() // 2
                direction = 1 if self.facing_right else -1
                bullet = Bullet(bullet_x, bullet_y, direction)
                self.bullets.append(bullet)  # Выстрел игрока
                self.shoot_sound.play()  # Проигрывание звука выстрела
                self.last_shot_time = current_time  # Обновление времени последнего выстрела

    def get_rect(self):
        global image
        if self.is_dead:
            image = self.death_images[self.current_image]
        elif self.is_jumping:
            image = self.jump_image
        elif self.is_falling:
            image = self.fall_image
        elif self.is_running:
            if 0 <= self.current_image < len(self.run_images):
                image = self.run_images[self.current_image]
            else:
                image = self.run_images[0]
        else:
            if 0 <= self.current_image < len(self.idle_images):
                image = self.idle_images[0]

        rect = image.get_rect()  # Получение прямоугольника, описывающего положение изображения
        rect.topleft = (self.x, self.y)  # Установка позиции прямоугольника
        return rect

    def take_damage(self, amount): # Получение урона игроком
        if not self.is_dead: # Если игрок жив
            self.current_health -= amount  # Уменьшение здоровья игрока
            if self.current_health <= 0: # Если здоровье игрока меньше или равно нулю
                self.current_health = 0 # Установка здоровья игрока в ноль
                self.die()  # Если здоровье меньше или равно нулю, игрок умирает

    def die(self):
        self.is_dead = True  # Установка состояния - игрок мёртв
        self.current_image = 0  # Начало анимации смерти
        self.death_sound.play()  # Проигрывание звука смерти
        print("Player has died")  # Вывод сообщения о смерти игрока

    def draw_health_bar(self, screen):
        bar_width = 50  # Ширина полоски здоровья
        bar_height = 5  # Высота полоски здоровья
        health_ratio = self.current_health / self.max_health  # Отношение текущего здоровья к максимальному
        fill_width = int(bar_width * health_ratio)  # Ширина заполненной части полоски здоровья
        outline_rect = pygame.Rect(self.x + 30, self.y - 10, bar_width, bar_height)  # Прямоугольник для обводки полоски здоровья
        fill_rect = pygame.Rect(self.x + 30, self.y - 10, fill_width, bar_height)  # Прямоугольник для заполненной части полоски здоровья
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)  # Отрисовка заполненной части полоски здоровья
        pygame.draw.rect(screen, (0, 0, 0), outline_rect, 1)  # Отрисовка обводки полоски здоровья
