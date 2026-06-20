import pygame
import math
import consts

class BalaEnemigo(pygame.sprite.Sprite):

    def __init__(self, x, y, target_x, target_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 100, 0), (6, 6), 6)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        dx = target_x - x
        dy = target_y - y
        distancia = math.hypot(dx, dy)

        if distancia == 0:
            distancia = 1

        self.dx = dx / distancia
        self.dy = dy / distancia

        self.velocidad = 5
        self.daño = 10

    def update(self, posicion_pantalla, player, obstaculos_tiles):
        self.rect.x += posicion_pantalla[0]
        self.rect.y += posicion_pantalla[1]

        self.rect.x += self.dx * self.velocidad
        self.rect.y += self.dy * self.velocidad

        if self.rect.colliderect(player.shape):

            if player.escudo > 0:
                player.escudo -= self.daño

                if player.escudo < 0:
                    player.escudo = 0
            else:
                player.energia -= self.daño

            self.kill()

        for obs in obstaculos_tiles:
            if obs[1].colliderect(self.rect):
                self.kill()

        if (
            self.rect.right < 0
            or self.rect.left > consts.ANCHO_VENTANA
            or self.rect.bottom < 0
            or self.rect.top > consts.ALTO_VENTANA
        ):
            self.kill()