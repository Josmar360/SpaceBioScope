import pygame
import sys
import random
import math
import pymongo
from PIL import Image
import io
import base64
import webbrowser
from .Pantalla_Final import Pantalla_Final

# Inicializar Pygame
pygame.init()

# Obtener información de la pantalla
info_pantalla = pygame.display.Info()
ANCHO, ALTO = info_pantalla.current_w, info_pantalla.current_h
pygame.display.set_caption("Información del experimento")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Clase para las estrellas parpadeantes


class Estrellas:
    def __init__(self):
        self.x = random.randint(0, ANCHO)
        self.y = random.randint(0, ALTO)
        self.tamano = random.randint(1, 3)
        self.velocidad = random.uniform(0.1, 0.5)
        self.parpadeo = random.uniform(0.1, 0.5)
        self.brillo = random.uniform(1, 1)

    def mover(self):
        self.y += self.velocidad
        if self.y > ALTO:
            self.y = 0
            self.x = random.randint(0, ANCHO)

    def dibujar(self, pantalla):
        brillo = (self.brillo +
                  math.sin(pygame.time.get_ticks() * self.parpadeo)) / 2
        color = (int(BLANCO[0] * brillo), int(BLANCO[1]
                 * brillo), int(BLANCO[2] * brillo))
        pygame.draw.circle(pantalla, color, (self.x, self.y), self.tamano)


# Conexión a MongoDB
cliente = pymongo.MongoClient("mongodb://localhost:27017")
db = cliente["SpaceBioScope"]
collection = db["Experimentos_Mamiferos"]

# Recuperar imágenes de MongoDB y escalarlas
imagenes_recuadros = []

recuadro_ancho = 426
recuadro_alto = 240

for documento in collection.find():
    # Decodificar la imagen desde base64
    imagen_base64 = documento["Contenido_del_archivo"]
    imagen_binaria = base64.b64decode(imagen_base64)
    try:
        imagen_pil = Image.open(io.BytesIO(imagen_binaria))
        # Asegúrate de que sea RGB o RGBA
        imagen_pil = imagen_pil.convert("RGB")
        imagen_pygame = pygame.image.fromstring(
            imagen_pil.tobytes(), imagen_pil.size, imagen_pil.mode)
        imagenes_recuadros.append(imagen_pygame)
    except Exception as e:
        print("Error al cargar la imagen:", e)


