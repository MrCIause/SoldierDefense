# map.py
import pygame
import os
from settings import WIDTH, HEIGHT
from game_platform import GamePlatform


class GameMap:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load(os.path.join('assets', 'images', 'background.png'))
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.platform_height = 125
        self.ground = GamePlatform(0, HEIGHT - self.platform_height, WIDTH + 10, self.platform_height)
        self.bg_x = 0  # Позиция фона по оси X

        # List of all platforms
        self.platforms = [self.ground]

    def update(self, player_x):
        self.bg_x = -(player_x % WIDTH)  # Позиция фона зависит от позиции игрока

    def draw(self):
        # Отрисовка фона
        self.screen.blit(self.background, (self.bg_x, 0))
        self.screen.blit(self.background, (self.bg_x + WIDTH, 0))

        # Отрисовка платформы (земли)
        for platform in self.platforms:
            platform.draw(self.screen)
