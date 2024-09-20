# enemy.py
import pygame
import os
from fireball import Fireball
from settings import WIDTH


class Enemy:
    def __init__(self, x, y, target_x, health=3, speed=2):
        # Инициализация врага с заданными координатами x и y,
        # позицией цели (target_x), здоровьем (health) и скоростью (speed).
        self.x = x
        self.y = y
        self.target_x = target_x
        self.velocity = speed  # Скорость перемещения врага
        self.direction = 1  # Направление движения вправо

        # Загрузка изображений для анимации: покоя, атаки и смерти врага
        self.idle_images = [
            pygame.image.load(os.path.join('assets', 'images', 'enemySkeletonIdle', 'idle1.png')),
            pygame.image.load(os.path.join('assets', 'images', 'enemySkeletonIdle', 'idle2.png')),
            # ... другие изображения покоя
        ]

        self.attack_images = [
            pygame.image.load(os.path.join('assets', 'images', 'enemySkeletonAttack', f'attack{i}.png')) for i in
            range(1, 8)
        ]

        self.die_images = [
            pygame.image.load(os.path.join('assets', 'images', 'enemySkeletonDie', f'death{i}.png')) for i in
            range(1, 22)
        ]

        # Масштабирование изображений
        self.idle_images = [pygame.transform.scale(img, (img.get_width() // 1.1, img.get_height() // 1.1)) for img in
                            self.idle_images]
        self.attack_images = [pygame.transform.scale(img, (img.get_width() // 1.1, img.get_height() // 1.1)) for img in
                              self.attack_images]
        self.die_images = [pygame.transform.scale(img, (img.get_width() // 1.1, img.get_height() // 1.1)) for img in
                           self.die_images]

        # Создание зеркальных изображений для анимации
        self.flipped_idle_images = [pygame.transform.flip(img, True, False) for img in self.idle_images]
        self.flipped_attack_images = [pygame.transform.flip(img, True, False) for img in self.attack_images]
        self.flipped_die_images = [pygame.transform.flip(img, True, False) for img in self.die_images]

        self.current_image = 0  # Текущее изображение для анимации
        self.animation_time = 0.1  # Время смены кадров анимации
        self.current_time = 0  # Текущее время для анимации
        self.facing_right = False  # Направление вправо

        self.is_attacking = False  # Флаг атаки
        self.attack_time = 2.0  # Время между атаками
        self.last_attack_time = 0  # Время последней атаки

        self.is_alive = True  # Флаг живой враг
        self.is_dying = False  # Флаг смерти врага

        self.fireballs = []  # Список для огненных шаров

        self.max_health = health  # Максимальное здоровье
        self.current_health = self.max_health  # Текущее здоровье

        # Загрузка звука для огненного шара
        self.fireball_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'fireballSound.mp3'))

    def update(self, dt):
        if self.is_dying:
            # Если враг умирает, обновляем анимацию смерти
            self.current_time += dt
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.current_image += 1
                if self.current_image >= len(self.die_images):
                    self.is_alive = False
                    self.is_dying = False

            # Обновление полета огненных шаров и их удаление, если они выходят за пределы экрана
            for fireball in self.fireballs:
                fireball.update(dt)
                if fireball.x < 0 or fireball.x > WIDTH:
                    self.fireballs.remove(fireball)
            return

        if not self.is_alive:
            return

        # Обновление анимации атаки и покоя в зависимости от состояния врага
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.current_image = (self.current_image + 1) % (
                len(self.attack_images) if self.is_attacking else len(self.idle_images))

        # Движение врага к игроку, если он находится достаточно далеко
        if abs(self.x - self.target_x) > 290:
            self.is_attacking = False
            if self.x > self.target_x:
                self.x -= self.velocity
            else:
                self.x += self.velocity

        self.facing_right = self.x < self.target_x  # Определение направления врага

        # Проверка на достаточную близость к игроку для атаки
        if abs(self.x - self.target_x) <= 290:
            self.is_attacking = True
            current_time = pygame.time.get_ticks() / 1000
            if current_time - self.last_attack_time >= self.attack_time:
                self.shoot()
                self.last_attack_time = current_time

        # Обновление полета огненных шаров и их удаление, если они выходят за пределы экрана
        for fireball in self.fireballs:
            fireball.update(dt)
            if fireball.x < 0 or fireball.x > WIDTH:
                self.fireballs.remove(fireball)

    def shoot(self):
        # Выстрел огненным шаром, если враг жив и не умирает
        if not self.is_alive or self.is_dying:
            return
        direction = 1 if self.facing_right else -1 # Определение направления выстрела огненного шара в зависимости от направления врага
        fireball_x = self.x + (self.flipped_idle_images[0].get_width() if self.facing_right else 0) # Позиция огненного шара по x в зависимости от направления врага
        fireball_y = self.y + self.flipped_idle_images[0].get_height() // 2
        fireball = Fireball(fireball_x, fireball_y, direction)
        self.fireballs.append(fireball) # Добавление огненного шара в список
        self.fireball_sound.play()  # Воспроизведение звука огненного шара

    # Отрисовка текущего кадра анимации врага на экране
    def draw(self, screen):
        global images
        if self.is_dying:
            images = self.die_images if self.facing_right else self.flipped_die_images
        elif self.is_alive:
            images = self.attack_images if self.facing_right else self.flipped_attack_images
            if not self.is_attacking:
                images = self.idle_images if self.facing_right else self.flipped_idle_images

        # Проверка, что текущий кадр анимации в пределах допустимого диапазона
        if self.current_image >= len(images):
            self.current_image = len(images) - 1

        image = images[self.current_image]
        screen.blit(image, (self.x, self.y))

        # Отрисовка огненных шаров, находящихся в полете
        for fireball in self.fireballs:
            fireball.draw(screen)

        # Отрисовка полоски здоровья, если враг жив
        if self.is_alive and not self.is_dying:
            self.draw_health_bar(screen)

    # Возвращает прямоугольник, описывающий текущие размеры и положение врага на основе текущего кадра анимации
    def get_rect(self):
        if self.is_dying: # Если враг умирает, возвращаем прямоугольник с размерами изображения смерти
            image = self.die_images[self.current_image] if self.facing_right else self.flipped_die_images[
                self.current_image]
        else: # Иначе возвращаем прямоугольник с размерами текущего изображения анимации
            if self.is_attacking: # Если враг атакует, возвращаем прямоугольник с размерами изображения атаки
                if self.current_image >= len(self.attack_images):
                    self.current_image = len(self.attack_images) - 1
                image = self.attack_images[self.current_image]
            else: # Иначе возвращаем прямоугольник с размерами изображения покоя
                if self.current_image >= len(self.idle_images):
                    self.current_image = len(self.idle_images) - 1
                image = self.idle_images[self.current_image]
        rect = image.get_rect() # Получение прямоугольника изображения для проверки столкновений
        rect.topleft = (self.x, self.y) # Установка позиции прямоугольника врага на экране
        return rect # Возвращение прямоугольника для проверки столкновений

    # Проверка столкновения врага с пулей игрока
    def take_damage(self, amount):  # Принимает количество урона
        self.current_health -= amount  # Уменьшение текущего здоровья врага на величину урона
        # Если здоровье опускается до нуля и враг жив, вызываем метод умирания
        if self.current_health <= 0 and self.is_alive and not self.is_dying:
            self.current_health = 0  # Установка текущего здоровья врага в 0
            self.die()  # Вызов метода умирания

    # Установка состояния умирания врага
    def die(self):
        self.is_dying = True  # Установка флага смерти врага
        self.current_image = 0  # Сброс текущего кадра анимации

    # Отрисовка полоски здоровья врага над его головой для отображения текущего уровня здоровья
    def draw_health_bar(self, screen):
        # Отрисовка полоски здоровья над головой врага для отображения текущего уровня здоровья
        bar_width = 50  # Ширина полоски здоровья
        bar_height = 5  # Ширина и высота полоски здоровья
        health_ratio = self.current_health / self.max_health  # Определение соотношения текущего здоровья к максимальному
        fill_width = int(bar_width * health_ratio)  # Ширина заполненной части полоски здоровья
        outline_rect = pygame.Rect(self.x + 40, self.y - 10, bar_width, bar_height)  # Контур полоски здоровья
        fill_rect = pygame.Rect(self.x + 40, self.y - 10, fill_width, bar_height)  # Заполненная часть полоски здоровья
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)  # Отрисовка заполненной части полоски здоровья
        pygame.draw.rect(screen, (0, 0, 0), outline_rect, 1)  # Отрисовка контура полоски здоровья
