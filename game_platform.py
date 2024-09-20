import pygame
import os


class GamePlatform:
    def __init__(self, x, y, width, height):
        self.x = x # Позиция по оси X
        self.y = y # Позиция по оси Y
        self.width = width # Ширина
        self.height = height # Высота
        self.image = pygame.image.load(os.path.join('assets', 'images', 'ground.png'))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen): # Отрисовка платформы
        screen.blit(self.image, (self.x, self.y)) # Отрисовка платформы на экране

    def get_rect(self): # Возвращает прямоугольник, описывающий платформу, для проверки столкновений
        return pygame.Rect(self.x, self.y, self.width, self.height) # Возвращает прямоугольник платформы
