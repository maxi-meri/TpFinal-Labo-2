import pygame
import sys
import math
import random

from jugador import Jugador
from balas import Bala
from enemigo import Enemigo
from mejoras import vida, daño, velocidad
from experiencia import Experiencia
from enemigo_disparo import EnemigoDisparo
from bala_enemigo import BalaEnemigo
from escudo import Escudo

pygame.init()

ancho = 800
alto = 600

ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("El juego del Papu")

clock = pygame.time.Clock()
jugador = Jugador()
balas = []
enemigos = []
balas_enemigos = []
experiencias = []
escudos = []
spawn_timer = 0
estado = "jugando"

ronda = 1
enemigos_rondas = 5
enemigos_spawned = 0

while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado == "lvl_up":
            if evento.type == pygame.KEYDOWN:

                mejora_elegida = False

                if evento.key == pygame.K_1:
                    vida(jugador)
                    mejora_elegida = True
                elif evento.key == pygame.K_2:
                    daño(jugador)
                    mejora_elegida = True
                elif evento.key == pygame.K_3:
                    velocidad(jugador)
                    mejora_elegida = True
                
                if mejora_elegida:
                    ronda += 1
                    enemigos_rondas += 5
                    enemigos_spawned = 0
                    estado = "jugando"

        if estado == "game_over":

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:

                    jugador = Jugador()
                    balas = []
                    enemigos = []
                    experiencias = []
                    balas_enemigos = []
                    spawn_timer = 0

                    ronda = 1
                    enemigos_rondas = 5
                    enemigos_spawned = 0
                    estado = "jugando"
                if evento.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN and estado == "jugando":

            if evento.button == 1:

                mouse_x, mouse_y = pygame.mouse.get_pos()

                centro_x = jugador.x + 50
                centro_y = jugador.y + 40

                dx = mouse_x - centro_x
                dy = mouse_y - centro_y

                distancia = math.hypot(dx, dy)

                if distancia != 0:

                    dx = dx / distancia
                    dy = dy / distancia
                    bala = Bala(centro_x, centro_y, dx, dy)
                    balas.append(bala)

    if estado == "jugando":

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas, ancho, alto)

        spawn_timer += 1

        if spawn_timer >= 180 and enemigos_spawned < enemigos_rondas:
            numero = random.randint(1, 100)

            if numero <= 33:
                enemigos.append(EnemigoDisparo(ancho, alto, ronda))
            else:
                enemigos.append(Enemigo(ancho, alto, ronda))

            enemigos_spawned += 1
            spawn_timer = 0

        for bala in balas_enemigos[:]:
            dx = bala.x - (jugador.x + 50)
            dy = bala.y - (jugador.y + 40)

            distancia = math.hypot(dx, dy)

            if distancia < bala.radio + 30:
                if jugador.escudos > 0:
                    jugador.escudos -= 1
                else:
                    jugador.vida -= 5

                balas_enemigos.remove(bala)

        for bala in balas:
            bala.mover()

        for bala in balas_enemigos:
            bala.mover()

        for enemigo in enemigos:
            enemigo.mover(jugador)

        for enemigo in enemigos:
            if isinstance(enemigo, EnemigoDisparo):
                datos = enemigo.disparar(jugador)

                if datos:
                    x,y,dx,dy = datos
                    
                    balas_enemigos.append(BalaEnemigo(x,y,dx,dy))

        for enemigo in enemigos[:]:

            for bala in balas[:]:

                dx = enemigo.x - bala.x
                dy = enemigo.y - bala.y

                distancia = math.hypot(dx, dy)

                if distancia < enemigo.radio + bala.radio:

                    enemigo.recibir_daño(jugador.daño)

                    if bala in balas:
                        balas.remove(bala)

        for enemigo in enemigos[:]:

            dx = enemigo.x - (jugador.x + 50)
            dy = enemigo.y - (jugador.y + 40)

            distancia = math.hypot(dx, dy)

            if distancia < enemigo.radio + 30:

                if jugador.escudos > 0:
                    jugador.escudos -= 1
                else:
                    jugador.vida -= enemigo.daño

                if enemigo in enemigos:
                    enemigos.remove(enemigo)

        for enemigo in enemigos:

            if enemigo.muerto():
                experiencias.append(Experiencia(enemigo.x, enemigo.y))

                if random.randint(1, 100) <= 10:
                    escudos.append(Escudo(enemigo.x, enemigo.y))

                enemigos.remove(enemigo) 
        
        for exp in experiencias[:]:
            dx = exp.x - (jugador.x + 50)
            dy = exp.y - (jugador.y + 40)

            distancia = math.hypot(dx, dy)

            if distancia < exp.radio + 30:
                jugador.exp += 1
                experiencias.remove(exp)

        for escudo in escudos[:]:
            dx = escudo.x - (jugador.x + 50)
            dy = escudo.y - (jugador.y + 40)

            distancia = math.hypot(dx, dy)

            if distancia < escudo.radio + 30:
                jugador.escudos += 1
                escudos.remove(escudo)

        if jugador.exp >= jugador.exp_max:
            jugador.nivel += 1
            jugador.exp = 0 
            jugador.exp_max += 5

        if enemigos_spawned >= enemigos_rondas and len(enemigos) == 0:
            estado = "lvl_up"

        balas = [
            bala for bala in balas
            if not bala.fuera_pantalla(ancho, alto)
        ]

        balas_enemigos = [
            bala for bala in balas_enemigos
            if not bala.fuera_pantalla(ancho, alto)
        ]

        if jugador.vida <= 0:
            estado = "game_over"

    ventana.fill((0, 0, 0))
    fuente = pygame.font.SysFont(None, 40)

    texto_vida = fuente.render(f"Vida: {jugador.vida}", True, (255, 255, 255))
    ventana.blit(texto_vida, (20, 20))

    texto_ronda = fuente.render(f"Ronda: {ronda}", True, (255, 255, 255))
    ventana.blit(texto_ronda, (20, 60))

    restantes = (enemigos_rondas - enemigos_spawned)
    texto_restantes = fuente.render(f"enemigos: {restantes}", True, (255, 255, 255))
    ventana.blit(texto_restantes, (20,100))

    texto_exp = fuente.render(f"exp: {jugador.exp}/{jugador.exp_max}", True, (255, 255, 255))
    ventana.blit(texto_exp, (20, 140))

    texto_nivel = fuente.render(f"nivel: {jugador.nivel}", True, (255, 255, 255))
    ventana.blit(texto_nivel, (20, 180))

    texto_escudos = fuente.render(f"escudos: {jugador.escudos}", True, (0, 200, 255))
    ventana.blit(texto_escudos, (20, 220))

    if estado == "jugando":

        jugador.dibujar(ventana)

        for bala in balas:
            bala.dibujar(ventana)

        for bala in balas_enemigos:
            bala.dibujar(ventana)

        for enemigo in enemigos:
            enemigo.dibujar(ventana)

        for exp in experiencias:
            exp.dibujar(ventana)

    if estado == "game_over":
        fuente_grande = pygame.font.SysFont(None, 70)

        texto = fuente_grande.render("GAME OVER", True, (255, 0, 0))
        texto2 = fuente.render("R = Reiniciar", True, (255, 255, 255))
        texto3 = fuente.render("ESC = Salir", True, (255, 255, 255))

        ventana.blit(texto, (220, 180))
        ventana.blit(texto2, (260, 300))
        ventana.blit(texto3, (270, 360))

    if estado == "lvl_up":
        fuente_grande = pygame.font.SysFont(None, 70)

        titulo = fuente_grande.render("nivel superado", True, (255, 255, 255))
        opcion1 = fuente.render("1 - vida", True, (255, 255, 255))
        opcion2 = fuente.render("2 - daño", True, (255, 255, 255))
        opcion3 = fuente.render("3 - velocidad", True, (255, 255, 255))

        ventana.blit(titulo, (180, 150))
        ventana.blit(opcion1, (250, 260))
        ventana.blit(opcion2, (250, 320))
        ventana.blit(opcion3, (250, 380))

    pygame.display.update()
    clock.tick(90)