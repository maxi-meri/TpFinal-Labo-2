import pygame

class Escudo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio = 10

    def dibujar(self, pantalla):

        pygame.draw.circle(pantalla, (0, 200, 255), (int(self.x), int(self.y)), self.radio)