def Informacion_Mamiferos(db_id):
    # Realizar la consulta con proyección para obtener solo los campos específicos
    documento = collection.find_one(
        {'_id': db_id},
        {
            "Designación": 1, "Identificador de carga útil": 1, "Titulo del proyecto": 1, "Tipo de proyecto": 1, "Programa de vuelo": 1, "Plataforma de experimentacion": 1, "Agencia patrocinadora": 1, "Centro de la NASA": 1, "Fuente de financiacion": 1, "Página_de_obtención": 1, "URL_página": 1,
            "Contenido_del_archivo": 1  # Obtener la imagen
        }
    )

    titulo = documento.get("Designación")

    # Cargar pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Información del experimento")

    # Generar estrellas
    num_estrellas = 200
    estrellas = [Estrellas() for _ in range(num_estrellas)]

    # Cargar la fuente del título del menú
    fuente_titulo = pygame.font.Font("Font/ethnocentric_rg.otf", 70)

    # Texto del título
    texto_titulo = fuente_titulo.render(titulo, True, BLANCO)
    text_titulo_rect = texto_titulo.get_rect(center=(ANCHO // 2, ALTO // 8))

    # Cargar la fuente del texto secundario
    fuente_secundaria = pygame.font.Font("Font/Xolonium-Regular.ttf", 20)

    # Crear la fuente de texto terciaria
    fuente_terciaria = pygame.font.Font("Font/A_Space_Black_Demo.otf", 30)

    # Verificar si se encontró el documento
    if documento:
        # Convertir el documento en una lista de strings para renderizarlo
        lineas_documento = [f"{key}: {
            value}" for key, value in documento.items() if key != "Contenido_del_archivo"]

        # Decodificar y cargar la imagen desde la base de datos
        imagen_base64 = documento["Contenido_del_archivo"]
        imagen_binaria = base64.b64decode(imagen_base64)
        try:
            imagen_pil = Image.open(io.BytesIO(imagen_binaria))
            # Asegúrate de que sea RGB o RGBA
            imagen_pil = imagen_pil.convert("RGB")
            imagen_pil = imagen_pil.resize((recuadro_ancho, recuadro_alto))
            imagen_pygame = pygame.image.fromstring(
                imagen_pil.tobytes(), imagen_pil.size, imagen_pil.mode)
        except Exception as e:
            print("Error al cargar la imagen:", e)
            imagen_pygame = None
    else:
        # Mensaje de error si no se encontró el documento
        lineas_documento = ["No se encontró la información del experimento."]
        imagen_pygame = None

    # Bucle para renderizar texto en dos columnas
    def render_text_lines(lineas, fuente, color, superficie, inicio_x, inicio_y, linea_altura):
        y_offset = inicio_y
        rects = []  # Lista para almacenar los rectángulos de las URL
        for line in lineas:
            clave, valor = line.split(": ", 1)
            texto_clave = fuente.render(clave, True, color)
            texto_valor = fuente.render(valor, True, color)
            texto_clave_rect = texto_clave.get_rect(
                topleft=(inicio_x, y_offset))
            texto_valor_rect = texto_valor.get_rect(
                topleft=(inicio_x + 285, y_offset))
            superficie.blit(texto_clave, texto_clave_rect)
            superficie.blit(texto_valor, texto_valor_rect)
            if clave == "URL_página":
                # Guardar rectángulo y URL para redireccionar al usuario
                rects.append((texto_valor_rect, valor))
            y_offset += linea_altura
        return rects

    # Configurar el botón "Regresar"
    fuente_boton_regresar = pygame.font.Font(None, 36)
    texto_boton_regresar = fuente_boton_regresar.render(
        "Regresar", True, BLANCO)
    boton_rect_regresar = pygame.Rect(20, (ALTO // 1.1), 120, 50)

    # Configurar el botón "Salir"
    fuente_boton_salir = pygame.font.Font(None, 36)
    texto_boton_salir = fuente_boton_salir.render("   Salir", True, BLANCO)
    boton_rect_salir = pygame.Rect((ANCHO // 1.11), (ALTO // 1.1), 120, 50)

    # Configurar el botón "Ver página"
    fuente_boton_pagina = pygame.font.Font(None, 36)
    texto_boton_pagina = fuente_boton_pagina.render("Ver página", True, BLANCO)
    boton_rect_pagina = pygame.Rect((ANCHO // 2.20), (ALTO // 1.1), 145, 50)

    # Configurar el botón "Visualizar"
    fuente_boton_visualizar = pygame.font.Font(None, 36)
    texto_boton_visualizar = fuente_boton_visualizar.render(
        "Visualizar", True, BLANCO)
    boton_rect_visualizar = pygame.Rect(
        (ANCHO // 1.3), (ALTO // 1.85), 120, 50)

    # Configurar el botón "Tabla de datos"
    fuente_boton_datos = pygame.font.Font(None, 36)
    texto_boton_datos = fuente_boton_datos.render(
        "Datos", True, BLANCO)
    boton_rect_datos = pygame.Rect(
        (ANCHO // 1.5), (ALTO // 1.85), 120, 50)

    def accion_regresar():
        from .Catalogo_Mamiferos import Catalogo_Mamiferos
        from .Carga_Informacion import Carga_Informacion
        Carga_Informacion()
        Catalogo_Mamiferos()

    def accion_salir():
        Pantalla_Final()

    def accion_visualizar(db_id):
        from Pantallas.Carga_Graficos import Carga_Graficas
        from Pantallas.Visualizacion import crear_graficas
        Carga_Graficas()
        crear_graficas(db_id)

    def accion_datos(db_id):
        from Pantallas.Tabla_Datos import visualizar_datos
        from Pantallas.Carga_Datos import Carga_Datos
        Carga_Datos()
        visualizar_datos(db_id)

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
                if evento.button == 1:  # Botón izquierdo del mouse
                    if boton_rect_regresar.collidepoint(evento.pos):
                        accion_regresar()
                    elif boton_rect_salir.collidepoint(evento.pos):
                        accion_salir()
                    elif boton_rect_visualizar.collidepoint(evento.pos):
                        accion_visualizar(db_id)
                    elif boton_rect_datos.collidepoint(evento.pos):
                        accion_datos(db_id)
                    else:
                        # Verificar si se hizo clic en la URL
                        for rect, url in render_text_lines(lineas_documento, fuente_secundaria, BLANCO, pantalla, 50, ALTO // 4, 30):
                            if rect.collidepoint(evento.pos):
                                webbrowser.open(url)

        # Dibujar el fondo
        pantalla.fill(NEGRO)

        # Dibujar estrellas
        for estrella in estrellas:
            estrella.mover()
            estrella.dibujar(pantalla)

        # Dibujar el título
        pantalla.blit(texto_titulo, text_titulo_rect)

        # Renderizar el texto del documento
        render_text_lines(lineas_documento, fuente_secundaria,
                          BLANCO, pantalla, 50, ALTO // 4, 30)

        # Dibujar imagen si se carga correctamente
        if imagen_pygame:
            pantalla.blit(imagen_pygame, (ANCHO // 1.20 -
                          recuadro_ancho // 2, ALTO // 5))

        # Dibujar botones
        pygame.draw.rect(pantalla, NEGRO, boton_rect_regresar)
        pygame.draw.rect(pantalla, NEGRO, boton_rect_salir)
        pygame.draw.rect(pantalla, NEGRO, boton_rect_pagina)
        pygame.draw.rect(pantalla, NEGRO, boton_rect_visualizar)
        pygame.draw.rect(pantalla, NEGRO, boton_rect_datos)

        pantalla.blit(texto_boton_regresar, boton_rect_regresar)
        pantalla.blit(texto_boton_salir, boton_rect_salir)
        pantalla.blit(texto_boton_pagina, boton_rect_pagina)
        pantalla.blit(texto_boton_visualizar, boton_rect_visualizar)
        pantalla.blit(texto_boton_datos, boton_rect_datos)

        pygame.display.flip()

    pygame.quit()
    sys.exit()
