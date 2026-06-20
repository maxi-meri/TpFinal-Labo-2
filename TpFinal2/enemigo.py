import pygame
import math
import random

class Enemigo:

    def __init__(self, ancho, alto, ronda):

        self.x = 300
        self.y = 300

        tamaño = 25

        lado = random.choice(["arriba", "abajo", "izquierda", "derecha"])

        if lado == "arriba":
            self.x = random.randint(0, ancho)
            self.y = -tamaño
        elif lado == "abajo":
            self.x = random.randint(0, ancho)
            self.y = alto + tamaño
        elif lado == "izquierda":
            self.x = -tamaño
            self.y = random.randint(0, alto)
        else:
            self.x = ancho + tamaño
            self.y = random.randint(0, alto)

        self.radio = 25
        self.velocidad = 2 + (ronda * 0.5)
        self.vida = 1 + (ronda // 3)
        self.daño = 10 + (ronda * 2)

    def mover(self, jugador):

        dx = jugador.x - self.x
        dy = jugador.y - self.y

        distancia = math.hypot(dx, dy)

        if distancia != 0:
            dx = dx / distancia
            dy = dy / distancia

            self.x += dx * self.velocidad
            self.y += dy * self.velocidad

    def dibujar(self, pantalla):

        pygame.draw.circle(pantalla, (255, 0, 0), (self.x, self.y), self.radio)

    def recibir_daño(self, daño):

        self.vida -= daño
    
    def muerto(self):

        return self.vida <= 0