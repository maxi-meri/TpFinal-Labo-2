import consts
import pygame
from items import Item
from character import Personaje

obstaculos = [16, 17, 18, 31, 32, 33, 35, 46, 47, 48, 140, 163, 178]
puerta_cerrada = [163, 178]
trampas = [166, 167, 211, 212, 213, 214, 215, 216, 232, 233, 234, 235, 236, 237]

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstaculos_tiles = []
        self.exit_tile = None
        self.lista_item = []
        self.lista_enemigos = []
        self.puerta_cerrada_tile = []
        self.trampas_tiles = []
        self.final_tile = None
    
    def process_data(self, data, tiles_list, item_imgs, animations_enemies):
        self.level_length = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tiles_list[tile]
                image_rect = image.get_rect()
                image_x = x * consts.TILE_SIZE
                image_y = y * consts.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y, tile]
                #Bounds
                if tile in obstaculos:
                    self.obstaculos_tiles.append(tile_data)
                #Trampas
                if tile in trampas:
                    self.trampas_tiles.append(tile_data)
                #Puerta
                if tile in puerta_cerrada:
                    self.puerta_cerrada_tile.append(tile_data)
                #Salida
                elif tile == 155:
                    self.exit_tile = tile_data
                #Easter Egg
                elif tile == 55:
                    self.final_tile = tile_data
                #Coins
                elif tile == 190:
                    coin = Item(image_x, image_y, 0, item_imgs[0])
                    self.lista_item.append(coin)
                    tile_data[0] = tiles_list[116]
                #Posiones
                elif tile == 191:
                    potion = Item(image_x, image_y, 1, item_imgs[1])
                    self.lista_item.append(potion)
                    tile_data[0] = tiles_list[116]
                #Hongo
                elif tile == 200:
                    hongo = Personaje(image_x, image_y, animations_enemies[1], 200, 2)
                    self.lista_enemigos.append(hongo)
                    tile_data[0] = tiles_list[116]
                #Goblin
                elif tile == 188:
                    goblin = Personaje(image_x, image_y, animations_enemies[0], 300, 2)
                    self.lista_enemigos.append(goblin)
                    tile_data[0] = tiles_list[116]
                self.map_tiles.append(tile_data)

    def abrir_puerta(self, player, tile_list):
        buffer = 50
        proximidad_rect = pygame.Rect(player.shape.x - buffer, player.shape.y - buffer, player.shape.width + 2 * buffer, player.shape.height + 2 * buffer)
        for tile_data in self.map_tiles:
            image, rect, x, y, tile_type = tile_data
            if proximidad_rect.colliderect(rect):
                if tile_type in puerta_cerrada:
                    if tile_type == 163 or tile_type == 178:
                        new_tile_type = 162
                    elif tile_type == 163 or tile_type == 178:
                        new_tile_type = 177

                    tile_data[-1] = new_tile_type
                    tile_data[0] = tile_list[new_tile_type]

                    if tile_data in self.obstaculos_tiles:
                        self.obstaculos_tiles.remove(tile_data)
                    return True
        return False     

    def tocar_trampa(self, player):
        for tile in self.trampas_tiles:
            if player.shape.colliderect(tile[1]):
                player.energia = 0
                player.vivo = False
                return True
        return False

    def update(self, posicion_pantalla):
        for tile in self.map_tiles:
            tile[2] += posicion_pantalla[0]
            tile[3] += posicion_pantalla[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
