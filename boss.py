import pygame
import random
from character import Personaje


class FinalBoss(Personaje):
    def __init__(self, x, y, animations):
        super().__init__(x, y, animations, 2000, 2)
        self.ataque = 100

        # Fase 2
        self.fase2 = False

        # Evento de invocación
        self.invocacion_realizada = False

        # Disparos
        self.cooldown_disparo = 1000
        self.ultimo_disparo = pygame.time.get_ticks()
    
    
    def comprobar_fase(self, lista_enemigos, animations_enemies):

        if self.energia <= 1000 and not self.invocacion_realizada:

            self.fase2 = True
            self.invocacion_realizada = True

            self.invocar_enemigos(lista_enemigos, animations_enemies)


    def es_fase2(self):
        return self.fase2


    def invocar_enemigos(self, lista_enemigos, animations_enemies):
        for i in range(15):

            x = random.randint(100, 700)
            y = random.randint(100, 500)

            if random.randint(1, 100) <= 50:
                enemigo = Personaje(x, y, animations_enemies[0], 50, 2)
            else:
                enemigo = Personaje(x, y, animations_enemies[1], 40, 2)

            lista_enemigos.append(enemigo)

    def disparar(self, player):
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_disparo >= self.cooldown_disparo:

            self.ultimo_disparo = tiempo_actual

            return EnemyBullet(self.shape.centerx, self.shape.centery, player)

        return None

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()

        self.image = pygame.Surface((12, 12))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        dx = player.shape.centerx - x
        dy = player.shape.centery - y

        distancia = (dx**2 + dy**2)**0.5

        if distancia != 0:
            dx /= distancia
            dy /= distancia

        velocidad = 6

        self.vel_x = dx * velocidad
        self.vel_y = dy * velocidad


    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

