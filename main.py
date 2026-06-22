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
from boss import FinalBoss
from shooting_enemies import EnemigoDisparo

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
pygame.mixer.init()

window = pygame.display.set_mode((consts.ANCHO_VENTANA, consts.ALTO_VENTANA))
pygame.display.set_caption("PLACEHOLDER")

posicion_pantalla = [0, 0]
nivel = 1
start_time = pygame.time.get_ticks()

# Rondas estilo codigo de Nico
ronda = 1
MAX_RONDAS = 10
salida_desbloqueada = False
ronda_terminada = False

#Fonts
font = pygame.font.Font("assets//fonts//Minecraft.ttf", consts.FONT_SIZE)
font_game_over = pygame.font.Font("assets//fonts//BLOODY.TTF", consts.FONT_SIZE*3)
font_reinicio = pygame.font.Font("assets//fonts//Minecraft.ttf", consts.FONT_SIZE)
font_titulo = pygame.font.Font("assets//fonts//Ghost.ttf", consts.FONT_SIZE*2)

game_over_text = font_game_over.render("Game Over", True, consts.ROJO_OSURO)
texto_boton_reinicio = font_reinicio.render("Reiniciar", True, consts.BLANCO)

#Menu Inicio
boton_jugar = pygame.Rect(consts.ANCHO_VENTANA // 2 - 100, consts.ALTO_VENTANA // 2 - 20, 200, 55)
boton_salir = pygame.Rect(consts.ANCHO_VENTANA // 2 - 100, consts.ALTO_VENTANA // 2 + 55, 200, 55)
texto_boton_jugar = font.render("Jugar", True, consts.BLANCO)
texto_boton_salir = font.render("Salir", True, consts.BLANCO)

def dibujar_texto_centrado(texto, fuente, color, centro_x, centro_y):
    img = fuente.render(texto, True, color)
    rect = img.get_rect(center=(centro_x, centro_y))
    window.blit(img, rect)

def pantalla_inicio():
    window.fill(consts.BLUE)

    panel = pygame.Surface((560, 360), pygame.SRCALPHA)
    panel.fill((30, 30, 30, 150))
    panel_rect = panel.get_rect(center=(consts.ANCHO_VENTANA // 2, consts.ALTO_VENTANA // 2))
    window.blit(panel, panel_rect)

    dibujar_texto_centrado("PLACEHOLDER", font_titulo, consts.BLANCO, consts.ANCHO_VENTANA // 2, consts.ALTO_VENTANA // 2 - 115)

    pygame.draw.rect(window, consts.NARANJA, boton_jugar, border_radius=12)
    pygame.draw.rect(window, consts.ROJO_OSURO, boton_salir, border_radius=12)
    pygame.draw.rect(window, consts.BLANCO, boton_jugar, 2, border_radius=12)
    pygame.draw.rect(window, consts.BLANCO, boton_salir, 2, border_radius=12)

    window.blit(texto_boton_jugar, texto_boton_jugar.get_rect(center=boton_jugar.center))
    window.blit(texto_boton_salir, texto_boton_salir.get_rect(center=boton_salir.center))

    pygame.display.update()

#Importar Imgs
#Energia
corazon_vacio = pygame.image.load("assets//images//items//hp_empty.png")
corazon_vacio = escalar_img(corazon_vacio, consts.ESCALA_CORAZONES)
corazon_mitad = pygame.image.load("assets//images//items//hp_half.png")
corazon_mitad = escalar_img(corazon_mitad, consts.ESCALA_CORAZONES)
corazon_full = pygame.image.load("assets//images//items//hp_full.png")
corazon_full = escalar_img(corazon_full, consts.ESCALA_CORAZONES)

#Personaje
animations = []
for i in range(7):
    img = pygame.image.load(f"assets//images//characters//player//Player_{i}.png").convert_alpha()
    img = escalar_img(img, consts.ESCALA_PERSONAJE)
    animations.append(img)

#Enemigos
directorio_enemigos = "assets//images//characters//enemies"
tipo_enemigos = nombre_carpetas(directorio_enemigos)
animations_enemies = []
boss_animations = []

for enemies in tipo_enemigos:
    list_temp = []
    ruta_temp = f"assets//images//characters//enemies//{enemies}"
    num_animations = contar_elementos(ruta_temp)
    
    for i in range(num_animations):
        ruta_img_enemigo = f"{ruta_temp}//{enemies}_{i}.png"
        if not os.path.exists(ruta_img_enemigo):
            ruta_img_enemigo = f"{ruta_temp}//{enemies.capitalize()}_{i}.png"
        img_enemigo = pygame.image.load(ruta_img_enemigo).convert_alpha()
        img_enemigo = escalar_img(img_enemigo, consts.ESCALA_ENEMIGOS)
        list_temp.append(img_enemigo)
    animations_enemies.append(list_temp)

#Animacion del boss final usando el enemigo shroom agrandado
if len(animations_enemies) > 1:
    for img in animations_enemies[1]:
        nueva = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
        boss_animations.append(nueva)

#Arma
imagen_pistola = pygame.image.load("assets//images//weapons//gun.png").convert_alpha()
imagen_pistola = escalar_img(imagen_pistola, consts.ESCALA_ARMA)

#Balas
imagen_balas = pygame.image.load("assets//images//weapons//bullet.png").convert_alpha()
imagen_balas = escalar_img(imagen_balas, consts.ESCALA_ARMA)

#BG
tile_list = []
for x in range(270):#270
    tile_image = pygame.image.load(f"assets//images//tiles//tile ({x + 1}).png")
    tile_image = pygame.transform.scale(tile_image, (consts.TILE_SIZE, consts.TILE_SIZE))
    tile_list.append(tile_image)

#Items
#Posion
imagen_posion = pygame.image.load("assets//images//items//potion.png")
imagen_posion = escalar_img(imagen_posion, consts.ESCALA_POSION)
#Monedas
coin_images = []
ruta_img = "assets//images//items//coin"
num_coin_img = contar_elementos(ruta_img)
for i in range(num_coin_img):
    img = pygame.image.load(f"assets//images//items//coin//coin_{i}.png")
    img = escalar_img(img, consts.ESCALA_MONEDAS)
    coin_images.append(img)

items_imgs = [coin_images, [imagen_posion]]

#Texto pantalla
def dibujar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    window.blit(img, (x, y))

def dibujar_barra(x, y, ancho, alto, valor, maximo, color, texto=None):
    porcentaje = valor / maximo if maximo != 0 else 0
    if porcentaje > 1:
        porcentaje = 1
    if porcentaje < 0:
        porcentaje = 0

    fondo = pygame.Rect(x, y, ancho, alto)
    relleno = pygame.Rect(x, y, ancho * porcentaje, alto)

    pygame.draw.rect(window, (30, 30, 30), fondo, border_radius=10)
    pygame.draw.rect(window, color, relleno, border_radius=10)
    pygame.draw.rect(window, consts.BLANCO, fondo, 2, border_radius=10)

    # Estilo de Nico: el texto va dentro de la barra para que quede mas prolijo.
    if texto is not None:
        texto_barra = font.render(str(texto), True, consts.BLANCO)
        texto_rect = texto_barra.get_rect(center=fondo.center)
        window.blit(texto_barra, texto_rect)

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
    grupo_balas_enemigas.empty()

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
with open("niveles//nivel_1.csv", newline= '') as csvfile:
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
player = Personaje(950, 170, animations, consts.ENERGIA_PERSONAJE, 1)

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
boss_creado = False
final_tile_usado = False
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

def carga_mapa(numero_nivel):
    global world, world_data, lista_enemigos, posicion_pantalla, boss_creado

    grupo_balas.empty()
    grupo_balas_enemigas.empty()
    grupo_dmg_text.empty()
    grupo_items.empty()

    posicion_pantalla = [0, 0]
    world_data = resetear_mundo()

    with open(f"niveles//nivel_{numero_nivel}.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, fila in enumerate(reader):
            for y, columna in enumerate(fila):
                world_data[x][y] = int(columna)

    world = World()
    world.process_data(world_data, tile_list, items_imgs, animations_enemies)

    player.actualizar_coordenadas(consts.COORDENADAS[str(numero_nivel)])

    lista_enemigos = []
    boss_creado = False

    for item in world.lista_item:
        grupo_items.add(item)

def enemigos_ronda(ronda_actual):
    return 7 + (ronda_actual - 1) * 3

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

def obtener_offset_mapa():
    # Los puntos de spawn estan guardados como coordenadas del mapa original.
    # Como la camara mueve todos los tiles en pantalla, calculamos cuanto se movio
    # el mapa para convertir coordenadas de mapa -> coordenadas actuales de pantalla.
    if world.map_tiles:
        tile = world.map_tiles[0]
        return tile[1].centerx - tile[2], tile[1].centery - tile[3]
    return 0, 0

def coordenada_mapa_a_pantalla(x_mapa, y_mapa):
    offset_x, offset_y = obtener_offset_mapa()
    return x_mapa + offset_x, y_mapa + offset_y

def spawn_valido(x, y):
    # Validamos contra los obstaculos actuales, que ya estan movidos por la camara.
    rect_spawn = pygame.Rect(x - 20, y - 20, 40, 40)
    for obstaculo in world.obstaculos_tiles:
        if rect_spawn.colliderect(obstaculo[1]):
            return False
    return True

def generar_enemigos_ronda(cantidad):
    global lista_enemigos
    zonas = spawn_por_nivel.get(nivel, spawn_por_nivel[1])
    enemigos_creados = 0
    intentos = 0

    while enemigos_creados < cantidad and intentos < cantidad * 80:
        intentos += 1

        # Elegimos una coordenada real del mapa y despues la pasamos a pantalla.
        x_mapa, y_mapa = random.choice(zonas)
        x_mapa += random.randint(-10, 10)
        y_mapa += random.randint(-10, 10)
        x, y = coordenada_mapa_a_pantalla(x_mapa, y_mapa)

        distancia_jugador = ((x - player.shape.centerx) ** 2 + (y - player.shape.centery) ** 2) ** 0.5
        if distancia_jugador < 180:
            continue

        if not spawn_valido(x, y):
            continue

        numero = random.randint(1, 100)

        if numero <= 66 or len(animations_enemies) < 2:
            enemigo = Personaje(x, y, animations_enemies[0], 100 + ronda * 20, 2)
        else:
            enemigo = EnemigoDisparo(x, y, animations_enemies[1], 80 + ronda * 15, 3)

        lista_enemigos.append(enemigo)
        enemigos_creados += 1

    # Fallback: si algun mapa tiene pocos puntos validos, igual intentamos completar
    # usando los puntos de spawn sin el filtro de distancia al jugador.
    while enemigos_creados < cantidad:
        x_mapa, y_mapa = random.choice(zonas)
        x, y = coordenada_mapa_a_pantalla(x_mapa, y_mapa)
        if not spawn_valido(x, y):
            break

        if random.randint(1, 100) <= 66 or len(animations_enemies) < 2:
            enemigo = Personaje(x, y, animations_enemies[0], 100 + ronda * 20, 2)
        else:
            enemigo = EnemigoDisparo(x, y, animations_enemies[1], 80 + ronda * 15, 3)

        lista_enemigos.append(enemigo)
        enemigos_creados += 1


def reiniciar_partida():
    global player, pistola, nivel, ronda, salida_desbloqueada, ronda_terminada
    global final_tile_usado, estado, world_data, world, lista_enemigos, boss_creado
    global nivel_completado, posicion_pantalla
    global mover_arriba, mover_abajo, mover_izquierda, mover_derecha

    player = Personaje(950, 170, animations, consts.ENERGIA_PERSONAJE, 1)
    pistola = Weapon(imagen_pistola, imagen_balas)

    nivel = 1
    ronda = 1
    salida_desbloqueada = False
    ronda_terminada = False
    nivel_completado = False
    final_tile_usado = False
    boss_creado = False
    estado = "jugando"

    mover_arriba = False
    mover_abajo = False
    mover_izquierda = False
    mover_derecha = False

    grupo_balas.empty()
    grupo_balas_enemigas.empty()
    grupo_dmg_text.empty()
    grupo_items.empty()

    carga_mapa(nivel)
    generar_enemigos_ronda(enemigos_ronda(ronda))




#Efectos sonido
pygame.mixer.music.load("assets//sounds//Megalovania.mp3")
pygame.mixer.music.play(-1)
sonido_disparo = pygame.mixer.Sound("assets//sounds//Gunshot.wav")


mostrar_inicio = True
pausa = False
estado = "jugando"
run = True

nivel_completado = False
ronda_limpia = False
while run:
    if mostrar_inicio:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    mostrar_inicio = False
                if boton_salir.collidepoint(event.pos):
                    run = False
    else:
        #FPS
        reloj.tick(consts.FPS)

        #Control Frame Rates
        reloj = pygame.time.Clock()

        window.fill(consts.BLUE)

        #Tiempo
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000
        minutos = elapsed_time // 60
        segundos = elapsed_time % 60
        time_text_font = font.render(f"Tiempo: {minutos:02d}:{segundos:02d}", True, consts.BLANCO)
        time_text = time_text_font.get_rect(center =(consts.ANCHO_VENTANA / 2 + 35, 45))
        

        if pausa:
                # Dibujamos el juego de fondo y arriba un overlay transparente,
                # igual que las pantallas de level_up y ronda completada.
                world.draw(window)
                vida_player()
                player.dibujo(window)
                grupo_items.draw(window)

                overlay_fondo = pygame.Surface((consts.ANCHO_VENTANA, consts.ALTO_VENTANA), pygame.SRCALPHA)
                overlay_fondo.fill((0, 0, 0, 130))
                window.blit(overlay_fondo, (0, 0))

                panel = pygame.Surface((520, 230), pygame.SRCALPHA)
                panel.fill((30, 30, 30, 180))
                panel_rect = panel.get_rect(center=(consts.ANCHO_VENTANA // 2, consts.ALTO_VENTANA // 2))
                window.blit(panel, panel_rect)

                texto_pausa = font.render("Juego pausado", True, consts.AMARILLO)
                texto_continuar = font.render("P para continuar", True, consts.BLANCO)
                window.blit(texto_pausa, texto_pausa.get_rect(center=(consts.ANCHO_VENTANA // 2, consts.ALTO_VENTANA // 2 - 35)))
                window.blit(texto_continuar, texto_continuar.get_rect(center=(consts.ANCHO_VENTANA // 2, consts.ALTO_VENTANA // 2 + 35)))

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            pausa = False
                continue

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

            #Tiempo
            window.blit(time_text_font, time_text)

            # Jugador
            # La salida solo cuenta si la ronda ya habilito la puerta.
            exit_tile_activa = world.exit_tile if salida_desbloqueada else None
            posicion_pantalla, nivel_completado = player.movimiento(delta_x, delta_y, world.obstaculos_tiles, exit_tile_activa)
            if world.final_tile and player.shape.colliderect(world.final_tile[1]) and not final_tile_usado:
                # Easter egg: manda directo a la ronda final.
                final_tile_usado = True
                nivel = consts.MAX_LVL
                ronda = MAX_RONDAS
                salida_desbloqueada = False
                ronda_terminada = False
                estado = "jugando"
                boss_creado = False

                carga_mapa(nivel)
                generar_enemigos_ronda(enemigos_ronda(ronda))
                print("Easter egg final_tile: salto directo a ronda 10")
                print("Primero mata los enemigos de la ronda 10; despues aparece el jefe")
                
            world.tocar_trampa(player)
            player.update()
            player.dibujo(window)

            # Boss final: aparece solamente en la ronda 10, cuando ya no quedan enemigos normales.
            if nivel == consts.MAX_LVL and ronda == MAX_RONDAS and len(lista_enemigos) == 0 and not boss_creado and boss_animations:
                boss = FinalBoss(player.shape.centerx + 300, player.shape.centery, boss_animations)
                lista_enemigos.append(boss)
                boss_creado = True
                print("Aparecio el jefe final")

            #Enemigos
            for enemies in lista_enemigos[:]:
                if enemies.energia <= 0:
                    player.exp += 1

                    if isinstance(enemies, FinalBoss):
                        lista_enemigos.remove(enemies)
                        grupo_balas_enemigas.empty()
                        estado = "victoria"
                        print("Jefe final derrotado. Ganaste")
                        continue

                    # Drop de escudo de Nico: 10% de probabilidad
                    if random.randint(1, 100) <= 10:
                        escudo = Item(enemies.shape.centerx, enemies.shape.centery, 2, [])
                        grupo_items.add(escudo)

                    lista_enemigos.remove(enemies)
                    continue

                if isinstance(enemies, EnemigoDisparo):
                    enemies.enemigos(player, world.obstaculos_tiles, posicion_pantalla, world.exit_tile, grupo_balas_enemigas)
                else:
                    enemies.enemigos(player, world.obstaculos_tiles, posicion_pantalla, world.exit_tile)

                enemies.update()

                if isinstance(enemies, FinalBoss):
                    enemies.comprobar_fase(lista_enemigos, animations_enemies)
                    if enemies.es_fase2():
                        bala_boss = enemies.disparar(player)
                        if bala_boss:
                            grupo_balas_enemigas.add(bala_boss)

                enemies.dibujo(window)
            
            # Si en ronda 10 ya no quedan enemigos normales, aparece el jefe.
            if estado == "jugando" and nivel == consts.MAX_LVL and ronda == MAX_RONDAS and len(lista_enemigos) == 0 and not boss_creado and boss_animations:
                boss = FinalBoss(player.shape.centerx + 300, player.shape.centery, boss_animations)
                lista_enemigos.append(boss)
                boss_creado = True
                print("Aparecio el jefe final")

            # Rondas: cuando no quedan enemigos se muestra la pantalla de ronda completada.
            # En la ronda 10 no se completa la ronda: primero tiene que aparecer y morir el jefe.
            if estado == "jugando" and len(lista_enemigos) == 0 and ronda_terminada == False:
                if nivel == consts.MAX_LVL and ronda == MAX_RONDAS:
                    pass
                else:
                    ronda_terminada = True
                    estado = "ronda_completada"
                    print(f"Ronda {ronda} completada")

            #Arma
            bala = pistola.update(player)
            pistola.dibujo(window)

            if bala:
                grupo_balas.add(bala)
                sonido_disparo.play()
            
            for bala in grupo_balas:
                bala.dibujo(window)
                dmg, pos_dmg = bala.update(lista_enemigos, world.obstaculos_tiles)
                if dmg:
                    dmg_txt = DamageText(pos_dmg.centerx, pos_dmg.centery, str(dmg), font, consts.COLOR_FONT_DMG)
                    grupo_dmg_text.add(dmg_txt)

            #Balas enemigas: sirven tanto para el boss como para enemigos de disparo
            for bala_enemiga in grupo_balas_enemigas:
                try:
                    bala_enemiga.update(posicion_pantalla, player, world.obstaculos_tiles)
                    bala_enemiga.dibujo(window) if hasattr(bala_enemiga, "dibujo") else window.blit(bala_enemiga.image, bala_enemiga.rect)
                except TypeError:
                    bala_enemiga.update()
                    window.blit(bala_enemiga.image, bala_enemiga.rect)

                    if bala_enemiga.rect.colliderect(player.shape):
                        # Usa el mismo hit_cd del jugador: no recibe daño varias veces seguidas.
                        if player.hit == False:
                            if getattr(player, "escudo", 0) > 0:
                                player.escudo -= 10
                                if player.escudo < 0:
                                    player.escudo = 0
                            else:
                                player.energia -= 10
                            player.hit = True
                            player.last_hit = pygame.time.get_ticks()
                        bala_enemiga.kill()

                    if (bala_enemiga.rect.right < 0 or bala_enemiga.rect.left > consts.ANCHO_VENTANA or
                        bala_enemiga.rect.bottom < 0 or bala_enemiga.rect.top > consts.ALTO_VENTANA):
                        bala_enemiga.kill()
            
            #Txt
            grupo_dmg_text.update(posicion_pantalla)
            grupo_dmg_text.draw(window)
            dibujar_texto(f"Score : {player.score}", font, consts.COLOR_TEXTO_SCORE, 690, 5)
            dibujar_texto(f"Sala: " + str(nivel), font, consts.BLANCO, consts.ANCHO_VENTANA / 2, 5)
            # Textos de ronda abajo a la izquierda para que no molesten en el centro.
            dibujar_texto(f"Ronda: {ronda}/{MAX_RONDAS}", font, consts.BLANCO, 10, consts.ALTO_VENTANA - 70)
            dibujar_texto(f"Enemigos: {len(lista_enemigos)}", font, consts.BLANCO, 10, consts.ALTO_VENTANA - 40)
            if salida_desbloqueada:
                dibujar_texto("Salida desbloqueada - apreta E en la puerta", font, consts.AMARILLO, 10, consts.ALTO_VENTANA - 100)

            # HUD estilo Nico: nivel + barras de EXP y escudo.
            dibujar_texto(f"lvl: {player.nivel}", font, consts.BLANCO, 10, 28)
            dibujar_barra(10, 50, 220, 24, player.exp, player.exp_max, (0, 200, 80))
            dibujar_barra(10, 85, 220, 24, player.escudo, 100, (0, 150, 255))

            if player.exp >= player.exp_max:
                estado = "level_up"

            #Items
            grupo_items.update(posicion_pantalla, player)
            grupo_items.draw(window)

        #Nivel completo: solo cambia de sala cuando la salida esta desbloqueada.
        if nivel_completado == True and salida_desbloqueada == True:
            if nivel < consts.MAX_LVL:
                nivel += 1
                carga_mapa(nivel)

                salida_desbloqueada = False
                nivel_completado = False
                ronda_terminada = False

                cantidad = enemigos_ronda(ronda)
                generar_enemigos_ronda(cantidad)

                print(f"Cambiando al nivel {nivel}")
                print("enemigos generados:", len(lista_enemigos))
        if estado == "level_up" and player.vivo:
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
            op2 = font.render("2 - +5 de Dano", True, consts.BLANCO)
            op3 = font.render("3 - +1 de Velocidad", True, consts.BLANCO)
            op4 = font.render("4 - +Vel. Ataque", True, consts.BLANCO)

            window.blit(titulo, (260, 140))
            window.blit(op1, (250, 220))
            window.blit(op2, (250, 280))
            window.blit(op3, (250, 340))
            window.blit(op4, (250, 400))


        if estado == "ronda_completada" and player.vivo:
            world.draw(window)
            vida_player()
            player.dibujo(window)
            grupo_items.draw(window)

            overlay = pygame.Surface((consts.ANCHO_VENTANA, consts.ALTO_VENTANA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 130))
            window.blit(overlay, (0, 0))

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
            texto_salir = font.render("ESC = Salir", True, consts.BLANCO)

            rect_victoria = texto_victoria.get_rect(center=(consts.ANCHO_VENTANA // 2, consts.ALTO_VENTANA // 2 - 90))
            rect_salir = texto_salir.get_rect(center=(consts.ANCHO_VENTANA // 2, consts.ALTO_VENTANA // 2 + 180))

            window.blit(texto_victoria, rect_victoria)
            window.blit(texto_salir, rect_salir)

        if player.vivo == False:
            window.fill(consts.BLUE_RED)
            text_rect = game_over_text.get_rect(center=(consts.ANCHO_VENTANA/2, consts.ALTO_VENTANA/2))
            window.blit(game_over_text, text_rect)

            pygame.draw.rect(window, consts.VERDE_SLIME, boton_reinicio)
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
                        if player.energia > 100:
                            player.energia = 100
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


                if estado == "ronda_completada":
                    if event.key == pygame.K_RETURN:
                        if ronda < MAX_RONDAS:
                            ronda += 1

                            # Cada 3 rondas se desbloquea la salida para pasar a la siguiente sala.
                            # En la ronda 10 se desbloquea la salida hacia el final/boss.
                            if ronda == 4 or ronda == 7 or ronda == 10:
                                salida_desbloqueada = True
                                ronda_terminada = True
                                estado = "jugando"
                                print("Salida desbloqueada")
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

                if event.key == pygame.K_e:
                    if salida_desbloqueada:
                        if world.abrir_puerta(player, tile_list, True):
                            print("Puerta abierta")
                    else:
                        print("La salida esta bloqueada")
                    if world.abrir_cofre(player, tile_list):
                        print("Cofre trampa")
                if event.key == pygame.K_p:
                    pausa = not pausa
                    mover_abajo = False
                    mover_arriba = False
                    mover_izquierda = False
                    mover_derecha = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_izquierda = False
                if event.key == pygame.K_d:
                    mover_derecha = False
                if event.key == pygame.K_w:
                    mover_arriba = False
                if event.key == pygame.K_s:
                    mover_abajo = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reinicio.collidepoint(event.pos) and (not player.vivo or estado == "victoria"):
                    reiniciar_partida()

        pygame.display.update()


pygame.quit()