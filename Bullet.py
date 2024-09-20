import pygame


class Bullet:
    def __init__(self, x, y, direction):
        self.x = x # Позиция по оси X
        self.y = y # Позиция по оси Y
        self.direction = direction # Направление пули
        self.speed = 10  # Скорость пули
        self.image = pygame.Surface((10, 5)) # Создание поверхности для пули
        self.image.fill((0, 0, 0))  # Черная пуля
        self.rect = self.image.get_rect() # Получение прямоугольника изображения для проверки столкновений

    def update(self):
        self.x += self.direction * self.speed # Перемещение пули в направлении, указанном переменной direction

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y)) # Отрисовка пули на экране

    def get_rect(self):
        """Возвращает прямоугольник, описывающий пулю, для проверки столкновений"""
        rect = self.image.get_rect() # Получение прямоугольника изображения для проверки столкновений
        rect.topleft = (self.x, self.y) # Установка позиции прямоугольника пули на экране
        return rect
