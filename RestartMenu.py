import pygame
import os
from settings import WIDTH, HEIGHT

class RestartMenu:
    def __init__(self, screen, wave_number):
        self.screen = screen
        self.wave_number = wave_number
        self.image = pygame.image.load(os.path.join('assets', 'images', 'enteranceImage.webp'))
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))  # Scale the image to fill the screen
        self.font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 50)
        self.button_color = (255, 0, 0)
        self.button_hover_color = (255, 100, 100)
        self.button_rect = pygame.Rect((WIDTH // 2 - 100, HEIGHT // 2 + 50), (200, 50))
        self.image = pygame.transform.flip(self.image, True, False)


    def draw(self):
        self.screen.blit(self.image, (0, 0))  # Blit the image to cover the entire screen
        text = self.font.render(f"Wave Survived: {self.wave_number}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)

        mouse_pos = pygame.mouse.get_pos()
        button_color = self.button_hover_color if self.button_rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, button_color, self.button_rect)
        button_text = self.button_font.render("Restart", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text, button_text_rect)

    def is_restart_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            return True
        return False
