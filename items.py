import pygame.sprite
import consts

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type #0 = monedas // 1 = posiones
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, posicion_pantalla, personaje):
        self.rect.x += posicion_pantalla[0]
        self.rect.y += posicion_pantalla[1]
        #Colision Personaje/Items
        if self.rect.colliderect(personaje.shape):
            #Monedas
            if self.item_type == 0:
                personaje.score += 1
            #Posiones
            elif self.item_type == 1:
                personaje.energia += 20
                if personaje.energia > 100:
                    personaje.energia = 100
            self.kill()

        cd_animation = consts.COOLDOWN_ANIMATION_MONEDAS
        self.image = self.animation_list[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > cd_animation:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
