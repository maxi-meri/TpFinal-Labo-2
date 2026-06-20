import os
from PIL import Image

def divir_guardar_imagen(ruta_imagen, carpeta_destino, divisiones_por_columna):
    #Carga de imagen
    with Image.open(ruta_imagen) as img:
        ancho, alto = img.size
    
        #Numero de divisiones por filas
        tamaño_cuadrado = ancho // divisiones_por_columna
        divisiones_por_filas = alto// tamaño_cuadrado

        os.makedirs(carpeta_destino, exist_ok=True)

        #Dividir y guardar
        contador = 0
        for i in range(divisiones_por_filas):
            for j in range(divisiones_por_columna):
                #Coordenadas
                izquierda = j * tamaño_cuadrado
                superior = i * tamaño_cuadrado
                derecha = izquierda + tamaño_cuadrado
                inferior = superior + tamaño_cuadrado

                #Cortar y guardar
                cuadrado = img.crop((izquierda, superior, derecha, inferior))
                nombre_archivo = f"tile ({contador+1}).png"
                cuadrado.save(os.path.join(carpeta_destino, nombre_archivo))
                contador += 1

divir_guardar_imagen("assets//images//tiles//tilesets//Dungeon Tile Set.png", "assets//images//tiles", 15)
