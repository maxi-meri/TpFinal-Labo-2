import pygame
import math
import random

class EnemigoDisparo:
    def __init__(self, ancho, alto, ronda):

        tamaño = 25
        lado = random.choice(["arriba", "abajo", "izquierda", "derecha"])

        if lado == "arriba":
            self.x  = random.randint(0, ancho)
            self.y = -tamaño
        elif lado == "abajo":
            self.x = random.randint(0, ancho)
            self.y = alto + tamaño
        elif lado == "izquierda":
            self.x = -tamaño
            self.y = random.randint(0, alto)
        elif lado == "derecha":
            self.x = ancho + tamaño
            self.y = random.randint(0, alto)

        self.radio = 20
        self.velocidad = 1.5
        self.vida = 2 + ronda
        self.daño = 5 + ronda
        self.rango_disparo = 250

        self.cooldown_disparo = 90
        self.timer_disparo = 0


    def mover(self, jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y

        distancia = math.hypot(dx, dy)

        if distancia > self.rango_disparo:
            dx /= distancia
            dy /= distancia

            self.x += dx * self.velocidad
            self.y += dy * self.velocidad

    def disparar(self, jugador):
        self.timer_disparo += 1

        dx = jugador.x - self.x
        dy = jugador.y - self.y

        distancia = math.hypot(dx, dy)
        if distancia <= self.rango_disparo:
            if self.timer_disparo >= self.cooldown_disparo:
                self.timer_disparo = 0 
                
                dx /= distancia
                dy /= distancia

                return (self.x, self.y, dx, dy)
        return None    

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (0, 0, 255), (int(self.x), int(self.y)), self.radio)

    def recibir_daño(self, daño):
        self.vida -= daño
    
    def muerto(self):
        return self.vida <= 0