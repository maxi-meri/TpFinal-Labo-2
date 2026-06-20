import pygame

class Bala:

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.vel = 10
        self.radio = 5

    def mover(self):
        self.x += self.dx * self.vel
        self.y += self.dy * self.vel

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (255, 255, 0), (int(self.x), int(self.y)), self.radio)

    def fuera_pantalla(self, ancho, alto):
        return (
            self.x < 0
            or self.x > ancho
            or self.y < 0
            or self.y > alto
        )