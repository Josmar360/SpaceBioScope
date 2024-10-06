import pygame
import random
import sys
from .Carga_Catalogo import Carga_Catalogo
from .Pantalla_Final import Pantalla_Final
from .Catalogo_Mamiferos import Catalogo_Mamiferos

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
    for _ in range(600):  # Generar 600 estrellas
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

# Funciones para las acciones de los recuadros

def accion_mamiferos():
    Carga_Catalogo("Mamiferos")
    Catalogo_Mamiferos()
    print("Acción personalizada para mamiferos")

def accion_semillas():
    Carga_Catalogo("Semillas")
    print("Acción personalizada para semillas")


def accion_microbianos():
    Carga_Catalogo("Microbianos")
    print("Acción personalizada para microbiano")


def accion_humanos():
    Carga_Catalogo("Humanos")
    print("Acción personalizada para humanos")


def accion_informacion():
    print("Acción personalizada para informacion")


def accion_ayuda():
    print("Acción personalizada para ayuda")


def Menu_Principal():
    # Crear la pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Menu Principal")

    # Generar estrellas aleatorias
    estrellas = generar_estrellas()

    # Cargar la fuente del título del menú
    fuente_titulo = pygame.font.Font("Font/13_Misa.ttf", 160)

    # Texto del título
    texto_titulo = fuente_titulo.render("Menu Principal", True, BLANCO)
    texto_titulo_rect = texto_titulo.get_rect(
        center=(ANCHO/2, ALTO/4.5))  # Centrar el texto

    # Cargar la fuente para los textos de los recuadros
    fuente_recuadros = pygame.font.Font("Font/OriginTech_personal_use.ttf", 28)

    # Lista de textos para los recuadros
    textos_recuadros = ["Mamíferos", "Semillas",
                        "Microbianos", "Humanos", "Información", "Ayuda"]

    # Imágenes para los recuadros
    imagenes_recuadros = [pygame.image.load("Imagenes/Menu_Principal/Menu_Maniferos.jpg").convert_alpha(),
                          pygame.image.load(
                              "Imagenes/Menu_Principal/Menu_Semillas.jpg").convert_alpha(),
                          pygame.image.load(
                              "Imagenes/Menu_Principal/Menu_Microbiano.jpg").convert_alpha(),
                          pygame.image.load(
                              "Imagenes/Menu_Principal/Menu_Humano.jpeg").convert_alpha(),
                          pygame.image.load(
                              "Imagenes/Menu_Principal/Menu_Informacion.jpg").convert_alpha(),
                          pygame.image.load("Imagenes/Menu_Principal/Menu_Ayuda.jpg").convert_alpha()]

    # Rectángulos interactivos
    recuadro_ancho = 250
    recuadro_alto = 150
    espacio_entre_recuadros = 100
    recuadro_y = ALTO // 2.5
    recuadros = []

    # Definir las acciones para cada recuadro
    acciones_recuadros = [accion_mamiferos, accion_semillas, accion_microbianos,
                          accion_humanos, accion_informacion, accion_ayuda]

    for i in range(4):
        recuadro_x = (ANCHO - (3.75 * (recuadro_ancho + espacio_entre_recuadros))
                      ) // 2 + i * (recuadro_ancho + espacio_entre_recuadros)
        recuadro = pygame.Rect(recuadro_x, recuadro_y,
                               recuadro_ancho, recuadro_alto)
        recuadros.append(recuadro)

    # Añadir dos recuadros más en una fila inferior a la principal
    recuadro_y += recuadro_alto + espacio_entre_recuadros
    for i in range(2):
        recuadro_x = (ANCHO - (1.5 * (recuadro_ancho + espacio_entre_recuadros))
                      ) // 2 + i * (recuadro_ancho + espacio_entre_recuadros)
        recuadro = pygame.Rect(recuadro_x, recuadro_y,
                               recuadro_ancho, recuadro_alto)
        recuadros.append(recuadro)

    # Configurar el botón "Salir"
    fuente_boton_salir = pygame.font.Font(None, 36)
    texto_boton_salir = fuente_boton_salir.render("   Salir", True, BLANCO)
    boton_rect_salir = pygame.Rect((ANCHO // 1.11), (ALTO // 1.12), 120, 50)

    def accion_salir():
        Pantalla_Final()

    # Bucle principal
    ejecutando = True
    while ejecutando:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                    Pantalla_Final()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botón izquierdo del ratón
                    for i, recuadro in enumerate(recuadros):
                        if recuadro.collidepoint(evento.pos):
                            # Ejecutar la acción correspondiente al recuadro
                            acciones_recuadros[i]()
                    if boton_rect_salir.collidepoint(evento.pos):
                        accion_salir()

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
            pantalla.blit(imagenes_recuadros[i], recuadro)
            texto_recuadro = fuente_recuadros.render(
                textos_recuadros[i], True, BLANCO)
            texto_recuadro_rect = texto_recuadro.get_rect(
                center=(recuadro.centerx, recuadro.bottom + 20))
            pantalla.blit(texto_recuadro, texto_recuadro_rect)

            # Dibujar el botón "Salir"
            pygame.draw.rect(pantalla, BLANCO, boton_rect_salir, 2)
            pantalla.blit(texto_boton_salir, boton_rect_salir.move(10, 10))

        pygame.display.flip()

    # Salir de Pygame
    pygame.quit()
    sys.exit()


# Ejecutar la función principal
if __name__ == "__main__":
    Menu_Principal()
