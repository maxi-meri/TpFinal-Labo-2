import pygame
import consts
import math

class Personaje():
    def __init__(self, x, y, animations, energia, tipo):
        self.score = 0
        self.energia = energia
        self.vivo = True
        self.flip = False
        self.animations = animations
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animations[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.center = (x, y)
        self.tipo = tipo
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.exp = 0
        self.exp_max = 10
        self.nivel = 1
        self.daño = 40
        self.velocidad = consts.VELOCIDAD_PERSONAJE
        self.cooldown_disparo = consts.COOLDOWN_BULLETS
        self.escudo = 0


    def update(self):
        #Comprobar estado Personaje
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False

        #CD DMG
        hit_cd = 1000
        if self.tipo == 1:
            if self.hit == True:
                if pygame.time.get_ticks() - self.last_hit > hit_cd:
                    self.hit = False

        cooldown_animation = 100
        self.image = self.animations[self.frame_index]

        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animations):
            self.frame_index = 0

    def dibujo(self, interfaz):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(image_flip, self.shape)
        #pygame.draw.rect(interfaz, consts.COLOR_PERSONAJE, self.shape, 1)

    def actualizar_coordenadas(self, tupla):
        self.shape.center = (tupla[0], tupla[1])

    def movimiento(self, delta_x, delta_y, obstaculos_tiles, exit_tile):
        posicion_pantalla = [0, 0]
        nivel_completado = False
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        
        self.shape.x = self.shape.x + delta_x
        #Colision eje x
        for obstaculo in obstaculos_tiles:
            if obstaculo[1].colliderect(self.shape):
                if delta_x > 0:
                    self.shape.right = obstaculo[1].left
                if delta_x < 0:
                    self.shape.left = obstaculo[1].right

        self.shape.y = self.shape.y + delta_y
        #Colision eje y
        for obstaculo in obstaculos_tiles:
            if obstaculo[1].colliderect(self.shape):
                if delta_y > 0:
                    self.shape.bottom = obstaculo[1].top
                if delta_y < 0:
                    self.shape.top = obstaculo[1].bottom

        #Camara
        if self.tipo == 1:
            #Salida
            if exit_tile[1].colliderect(self.shape):
                nivel_completado = True
                print("Nivel Completado")

            if self.shape.right > (consts.ANCHO_VENTANA - consts.LIMITE_PANTALLA):
                posicion_pantalla[0] = (consts.ANCHO_VENTANA - consts.LIMITE_PANTALLA) - self.shape.right
                self.shape.right = consts.ANCHO_VENTANA - consts.LIMITE_PANTALLA
            if self.shape.left < consts.LIMITE_PANTALLA:
                posicion_pantalla[0] = consts.LIMITE_PANTALLA - self.shape.left
                self.shape.left =consts.LIMITE_PANTALLA
        
            if self.shape.bottom > (consts.ALTO_VENTANA - consts.LIMITE_PANTALLA):
                posicion_pantalla[1] = (consts.ALTO_VENTANA - consts.LIMITE_PANTALLA) - self.shape.bottom
                self.shape.bottom = consts.ALTO_VENTANA - consts.LIMITE_PANTALLA
            if self.shape.top < consts.LIMITE_PANTALLA:
                posicion_pantalla[1] = consts.LIMITE_PANTALLA - self.shape.top
                self.shape.top =consts.LIMITE_PANTALLA
            return posicion_pantalla, nivel_completado
        
    def enemigos(self, player, obstaculos_tiles, posicion_pantalla, exit_tile):
        clipped_lined = ()
        enemigos_delta_x = 0
        enemigos_delta_y = 0
        self.shape.x += posicion_pantalla[0]
        self.shape.y += posicion_pantalla[1]

        #Rango de vision
        linea_vision = ((self.shape.centerx, self.shape.centery), (player.shape.centerx, player.shape.centery))
        for obs in obstaculos_tiles:
            if obs[1].clipline(linea_vision):
                clipped_lined = obs[1].clipline(linea_vision)

        #Agro
        agro = math.sqrt(((self.shape.centerx - player.shape.centerx) ** 2) + ((self.shape.centery - player.shape.centery) ** 2))
        if not clipped_lined and agro < consts.RANGO_ENEMIGOS:
            #Seguimiento Jugador
            if self.shape.centerx > player.shape.centerx:
                enemigos_delta_x = -consts.VELOCIDAD_ENEMIGOS
            if self.shape.centerx < player.shape.centerx:
                enemigos_delta_x = consts.VELOCIDAD_ENEMIGOS
            if self.shape.centery > player.shape.centery:
                enemigos_delta_y = -consts.VELOCIDAD_ENEMIGOS
            if self.shape.centery < player.shape.centery:
                enemigos_delta_y = consts.VELOCIDAD_ENEMIGOS
        self.movimiento(enemigos_delta_x, enemigos_delta_y, obstaculos_tiles, exit_tile)

        #Ataque
        if agro < consts.ATK_RANGE and player.hit == False:
            if player.escudo > 0:
                player.escudo -= 10

                if player.escudo < 0:
                    player.escudo = 0
            else:
                player.energia -= 10
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
