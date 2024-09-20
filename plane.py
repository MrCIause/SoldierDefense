import pygame
import os
import random
from heart import Heart

class Plane:
    def __init__(self, y):
        self.x = -100  # начальная позиция самолета
        self.y = y # начальная позиция самолета
        self.velocity = 5 # Скорость самолета

        # загрузка изображений самолета
        self.fly_images = [
            pygame.image.load(os.path.join('assets', 'images', 'PlaneFlying', 'FlyOne.png')),
            pygame.image.load(os.path.join('assets', 'images', 'PlaneFlying', 'FlyTWO.png'))
        ]

        # изменение размера изображений самолета
        self.fly_images = [pygame.transform.scale(img, (img.get_width() // 2, img.get_height() // 2)) for img in self.fly_images]

        self.current_image = 0 # текущее изображение самолета
        self.animation_time = 0.1 # Время между кадрами анимации в секундах
        self.current_time = 0 # текущее время
        self.heart_dropped = False # Падает ли сердце

        # Загрузка звука самолета
        self.fly_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'planeFly.mp3')) # Загрузка звука самолета
        self.fly_sound.set_volume(0.5)  # Установка громкости звука
        self.is_flying = False  # Летит ли самолет

    # Обновление позиции самолета и анимации полета самолета
    def update(self, dt): # dt - время прошедшее с последнего обновления
        self.current_time += dt # Увеличение текущего времени на dt секунд
        if self.current_time >= self.animation_time: # Если текущее время больше времени анимации
            self.current_time = 0 # Сброс текущего времени
            self.current_image = (self.current_image + 1) % len(self.fly_images) # Переключение изображения самолета

        self.x += self.velocity # Перемещение самолета вправо
        self.is_flying = True # Самолет летит

        if not self.heart_dropped and random.random() < 0.01: # Если сердце еще не упало и случайное число меньше 0.01
            self.heart_dropped = True # Сердце упало
            return Heart(self.x + self.fly_images[0].get_width() // 2, self.y + self.fly_images[0].get_height() // 2) # Вернуть сердце в позиции самолета и высоте самолета // 2
        return None

    # Отрисовка самолета на экране
    def draw(self, screen):  # screen - экран для отрисовки
        image = self.fly_images[self.current_image] # Получение текущего изображения самолета
        screen.blit(image, (self.x, self.y)) # Отрисовка самолета на экране

    # Возвращает прямоугольник, описывающий самолет, для проверки столкновений
    def off_screen(self, width): # width - ширина экрана
        return self.x > width # Возвращает True, если самолет за пределами экрана

    # Воспроизведение звука самолета при полете
    def start_flying_sound(self):  # Воспроизведение звука самолета при полете
        if not pygame.mixer.get_busy(): # Если звук не воспроизводится
            self.fly_sound.play(loops=-1) # Воспроизвести звук самолета бесконечно (loops=-1)

    # Остановка звука самолета при полете
    def stop_flying_sound(self): # Остановка звука самолета при полете
        self.fly_sound.stop() # Остановка звука самолета


