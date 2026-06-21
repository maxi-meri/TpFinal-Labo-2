import pygame
import consts
import os
import csv
import random

from character import Personaje
from weapons import Weapon
from textos import DamageText
from items import Item
from world import World
from shooting_enemies import EnemigoDisparo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ruta(*partes):
    return os.path.join(BASE_DIR, *partes)

#Funciones
#Escalar Imagenes
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w * scale, h * scale))
    return nueva_imagen

#Contar Elementos
def contar_elementos(directorio):
    return len(os.listdir(directorio))

#Listar Nombres Elementos
def nombre_carpetas(directorio):
    return os.listdir(directorio)


pygame.init()
window = pygame.display.set_mode((consts.ANCHO_VENTANA, consts.ALTO_VENTANA))
pygame.display.set_caption("Mi primer juego")

posicion_pantalla = [0, 0]
nivel = 1

#rondas
ronda = 1
MAX_RONDAS = 10
salida_desbloqueada = False
ronda_terminada = False

#Fonts
font = pygame.font.Font(ruta("assets", "fonts", "Minecraft.ttf"), consts.FONT_SIZE)
font_game_over = pygame.font.Font(ruta("assets", "fonts", "BLOODY.TTF"), consts.FONT_SIZE * 3)
font_reinicio = pygame.font.Font(ruta("assets", "fonts", "Minecraft.ttf"), consts.FONT_SIZE)

game_over_text = font_game_over.render("Game Over", True, consts.BLANCO)
texto_boton_reinicio = font_reinicio.render("Reiniciar", True, consts.NEGRO)

#Importar Imgs
#Energia
corazon_vacio = pygame.image.load(ruta("assets", "images", "items", "hp_empty.png"))
corazon_vacio = escalar_img(corazon_vacio, consts.ESCALA_CORAZONES)
corazon_mitad = pygame.image.load(ruta("assets", "images", "items", "hp_half.png"))
corazon_mitad = escalar_img(corazon_mitad, consts.ESCALA_CORAZONES)
corazon_full = pygame.image.load(ruta("assets", "images", "items", "hp_full.png"))
corazon_full = escalar_img(corazon_full, consts.ESCALA_CORAZONES)

#Personaje
animations = []
for i in range(7):
    img = pygame.image.load(ruta("assets", "images", "characters", "player", f"Player_{i}.png")).convert_alpha()
    img = escalar_img(img, consts.ESCALA_PERSONAJE)
    animations.append(img)

#Enemigos
directorio_enemigos = ruta("assets", "images", "characters", "enemies")
tipo_enemigos = nombre_carpetas(directorio_enemigos)
animations_enemies = []

