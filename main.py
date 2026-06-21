import pygame
import consts
import os
import csv
from character import Personaje
from weapons import Weapon
from textos import DamageText
from items import Item
from world import World

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
pygame.display.set_caption("Mi primer juego")

posicion_pantalla = [0, 0]
nivel = 1
start_time = pygame.time.get_ticks()

#Fonts
font = pygame.font.Font("assets//fonts//Minecraft.ttf", consts.FONT_SIZE)
font_game_over = pygame.font.Font("assets//fonts//BLOODY.TTF", consts.FONT_SIZE*3)
font_reinicio = pygame.font.Font("assets//fonts//Minecraft.ttf", consts.FONT_SIZE)
font_titulo = pygame.font.Font("assets//fonts//Ghost.ttf", consts.FONT_SIZE*2)

game_over_text = font_game_over.render("Game Over", True, consts.ROJO_OSURO)
texto_boton_reinicio = font_reinicio.render("Reiniciar", True, consts.BLANCO)

#Menu Inicio
boton_jugar = pygame.Rect(consts.ANCHO_VENTANA / 2 - 100, consts.ALTO_VENTANA / 2 - 50, 200, 50)
boton_salir = pygame.Rect(consts.ANCHO_VENTANA / 2 - 100, consts.ALTO_VENTANA / 2 + 50, 200, 50)
texto_boton_jugar = font.render("Jugar", True, consts.BLANCO)
texto_boton_salir = font.render("Salir", True, consts.BLANCO)

def pantalla_inicio():
    window.fill(consts.BLUE)
    dibujar_texto("PLACEHOLDER", font_titulo, consts.BLANCO, consts.ANCHO_VENTANA / 2 - 200, consts.ALTO_VENTANA / 2 - 200)
    pygame.draw.rect(window, consts.NARANJA, boton_jugar)
    pygame.draw.rect(window, consts.ROJO_OSURO, boton_salir)
    window.blit(texto_boton_jugar, (boton_jugar.x + 50, boton_jugar.y + 10))
    window.blit(texto_boton_salir, (boton_salir.x + 50, boton_salir.y + 10))
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

for enemies in tipo_enemigos:
    list_temp = []
    ruta_temp = f"assets//images//characters//enemies//{enemies}"
    num_animations = contar_elementos(ruta_temp)
    
    for i in range(num_animations):
        img_enemigo = pygame.image.load(f"{ruta_temp}//{enemies}_{i}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo, consts.ESCALA_ENEMIGOS)
        list_temp.append(img_enemigo)
    animations_enemies.append(list_temp)


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

#Efectos sonido
pygame.mixer.music.load("assets//sounds//Megalovania.mp3")
pygame.mixer.music.play(-1)
sonido_disparo = pygame.mixer.Sound("assets//sounds//Gunshot.wav")


mostrar_inicio = True
pausa = False
run = True
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
                texto_pausa = font.render("Juego pausado", True, consts.AMARILLO)    
                text_rect = texto_pausa.get_rect(center =(consts.ANCHO_VENTANA / 2, consts.ALTO_VENTANA / 2))
                window.blit(texto_pausa, text_rect)
                
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            pausa = False
                continue

        if player.vivo:
                
            #dibujar_grid()

            #Calculo Movimiento Jugador
            delta_x = 0
            delta_y = 0

            if mover_derecha == True:
                delta_x = consts.VELOCIDAD_PERSONAJE
            if mover_izquierda == True:
                delta_x = -consts.VELOCIDAD_PERSONAJE
            if mover_arriba == True:
                delta_y = -consts.VELOCIDAD_PERSONAJE
            if mover_abajo == True:
                delta_y = consts.VELOCIDAD_PERSONAJE


            #BG
            world.draw(window)
            world.update(posicion_pantalla)

            #Corazones
            vida_player()

            #Tiempo
            window.blit(time_text_font, time_text)

            #Jugador
            posicion_pantalla, nivel_completado = player.movimiento(delta_x, delta_y, world.obstaculos_tiles, world.exit_tile)
            if world.final_tile and player.shape.colliderect(world.final_tile[1]):
                nivel = consts.MAX_LVL

                world_data = resetear_mundo()

                with open(f"niveles//nivel_{nivel}.csv", newline='') as csvfile:
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

                grupo_items.empty()
                for item in world.lista_item:
                    grupo_items.add(item)
                
            world.tocar_trampa(player)
            player.update()
            player.dibujo(window)

            #Enemigos
            for enemies in lista_enemigos:
                if enemies.energia == 0:
                    lista_enemigos.remove(enemies)
                if enemies.energia > 0:
                    enemies.enemigos(player, world.obstaculos_tiles, posicion_pantalla, world.exit_tile)
                    enemies.update()
                    enemies.dibujo(window)
            
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
            
            #Txt
            grupo_dmg_text.update(posicion_pantalla)
            grupo_dmg_text.draw(window)
            dibujar_texto(f"Score : {player.score}", font, consts.COLOR_TEXTO_SCORE, 690, 5)
            dibujar_texto(f"Sala: " + str(nivel), font, consts.BLANCO, consts.ANCHO_VENTANA / 2, 5)


            #Items
            grupo_items.update(posicion_pantalla, player)
            grupo_items.draw(window)

        #Nivel completo
        if nivel_completado == True:
            if nivel < consts.MAX_LVL:
                nivel += 1
                world_data = resetear_mundo()
                with open(f"niveles//nivel_{nivel}.csv", newline= '') as csvfile:    
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
                if event.key == pygame.K_e:
                    if world.abrir_puerta(player, tile_list):
                        print("Puerta abierta")
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
                if boton_reinicio.collidepoint(event.pos) and not player.vivo:
                    player.vivo = True
                    player.energia = 100
                    player.score = 0
                    nivel = 1
                    world_data = resetear_mundo()
                    with open(f"niveles//nivel_{nivel}.csv", newline= '') as csvfile:    
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