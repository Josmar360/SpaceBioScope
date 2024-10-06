import pygame
import random
import sys
import pymongo
from PIL import Image
import io
import base64
from .Pantalla_Final import Pantalla_Final
# from .Informacion_Nebulosa import Informacion_Nebulosa
# from .Carga_Informacion import Carga_Informacion

# Inicializar Pygame
pygame.init()

# Obtener información de la pantalla
info_pantalla = pygame.display.Info()
ANCHO, ALTO = info_pantalla.current_w, info_pantalla.current_h

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Función para generar estrellas aleatorias


def generar_estrellas():
    estrellas = []
    for _ in range(200):  # Generar 200 estrellas
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        estrellas.append((x, y))
    return estrellas


# Velocidad de movimiento de las estrellas
VELOCIDAD_ESTRELLAS = 0.2

# Función para mover las estrellas


def mover_estrellas(estrellas):
    nuevas_estrellas = []
    for estrella in estrellas:
        x, y = estrella
        y += VELOCIDAD_ESTRELLAS
        if y > ALTO:  # Si la estrella se sale de la pantalla, reaparece en la parte superior
            y = random.randint(-50, 0)
        nuevas_estrellas.append((x, y))
    return nuevas_estrellas


# Conexión a MongoDB
cliente = pymongo.MongoClient("mongodb://localhost:27017")
db = cliente["SpaceBioScope"]
collection = db["Experimentos_Mamiferos"]

# Recuperar imágenes de MongoDB y escalarlas
imagenes_recuadros = []
textos_recuadros = []
imagenes_escaladas = []

recuadro_ancho = 250
recuadro_alto = 150

for documento in collection.find():
    # Decodificar la imagen desde base64
    imagen_base64 = documento["Contenido_del_archivo"]
    imagen_binaria = base64.b64decode(imagen_base64)

    # Asegurarse de que la imagen esté en formato RGBA
    imagen_pil = Image.open(io.BytesIO(imagen_binaria)).convert('RGBA')
    imagen_pygame = pygame.image.fromstring(
        imagen_pil.tobytes(), imagen_pil.size, imagen_pil.mode)

    imagenes_recuadros.append(imagen_pygame)
    textos_recuadros.append(documento["Designación"])

    # Escalar la imagen al tamaño del recuadro
    imagen_escalada = pygame.transform.scale(
        imagen_pygame, (recuadro_ancho, recuadro_alto))
    imagenes_escaladas.append(imagen_escalada)

# Imprimir la cantidad de nebulosas cargadas
print("Número de nebulosas cargadas:", len(imagenes_recuadros))


