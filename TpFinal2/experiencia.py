import pygame

class Experiencia:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio = 15

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (0, 255, 0), (int(self.x), int(self.y)), self.radio)