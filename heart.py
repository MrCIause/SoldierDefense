import pygame
import os

class Heart:
    def __init__(self, x, y):
        # Инициализация сердца с заданными координатами x и y
        self.x = x
        self.y = y
        self.velocity = 3  # Скорость падения сердца
        self.image = pygame.image.load(os.path.join('assets', 'images', 'Heart.png'))  # Загрузка изображения сердца
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() // 2 + 100, self.image.get_height() // 2 + 100))  # Масштабирование изображения сердца
        self.falling = True  # Флаг, указывающий на то, что сердце все еще падает

    def update(self, dt, platforms):
        # Обновление состояния сердца на основе времени dt и платформ, на которые оно может падать
        if self.falling:
            self.y += self.velocity  # Падение сердца вниз с заданной скоростью
            self.check_collision(platforms)  # Проверка столкновения сердца с платформами

    def draw(self, screen):
        # Отрисовка изображения сердца на экране
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        # Возвращает прямоугольник, описывающий текущие размеры и положение сердца на основе его изображения
        return self.image.get_rect(topleft=(self.x, self.y))

    def check_collision(self, platforms):
        # Проверка столкновения сердца с платформами
        heart_rect = self.get_rect()
        for platform in platforms:
            if heart_rect.colliderect(platform.get_rect()):
                # Если произошло столкновение, сердце останавливается на платформе
                self.y = platform.y - heart_rect.height + 100
                self.falling = False
                break