def Catalogo_Mamiferos():
    # Crear la pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Catálogo de Nebulosas")

    # Generar estrellas aleatorias
    estrellas = generar_estrellas()

    # Cargar la fuente del título del catálogo
    fuente_titulo = pygame.font.Font("Font/13_Misa.ttf", 100)

    # Texto del título
    texto_titulo = fuente_titulo.render("Catalogo de Nebulosas", True, BLANCO)
    texto_titulo_rect = texto_titulo.get_rect(
        center=(ANCHO / 2, ALTO / 6))  # Centrar el texto

    # Cargar la fuente para los textos de los recuadros
    fuente_recuadros = pygame.font.Font("Font/OriginTech_personal_use.ttf", 28)

    # Rectángulos interactivos
    espacio_entre_recuadros_ancho = 60
    espacio_entre_recuadros_alto = 80
    margen_superior = ALTO / 3  # Ajustar el margen superior para evitar solapamiento
    margen_inferior = 80
    recuadros = []
    num_columnas = 4

    for i in range(len(textos_recuadros)):
        columna = i % num_columnas
        fila = i // num_columnas
        recuadro_x = ((ANCHO // 1.15) - (num_columnas * (recuadro_ancho + espacio_entre_recuadros_ancho -
                      espacio_entre_recuadros_ancho))) // 2 + columna * (recuadro_ancho + espacio_entre_recuadros_ancho)
        recuadro_y = margen_superior + fila * \
            (recuadro_alto + espacio_entre_recuadros_alto)
        recuadro = pygame.Rect(recuadro_x, recuadro_y,
                               recuadro_ancho, recuadro_alto)
        recuadros.append(recuadro)

    # Variables para la barra de desplazamiento
    desplazamiento = 0
    velocidad_desplazamiento = 20

    # Configurar el botón "Regresar"
    fuente_boton_regresar = pygame.font.Font(None, 36)
    texto_boton_regresar = fuente_boton_regresar.render(
        "Regresar", True, BLANCO)
    boton_rect_regresar = pygame.Rect(20, (ALTO // 1.1), 120, 50)

    # Configurar el botón "Salir"
    fuente_boton_salir = pygame.font.Font(None, 36)
    texto_boton_salir = fuente_boton_salir.render("   Salir", True, BLANCO)
    boton_rect_salir = pygame.Rect((ANCHO // 1.11), (ALTO // 1.1), 120, 50)

    def accion_regresar():
        from .Carga_Catalogo import Carga_Catalogo
        from .Menu_Principal import Menu_Principal
        Carga_Catalogo("Mamiferos")
        Menu_Principal()

    def accion_salir():
        Pantalla_Final()

    def informacion_nebulosa(_id):
        print("Hola")
        # Carga_Informacion()
        # Informacion_Nebulosa(_id)

    # Bucle principal
    ejecutando = True
    while ejecutando:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    ejecutando = False
                    accion_regresar()
                elif evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                    Pantalla_Final()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 4:  # Rueda del ratón hacia arriba
                    desplazamiento = min(
                        desplazamiento + velocidad_desplazamiento, 0)
                elif evento.button == 5:  # Rueda del ratón hacia abajo
                    max_desplazamiento = -(len(textos_recuadros) // num_columnas) * (
                        recuadro_alto + espacio_entre_recuadros_alto) + ALTO - margen_superior - margen_inferior - recuadro_alto
                    desplazamiento = max(
                        desplazamiento - velocidad_desplazamiento, max_desplazamiento)
                elif evento.button == 1:  # Botón izquierdo del ratón
                    if boton_rect_regresar.collidepoint(evento.pos):
                        accion_regresar()
                    elif boton_rect_salir.collidepoint(evento.pos):
                        accion_salir()
                    for i, recuadro in enumerate(recuadros):
                        recuadro_desplazado = recuadro.move(0, desplazamiento)
                        if recuadro_desplazado.collidepoint(evento.pos):
                            db_id = collection.find_one(
                                {"Designación": textos_recuadros[i]})["_id"]
                            informacion_nebulosa(db_id)

        # Mover las estrellas
        estrellas = mover_estrellas(estrellas)

        # Dibujar la pantalla
        pantalla.fill(NEGRO)

        # Dibujar las estrellas
        for estrella in estrellas:
            pygame.draw.circle(pantalla, BLANCO, estrella,
                               1)  # Dibujar estrella

        # Mostrar el título
        pantalla.blit(texto_titulo, texto_titulo_rect)

        # Dibujar los recuadros con sus respectivas imágenes y textos
        for i, recuadro in enumerate(recuadros):
            recuadro_desplazado = recuadro.move(0, desplazamiento)
            alpha = 255

            # Aplicar desvanecimiento si el recuadro está cerca de los márgenes
            fade_margin = 70  # Margen para empezar a desvanecer
            if recuadro_desplazado.top < texto_titulo_rect.bottom + fade_margin:
                alpha = max(0, 255 * (recuadro_desplazado.top -
                            0.8 * texto_titulo_rect.bottom) / fade_margin)
            elif recuadro_desplazado.bottom > ALTO - margen_inferior - fade_margin:
                alpha = max(0, 255 * (ALTO - margen_inferior -
                            recuadro_desplazado.bottom) / fade_margin)

            # Dibujar la imagen del recuadro
            imagen = imagenes_escaladas[i].copy()
            imagen.set_alpha(alpha)
            pantalla.blit(imagen, recuadro_desplazado)

            # Dibujar el texto del recuadro
            texto_recuadro = fuente_recuadros.render(
                textos_recuadros[i], True, BLANCO)
            texto_recuadro.set_alpha(alpha)
            pantalla.blit(texto_recuadro, (recuadro_desplazado.x,
                                           recuadro_desplazado.bottom + 5))

        # Dibujar los botones
        pygame.draw.rect(pantalla, BLANCO, boton_rect_regresar, 2)
        pantalla.blit(texto_boton_regresar, boton_rect_regresar)
        pygame.draw.rect(pantalla, BLANCO, boton_rect_salir, 2)
        pantalla.blit(texto_boton_salir, boton_rect_salir)

        # Actualizar la pantalla
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    Catalogo_Mamiferos()
