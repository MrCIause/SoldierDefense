import pygame
import os

class Fireball:
    def __init__(self, x, y, direction):
        # Инициализация огненного шара с заданными координатами x и y, и направлением движения
        self.x = x
        self.y = y
        self.direction = direction  # Направление движения огненного шара (-1 влево, 1 вправо)
        self.speed = 5  # Скорость огненного шара
        self.images = [
            pygame.image.load(os.path.join('assets', 'images', 'fireBall', f'fireball{i}.png')) for i in range(1, 9)
        ]  # Загрузка изображений огненного шара для анимации
        self.images = [pygame.transform.scale(img, (img.get_width() // 1.5, img.get_height() // 1.5)) for img in self.images]  # Масштабирование изображений огненного шара

        if direction == -1:  # Если направление - влево, отразить изображения
            self.images = [pygame.transform.flip(img, True, False) for img in self.images]

        self.current_image = 0  # Индекс текущего изображения в анимации огненного шара
        self.animation_time = 0.1  # Время между кадрами анимации в секундах
        self.current_time = 0  # Текущее время анимации

    def update(self, dt):
        # Обновление состояния огненного шара на основе времени dt
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.current_image = (self.current_image + 1) % len(self.images)  # Обновление текущего изображения для анимации
        self.x += self.direction * self.speed  # Движение огненного шара в заданном направлении и скорости

    def draw(self, screen):
        # Отрисовка текущего изображения огненного шара на экране
        image = self.images[self.current_image]
        screen.blit(image, (self.x, self.y))

    def get_rect(self):
        """Возвращает прямоугольник, описывающий огненный шар, для проверки столкновений"""
        rect = self.images[self.current_image].get_rect()  # Получение прямоугольника текущего изображения огненного шара
        rect.topleft = (self.x, self.y)  # Установка положения прямоугольника
        return rect
