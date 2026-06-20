import pygame
import consts
import math
import random

class Weapon():
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.shape = self.imagen.get_rect()
        self.shoot = False
        self.last_shoot = pygame.time.get_ticks()

    def update(self, personaje):
        cooldown= personaje.cooldown_disparo
        bala = None
        self.shape.center = personaje.shape.center
        if personaje.flip == False:
            self.shape.x = self.shape.x + personaje.shape.width / 2
            self.rotar_arma(False)
        if personaje.flip == True:
            self.shape.x = self.shape.x - personaje.shape.width / 2
            self.rotar_arma(True)

        #Angulo de la Pistola con el Mouse
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.shape.centerx
        distancia_y = -(mouse_pos[1] - self.shape.centery)
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))

        #Detectar Click Mouse
        if pygame.mouse.get_pressed()[0] and self.shoot == False and (pygame.time.get_ticks() - self.last_shoot >= cooldown):
            bala = Bullet(self.imagen_bala, self.shape.centerx, self.shape.centery, self.angulo, personaje.daño)
            self.shoot = True
            self.last_shoot = pygame.time.get_ticks()

            #reset click
        if pygame.mouse.get_pressed()[0] == False:
            self.shoot = False
        return bala

    def dibujo(self, interfaz):
        self.imagen = pygame.transform.rotate(self.imagen, self.angulo)
        interfaz.blit(self.imagen, self.shape)
        #pygame.draw.rect(interfaz, consts.COLOR_ARMA, self.shape, 1)
    
    def rotar_arma(self, rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.imagen_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.imagen_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle, daño):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.daño = daño

        #Velocidad Bala
        self.delta_x = math.cos(math.radians(self.angle)) * consts.VELOCIDAD_BULLET
        self.delta_y = -math.sin(math.radians(self.angle)) * consts.VELOCIDAD_BULLET

    def update(self, lista_enemigos, obstaculos_tiles):
        dmg = 0
        pos_dmg = None
        self.rect.x = self.rect.x + self.delta_x
        self.rect.y = self.rect.y + self.delta_y

        #Borrar balas fuera de pantalla
        if self.rect.right < 0 or self.rect.left > consts.ANCHO_VENTANA or self.rect.bottom < 0 or self.rect.top > consts.ALTO_VENTANA:
            self.kill()
        
        #Colision Enemigos
        for enemigo in lista_enemigos:
            if enemigo.shape.colliderect(self.rect):
                dmg = self.daño + random.randint(-7, 7)
                pos_dmg = enemigo.shape
                enemigo.energia = enemigo.energia - dmg
                self.kill()
                break
        
        #Colision Paredes
        for obs in obstaculos_tiles:
            if obs[1].colliderect(self.rect):
                self.kill()
                break
        return dmg, pos_dmg

    def dibujo(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery - int(self.image.get_height())))
