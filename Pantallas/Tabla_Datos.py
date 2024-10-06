import pandas as pd
import pygame
from pygame.locals import *
from pymongo import MongoClient

# Configura la conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['SpaceBioScope']  # Cambia por el nombre de tu base de datos
collection = db['OSD-665']  # Cambia por el nombre de tu colección

# Extrae los datos de MongoDB y los convierte en un DataFrame
data = pd.DataFrame(list(collection.find()))
print(data.head())  # Verifica que se están obteniendo los datos

# Inicializa Pygame
pygame.init()
info_pantalla = pygame.display.Info()
ANCHO, ALTO = info_pantalla.current_w, info_pantalla.current_h
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Visualización de Datos")

# Estilo de la tabla
FONDO = (255, 255, 255)  # Fondo blanco
TEXTO = (0, 0, 0)  # Texto negro
FUENTE = pygame.font.SysFont('Arial', 20)
MARGEN_FILA = 10  # Espacio entre filas
MARGEN_COL = 5  # Margen entre columnas

# Variables para el desplazamiento
offset_y = 0
offset_x = 0
scroll_speed = 5

# Definir anchos dinámicos según el tipo de dato
column_widths = []
for col in data.columns:
    # Determina la longitud del valor más largo
    max_len = data[col].astype(str).map(len).max()
    # Asigna ancho basado en el contenido
    column_width = max(100, min(max_len * 10, 300))
    column_widths.append(column_width)

# Función para dibujar la tabla


def dibujar_tabla(data, offset_y, offset_x):
    screen.fill(FONDO)

    if data.empty:
        # Mensaje si no hay datos
        mensaje = FUENTE.render("No hay datos disponibles", True, TEXTO)
        screen.blit(mensaje, (ANCHO // 2 - mensaje.get_width() //
                    2, ALTO // 2 - mensaje.get_height() // 2))
    else:
        # Calcular posiciones de columnas con desplazamiento horizontal
        # Posición de la primera columna con el desplazamiento
        col_pos_x = [-offset_x]
        for width in column_widths:
            col_pos_x.append(col_pos_x[-1] + width + MARGEN_COL)

        # Dibujar encabezados
        for col_num, column in enumerate(data.columns):
            # Si la columna está fuera de la pantalla a la derecha
            if col_pos_x[col_num] >= ANCHO:
                break
            # Si la columna está al menos parcialmente en pantalla
            if col_pos_x[col_num + 1] > 0:
                texto = FUENTE.render(column, True, TEXTO)
                screen.blit(texto, (col_pos_x[col_num] + MARGEN_COL, 5))

        # Dibujar filas
        for row_num, row in enumerate(data.values):
            if row_num * (25 + MARGEN_FILA) - offset_y > ALTO - 40:  # Límite inferior
                break
            if row_num * (25 + MARGEN_FILA) - offset_y < 0:  # Límite superior
                continue

            for col_num, value in enumerate(row):
                # Si la columna está fuera de la pantalla a la derecha
                if col_pos_x[col_num] >= ANCHO:
                    break
                # Si la columna está al menos parcialmente en pantalla
                if col_pos_x[col_num + 1] > 0:
                    texto = FUENTE.render(str(value), True, TEXTO)
                    screen.blit(
                        texto, (col_pos_x[col_num] + MARGEN_COL, (row_num * (25 + MARGEN_FILA)) - offset_y + 25))

    pygame.display.flip()


# Bucle principal de Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Controlar el desplazamiento
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Mover hacia arriba
                offset_y = max(0, offset_y - scroll_speed)
            elif event.key == pygame.K_DOWN:
                offset_y = min(len(data) * (25 + MARGEN_FILA) - ALTO +
                               40, offset_y + scroll_speed)  # Mover hacia abajo
            elif event.key == pygame.K_LEFT:
                # Mover hacia la izquierda
                offset_x = max(0, offset_x - scroll_speed * 10)
            elif event.key == pygame.K_RIGHT:
                max_x = sum(column_widths) + \
                    len(column_widths) * MARGEN_COL - ANCHO
                # Mover hacia la derecha
                offset_x = min(max_x, offset_x + scroll_speed * 10)

            # Terminar la ejecución con ESC o R
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_r:
                running = False

    dibujar_tabla(data, offset_y, offset_x)  # Muestra la tabla en la pantalla

pygame.quit()
