import pygame
import math

class Jugador:

    def __init__(self):
        
        self.image = pygame.image.load("001.png")
        self.image = pygame.transform.scale(self.image, (100, 80))

        self.x = 100
        self.y = 100
        
        self.daño = 1
        self.velocidad = 5
        self.vida = 100
        self.escudos = 0

        self.nivel = 1
        self.exp = 0
        self.exp_max = 10

    def mover(self, teclas, ancho, alto):
  
        if teclas[pygame.K_w]:
            self.y -= self.velocidad
        if teclas[pygame.K_s]:
            self.y += self.velocidad

        if teclas[pygame.K_a]:
            self.x -= self.velocidad
        if teclas[pygame.K_d]:
            self.x += self.velocidad

        if self.x < 0:
            self.x = 0
        if self.x > ancho - 100:
            self.x = ancho - 100

        if self.y < 0:
            self.y = 0
        if self.y > alto - 80:
            self.y = alto - 80
    
    def dibujar(self, ventana):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - (self.x + 50)
        dy = mouse_y - (self.y + 40)

        angulo = math.degrees(math.atan2(-dy, dx))
        jugador_rotado = pygame.transform.rotate(self.image, angulo)

        rect = jugador_rotado.get_rect(center=(self.x + 50, self.y +  40))

        ventana.blit(jugador_rotado, rect)