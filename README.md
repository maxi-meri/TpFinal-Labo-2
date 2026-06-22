# TP Final - Laboratorio de Programación 2

## Integrantes

- Lucas Viña
- Nicolás Olivares
- Matias Gebecke

---

## Descripción

Este trabajo consiste en un juego desarrollado en Python utilizando la librería Pygame.

El jugador debe recorrer distintas salas eliminando enemigos para superar rondas y avanzar por los diferentes niveles. Durante la partida podrá obtener experiencia, subir de nivel y elegir mejoras para fortalecer a su personaje.

El objetivo es llegar hasta la última sala y completar la ronda final para ganar la partida.

---

## Características del juego

- Movimiento libre del personaje.
- Disparo con arma a distancia.
- Sistema de vida mediante corazones.
- Sistema de experiencia y subida de nivel.
- Menú de mejoras al subir de nivel.
- Enemigos cuerpo a cuerpo.
- Enemigos que atacan a distancia.
- Sistema de rondas con dificultad progresiva.
- Desbloqueo de puertas para avanzar entre niveles.
- Pantalla de ronda completada.
- Pantalla de victoria.
- Pantalla de derrota y reinicio.

---

## Controles

| Tecla | Acción |
|--------|----------|
| W | Mover arriba |
| A | Mover izquierda |
| S | Mover abajo |
| D | Mover derecha |
| Click Izquierdo | Disparar |
| E | Abrir puerta |
| Enter | Continuar a la siguiente ronda |
| 1 - 4 | Elegir mejora al subir de nivel |
| R | Reiniciar partida |
| ESC | Salir del juego |

---

## Sistema de Rondas

Los enemigos aparecen en rondas.

A medida que avanzan las rondas:

- Aparecen más enemigos.
- Los enemigos tienen más vida.
- Se combinan enemigos de distintos tipos.
- La dificultad aumenta progresivamente.

Al completar determinadas rondas se desbloquea la salida para avanzar al siguiente nivel.

---

## Sistema de Mejoras

Cuando el jugador consigue suficiente experiencia sube de nivel y puede elegir una mejora:

1. Aumentar vida.
2. Aumentar daño.
3. Aumentar velocidad.
4. Aumentar velocidad de ataque.

---

## Niveles

El juego cuenta con varias salas conectadas entre sí.

- Sala 1
- Sala 2
- Sala 3
- Sala 4 (ronda final)

Cada sala posee una distribución distinta y diferentes puntos de aparición para los enemigos.

---

## Tecnologías utilizadas

- Python 3
- Pygame

---

## Cómo ejecutar el juego

Instalar Pygame:

```bash
pip install pygame
```

Ejecutar el archivo principal:

```bash
python main.py
```

---

## Estructura del proyecto

- `main.py` → Lógica principal del juego.
- `character.py` → Jugador y enemigos.
- `weapons.py` → Sistema de armas y disparos.
- `shooting_enemies.py` → Enemigos a distancia.
- `boss.py` → Lógica del jefe.
- `items.py` → Objetos e ítems.
- `world.py` → Carga y manejo de mapas.
- `textos.py` → Textos de daño.
- `consts.py` → Configuración general.

---

## Comentarios

Durante el desarrollo se trabajó con:

- Programación orientada a objetos.
- Manejo de sprites.
- Colisiones.
- Carga de mapas desde archivos CSV.
- Administración de estados del juego.
- Uso de grupos de sprites de Pygame.

Este proyecto fue realizado como trabajo práctico final de Laboratorio de Programación 2.