for enemies in tipo_enemigos:
    list_temp = []
    ruta_temp = ruta("assets", "images", "characters", "enemies", enemies)
    num_animations = contar_elementos(ruta_temp)
    
    for i in range(num_animations):
        img_enemigo = pygame.image.load(ruta_temp + f"/{enemies}_{i}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo, consts.ESCALA_ENEMIGOS)
        list_temp.append(img_enemigo)
    animations_enemies.append(list_temp)


#Arma
imagen_pistola = pygame.image.load(ruta("assets", "images", "weapons", "gun.png")).convert_alpha()
imagen_pistola = escalar_img(imagen_pistola, consts.ESCALA_ARMA)

#Balas
imagen_balas = pygame.image.load(
    ruta("assets", "images", "weapons", "bullet.png")
).convert_alpha()
imagen_balas = escalar_img(imagen_balas, consts.ESCALA_ARMA)

#BG
tile_list = []
for x in range(270):#270
    tile_image = pygame.image.load(ruta("assets", "images", "tiles", f"tile ({x + 1}).png"))
    tile_image = pygame.transform.scale(tile_image, (consts.TILE_SIZE, consts.TILE_SIZE))
    tile_list.append(tile_image)

#Items
#Posion
imagen_posion = pygame.image.load(ruta("assets", "images", "items", "potion.png"))
imagen_posion = escalar_img(imagen_posion, consts.ESCALA_POSION)
#Monedas
coin_images = []
ruta_img = ruta("assets", "images", "items", "coin")
num_coin_img = contar_elementos(ruta_img)
for i in range(num_coin_img):
    img = pygame.image.load(ruta("assets", "images", "items", "coin", f"coin_{i}.png"))
    img = escalar_img(img, consts.ESCALA_MONEDAS)
    coin_images.append(img)

items_imgs = [coin_images, [imagen_posion]]

#Texto pantalla
def dibujar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    window.blit(img, (x, y))

def dibujar_barra(x, y, ancho, alto, valor, maximo, color, texto):
    porcentaje = valor / maximo

    if porcentaje > 1:
        porcentaje = 1
    if porcentaje < 0:
        porcentaje = 0

    fondo = pygame.Rect(x, y, ancho, alto)
    relleno = pygame.Rect(x, y, ancho * porcentaje, alto)

    pygame.draw.rect(window, (30, 30, 30), fondo, border_radius=10)
    pygame.draw.rect(window, color, relleno, border_radius=10)
    pygame.draw.rect(window, consts.BLANCO, fondo, 2, border_radius=10)

#Energia/Vida
def vida_player():
    c_mitad_dibujado = False
    for i in range(5):
        if player.energia >= ((i + 1) * 20):
            window.blit(corazon_full, (5 + i * 50, 5))
        elif player.energia % 20 > 0 and c_mitad_dibujado == False:
            window.blit(corazon_mitad, (5 + i * 50, 5))
            c_mitad_dibujado = True
        else:
            window.blit(corazon_vacio, (5 + i * 50, 5))

def resetear_mundo():
    grupo_dmg_text.empty()
    grupo_balas.empty()
    grupo_items.empty()

    data = []
    for fila in range(consts.FILAS):
        filas = [2] * consts.COLUMNAS
        data.append(filas)
    return data

world_data = []

#Carga de emergencia en caso de que falten tiles en el mapa <----- No funciona arreglar
for fila in range(consts.FILAS):
    filas = [1] * consts.COLUMNAS
    world_data.append(filas)

#Carga de nivel
with open(ruta("niveles", "nivel_1.csv"), newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_data[x][y] = int(columna)

world = World()
world.process_data(world_data, tile_list, items_imgs, animations_enemies)

#Grid
def dibujar_grid():
    for x in range(30):
        pygame.draw.line(window, consts.BLANCO, (x * consts.TILE_SIZE, 0), (x * consts.TILE_SIZE, consts.ALTO_VENTANA))
        pygame.draw.line(window, consts.BLANCO, (0, x * consts.TILE_SIZE), (consts.ANCHO_VENTANA, x * consts.TILE_SIZE))

#Jugador Clase Personaje
player = Personaje(450, 350, animations, consts.ENERGIA_PERSONAJE, 1)

#Enemigos Clase Personaje
#Creacion Manual
# goblin = Personaje(400, 300, animations_enemies[0], consts.ENERGIA_ENEMIGOS, 2)
# shroom = Personaje(200, 200, animations_enemies[1], consts.ENERGIA_ENEMIGOS, 2)
# goblin_2 = Personaje(100, 200, animations_enemies[0], consts.ENERGIA_ENEMIGOS, 2)
#Lista de enemigos
lista_enemigos = []
for enemies in world.lista_enemigos:
    lista_enemigos.append(enemies)
# lista_enemigos.append(goblin)
# lista_enemigos.append(goblin_2)
# lista_enemigos.append(shroom)

#Arma Clase Weapon
pistola = Weapon(imagen_pistola, imagen_balas)

#Grupo Sprites
grupo_balas = pygame.sprite.Group()
grupo_dmg_text = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()
grupo_balas_enemigas = pygame.sprite.Group()
#Items desde la data del nivel
for item in world.lista_item:
    grupo_items.add(item)

#Items Clase Items
#Manual
# moneda = Item(350, 25, 0, coin_images)
# posion = Item(370, 55, 1, [imagen_posion])
# grupo_items.add(moneda)
# grupo_items.add(posion)


#Variables Movimiento Jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

#Control Frame Rates
reloj = pygame.time.Clock()


boton_reinicio = pygame.Rect(consts.ANCHO_VENTANA / 2 - 100, consts.ALTO_VENTANA / 2 + 100, 200, 50)

estado = "jugando"

def carga_mapa(numero_nivel):
    global world, world_data, lista_enemigos, posicion_pantalla

    grupo_balas.empty()
    grupo_balas_enemigas.empty()
    grupo_dmg_text.empty()
    grupo_items.empty()

    posicion_pantalla = [0, 0]
    world_data = resetear_mundo()

    with open(ruta("niveles", f"nivel_{numero_nivel}.csv"), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, fila in enumerate(reader):
            for y, columna in enumerate(fila):
                world_data[x][y] = int(columna)

    world = World()
    world.process_data(world_data, tile_list, items_imgs, animations_enemies)

    player.actualizar_coordenadas(consts.COORDENADAS[str(numero_nivel)])

    lista_enemigos = []
    
    for item in world.lista_item:
        grupo_items.add(item)

#cantidad de enemigos
def enemigos_ronda(ronda):
    return 7 + (ronda - 1) * 3

spawn_por_nivel = {
    1: [
        (658, 370), (628, 72), (680, 460),
        (125, 417), (273, 186), (301, 81),
        (75, 278), (340, 118), (323, 200),
        (722, 201), (230, 198)
    ],

    2: [
        (378, 123), (556, 135), (581, 454),
        (172, 305), (595, 334), (102, 312),
        (119, 443), (353, 339), (389, 232),
        (194, 161), (636, 166), (745, 178),
        (327, 124), (504, 143), (694, 448)
    ],

    3: [
        (120, 300), (130, 430), (220, 430),
        (500, 180), (620, 180), (700, 250),
        (520, 420), (650, 420), (720, 380)
    ],

    4: [
        (250, 200), (450, 200), (650, 200),
        (250, 400), (450, 400), (650, 400)
    ]
}
#generacion de enemigos
def generar_enemigos_ronda(cantidad):
    zonas = spawn_por_nivel[nivel]
    enemigos_creados = 0
    intentos = 0

    while enemigos_creados < cantidad and intentos < cantidad * 50:
        intentos += 1

        x, y = zonas[intentos % len(zonas)]

        x += random.randint(-10, 10)
        y += random.randint(-10, 10)

        # evitar que aparezcan cerca del jugador
        distancia_jugador = ((x - player.shape.centerx) ** 2 + (y - player.shape.centery) ** 2) ** 0.5
        if distancia_jugador < 180:
            continue

        # evitar paredes
        rect_spawn = pygame.Rect(x - 20, y - 20, 40, 40)

        colisiona = False
        for obstaculo in world.obstaculos_tiles:
            if rect_spawn.colliderect(obstaculo[1]):
                colisiona = True
                break

        if colisiona:
            continue

        numero = random.randint(1, 100)

        if numero <= 66:
            enemigo = Personaje(x, y, animations_enemies[0], 100 + ronda * 20, 2)
        else:
            enemigo = EnemigoDisparo(x, y, animations_enemies[1], 80 + ronda * 15, 3)

        lista_enemigos.append(enemigo)
        enemigos_creados += 1

run = True
while run:
    #FPS
    reloj.tick(consts.FPS)

    #Control Frame Rates
    reloj = pygame.time.Clock()

    window.fill(consts.BLUE)

    if player.vivo and estado == "jugando": 
            
        #dibujar_grid()

        #Calculo Movimiento Jugador
        delta_x = 0
        delta_y = 0

        if mover_derecha == True:
            delta_x = player.velocidad
        if mover_izquierda == True:
            delta_x = -player.velocidad
        if mover_arriba == True:
            delta_y = -player.velocidad
        if mover_abajo == True:
            delta_y = player.velocidad


        #BG
        world.draw(window)
        world.update(posicion_pantalla)

        #Corazones
        vida_player()

        #Jugador
        posicion_pantalla, nivel_completado = player.movimiento(delta_x, delta_y, world.obstaculos_tiles, world.exit_tile)
        player.update()
        player.dibujo(window)

        #Enemigos
        for enemies in lista_enemigos[:]:
            if enemies.energia <= 0:
                player.exp += 1
                if random.randint(1, 100) <= 10:
                    escudo = Item(enemies.shape.centerx, enemies.shape.centery, 2, [])
                    grupo_items.add(escudo)

                lista_enemigos.remove(enemies)
            if enemies.energia > 0:

                if isinstance(enemies, EnemigoDisparo):
                    enemies.enemigos(player, world.obstaculos_tiles, posicion_pantalla, world.exit_tile, grupo_balas_enemigas)
                else:
                    enemies.enemigos(player, world.obstaculos_tiles, posicion_pantalla, world.exit_tile)

                enemies.update()
                enemies.dibujo(window)

        #rondas
        if len(lista_enemigos) == 0 and ronda_terminada == False:
            ronda_terminada = True
            estado = "ronda_completada"
            print(f"Ronda {ronda} completada")

        if player.exp >= player.exp_max:
            estado = "level_up"
        
        #Arma
        bala = pistola.update(player)
        pistola.dibujo(window)

        if bala:
            grupo_balas.add(bala)
        
        for bala in grupo_balas:
            bala.dibujo(window)
            dmg, pos_dmg = bala.update(lista_enemigos, world.obstaculos_tiles)
            if dmg:
                dmg_txt = DamageText(pos_dmg.centerx, pos_dmg.centery, str(dmg), font, consts.COLOR_FONT_DMG)
                grupo_dmg_text.add(dmg_txt)

        grupo_balas_enemigas.update(posicion_pantalla, player, world.obstaculos_tiles)
        grupo_balas_enemigas.draw(window)
        
        #Txt
        grupo_dmg_text.update(posicion_pantalla)
        grupo_dmg_text.draw(window)
        dibujar_texto(f"Score : {player.score}", font, consts.COLOR_TEXTO_SCORE, 690, 5)
        dibujar_texto(f"Sala: " + str(nivel), font, consts.BLANCO, consts.ANCHO_VENTANA / 2, 5)
        dibujar_texto(f"lvl: {player.nivel}", font, consts.BLANCO, 10, 28)

        dibujar_barra(10, 50, 220, 24, player.exp, player.exp_max, (0, 200, 80), f"EXP {player.exp}/{player.exp_max}")
        dibujar_barra(10, 85, 220, 24, player.escudo, 100, (0, 150, 255), f"ESCUDO {player.escudo}/100")

        #Items
        grupo_items.update(posicion_pantalla, player)
        grupo_items.draw(window)

    #Nivel completo
    if nivel_completado == True and salida_desbloqueada == True:
        if nivel < consts.MAX_LVL:
            nivel += 1
            carga_mapa(nivel)

            salida_desbloqueada = False
            nivel_completado = False

            cantidad = enemigos_ronda(ronda)
            generar_enemigos_ronda(ronda)

            ronda_terminada = False

            print(f"Cambiando al nivel {nivel}")
            print("enemigos generados:", len(lista_enemigos))

    if estado == "level_up":
        world.draw(window)
        vida_player()
        player.dibujo(window)
        grupo_items.draw(window)

        overlay_fondo = pygame.Surface((consts.ANCHO_VENTANA, consts.ALTO_VENTANA), pygame.SRCALPHA)
        overlay_fondo.fill((0, 0, 0, 130))
        window.blit(overlay_fondo, (0, 0))

        overlay = pygame.Surface((500, 400), pygame.SRCALPHA)
        overlay.fill((40, 40, 40, 180))
        window.blit(overlay, (150, 100))

        titulo = font.render("Subiste de Nivel", True, consts.BLANCO)

        op1 = font.render("1 - +1 Corazon", True, consts.BLANCO)
        op2 = font.render("2 - +5 de Daño", True, consts.BLANCO)
        op3 = font.render("3 - +1 de Velocidad", True, consts.BLANCO)
        op4 = font.render("4 - +Vel. Ataque", True, consts.BLANCO)

        window.blit(titulo, (260, 140))
        window.blit(op1, (250, 220))
        window.blit(op2, (250, 280))
        window.blit(op3, (250, 340))
        window.blit(op4, (250, 400))

    if estado == "ronda_completada":
        world.draw(window)
        vida_player()
        player.dibujo(window)
        grupo_items.draw(window)

        # Capa oscura transparente
        overlay = pygame.Surface((consts.ANCHO_VENTANA, consts.ALTO_VENTANA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        window.blit(overlay, (0, 0))

        # Panel transparente
        panel = pygame.Surface((520, 230), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 180))
        panel_rect = panel.get_rect(center=(consts.ANCHO_VENTANA // 2, consts.ALTO_VENTANA // 2))
        window.blit(panel, panel_rect)

        txt1 = font.render("Ronda Completada", True, consts.BLANCO)
        txt2 = font.render("Enter para continuar", True, consts.BLANCO)

        txt1_rect = txt1.get_rect(center=(consts.ANCHO_VENTANA // 2, consts.ALTO_VENTANA // 2 - 40))
        txt2_rect = txt2.get_rect(center=(consts.ANCHO_VENTANA // 2, consts.ALTO_VENTANA // 2 + 35))

        window.blit(txt1, txt1_rect)
        window.blit(txt2, txt2_rect)
    
    if estado == "victoria":
        window.fill((20, 20, 20))

        texto_victoria = font_game_over.render("GANASTE", True, consts.AMARILLO)
        texto_reinicio = font.render("R = Reiniciar", True, consts.BLANCO)
        texto_salir = font.render("ESC = Salir", True, consts.BLANCO)

        rect_victoria = texto_victoria.get_rect(center=(consts.ANCHO_VENTANA // 2, consts.ALTO_VENTANA // 2 - 80))

        window.blit(texto_victoria, rect_victoria)
        window.blit(texto_reinicio, (consts.ANCHO_VENTANA // 2 - 90, 330))
        window.blit(texto_salir, (consts.ANCHO_VENTANA // 2 - 70, 370))

    if player.vivo == False:
        window.fill(consts.ROJO_OSURO)
        text_rect = game_over_text.get_rect(center=(consts.ANCHO_VENTANA/2, consts.ALTO_VENTANA/2))
        window.blit(game_over_text, text_rect)

        pygame.draw.rect(window, consts.AMARILLO, boton_reinicio)
        window.blit(texto_boton_reinicio, (boton_reinicio.x + 50, boton_reinicio.y + 10))

    for event in pygame.event.get():

        #Cerrar Juego
        if event.type == pygame.QUIT:
            run = False

        #Controles Movimiento Jugador 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True

            if estado == "level_up":

                mejora_elegida = False

                if event.key == pygame.K_1:
                    player.energia += 25
                    mejora_elegida = True
                elif event.key == pygame.K_2:
                    player.daño += 5
                    mejora_elegida = True
                elif event.key == pygame.K_3:
                    player.velocidad += 1
                    mejora_elegida = True
                elif event.key == pygame.K_4:
                    player.cooldown_disparo -= 50
                    if player.cooldown_disparo < 100:
                        player.cooldown_disparo = 100
                    mejora_elegida = True

                if mejora_elegida:
                    player.nivel += 1
                    player.exp = 0
                    player.exp_max += 5
                    estado = "jugando"

            if estado == "victoria":
                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_r:
                    player = Personaje(160, 160, animations, consts.ENERGIA_PERSONAJE, 1)
                    pistola = Weapon(imagen_pistola, imagen_balas)

                    nivel = 1
                    ronda = 1
                    salida_desbloqueada = False
                    ronda_terminada = False
                    estado = "jugando"

                    grupo_balas.empty()
                    grupo_balas_enemigas.empty()
                    grupo_dmg_text.empty()
                    grupo_items.empty()

                    carga_mapa(nivel)

            
            if estado == "ronda_completada":
                if event.key == pygame.K_RETURN:
                    if ronda < MAX_RONDAS:
                        ronda += 1
                        
                        if ronda == 4 or ronda == 7 or ronda == 10:
                            salida_desbloqueada = True
                            ronda_terminada = True
                            estado = "jugando"
                            print("Salida Desbloqueada")
                        else:
                            cantidad = enemigos_ronda(ronda)
                            generar_enemigos_ronda(cantidad)
                            print("enemigos generados:", len(lista_enemigos))

                            ronda_terminada = False
                            estado = "jugando"
                        print(f"Comienza Ronda {ronda}")
                    else:
                        estado = "victoria"
                        print("Ganaste")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False
            if event.key == pygame.K_e:
                if salida_desbloqueada:
                    if world.abrir_puerta(player, tile_list):
                        print("Puerta abierta")
                else:
                    print("La salida esta Bloqueada")
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            if boton_reinicio.collidepoint(event.pos) and not player.vivo:
                player.vivo = True
                player.enemigos = 100
                player.score = 0
                grupo_balas_enemigas.empty()
                nivel = 1
                salida_desbloqueada = False
                ronda_terminada = False
                world_data = resetear_mundo()
                with open(ruta("niveles", f"nivel_{nivel}.csv"), newline='') as csvfile:   
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, fila in enumerate(reader):
                        for y, columna in enumerate(fila):
                            world_data[x][y] = int(columna)
                world = World()
                world.process_data(world_data, tile_list, items_imgs, animations_enemies)
                player.actualizar_coordenadas(consts.COORDENADAS[str(nivel)])

                lista_enemigos = []
                for enemies in world.lista_enemigos:
                    lista_enemigos.append(enemies)
                for item in world.lista_item:
                    grupo_items.add(item)


    pygame.display.update()


pygame.quit()