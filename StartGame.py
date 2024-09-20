import pygame
import os
from settings import WIDTH, HEIGHT


class StartGame:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load(os.path.join('assets', 'images', 'enteranceImage.webp'))
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))  # Scale the image to fill the screen
        self.font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 50)
        self.button_color = (0, 255, 0)
        self.button_hover_color = (100, 255, 100)
        self.button_rect = pygame.Rect((WIDTH // 2 - 100, HEIGHT // 2 + 50), (200, 50))

    def draw(self):
        self.screen.blit(self.image, (0, 0))  # Blit the image to cover the entire screen

        mouse_pos = pygame.mouse.get_pos()
        button_color = self.button_hover_color if self.button_rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, button_color, self.button_rect)
        button_text = self.button_font.render("Start", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text, button_text_rect)

    def is_start_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            return True
        return False
