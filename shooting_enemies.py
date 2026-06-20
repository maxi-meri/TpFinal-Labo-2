import pygame
import math
import consts
from character import Personaje
from bullet_enemies import BalaEnemigo


class EnemigoDisparo(Personaje):

    def __init__(self, x, y, animations, energia, tipo):
        super().__init__(x, y, animations, energia, tipo)

        self.rango_disparo = consts.RANGO_ENEMIGOS
        self.cooldown_disparo = consts.RANGO_DISPARO_ENEMIGOS
        self.ultimo_disparo = pygame.time.get_ticks()

    def enemigos(self, player, obstaculos_tiles, posicion_pantalla, exit_tile, grupo_balas_enemigas):
        clipped_lined = ()
        enemigos_delta_x = 0
        enemigos_delta_y = 0

        self.shape.x += posicion_pantalla[0]
        self.shape.y += posicion_pantalla[1]

        linea_vision = (
            (self.shape.centerx, self.shape.centery),
            (player.shape.centerx, player.shape.centery)
        )

        for obs in obstaculos_tiles:
            if obs[1].clipline(linea_vision):
                clipped_lined = obs[1].clipline(linea_vision)

        distancia = math.hypot(
            self.shape.centerx - player.shape.centerx,
            self.shape.centery - player.shape.centery
        )

        if not clipped_lined and distancia < consts.RANGO_ENEMIGOS:

            if distancia > self.rango_disparo:
                if self.shape.centerx > player.shape.centerx:
                    enemigos_delta_x = -consts.VELOCIDAD_ENEMIGOS
                if self.shape.centerx < player.shape.centerx:
                    enemigos_delta_x = consts.VELOCIDAD_ENEMIGOS
                if self.shape.centery > player.shape.centery:
                    enemigos_delta_y = -consts.VELOCIDAD_ENEMIGOS
                if self.shape.centery < player.shape.centery:
                    enemigos_delta_y = consts.VELOCIDAD_ENEMIGOS

            else:
                tiempo_actual = pygame.time.get_ticks()

                if tiempo_actual - self.ultimo_disparo >= self.cooldown_disparo:
                    bala = BalaEnemigo(
                        self.shape.centerx,
                        self.shape.centery,
                        player.shape.centerx,
                        player.shape.centery
                    )

                    grupo_balas_enemigas.add(bala)
                    self.ultimo_disparo = tiempo_actual

        self.movimiento(enemigos_delta_x, enemigos_delta_y, obstaculos_tiles, exit_tile)