import pygame
import random
import sys
from Pantallas.Advertencia import Advertencia
from Pantallas.Pantalla_Final import Pantalla_Final
from Pantallas.Informacion_Mamiferos import Informacion_Mamiferos

# Inicializar Pygame
pygame.init()

# Obtener información de la pantalla
info_pantalla = pygame.display.Info()
ANCHO, ALTO = info_pantalla.current_w, info_pantalla.current_h

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)

# Velocidad de movimiento de las estrellas
VELOCIDAD_ESTRELLAS = 0.2

# Función para generar estrellas aleatorias


def generar_estrellas():
    estrellas = []
    for _ in range(200):  # Generar 200 estrellas
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        estrellas.append((x, y))
    return estrellas

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

# Función principal


def Inicio():
    # Crear la pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
    pygame.display.set_caption("SpaceBioScope")

    # Generar estrellas aleatorias
    estrellas = generar_estrellas()

    # Cargar la fuente para el título
    fuente_titulo = pygame.font.Font("Font/Space_age.ttf", 1)

    # Texto principal (título)
    texto_titulo = fuente_titulo.render("SpaceBioScope", True, BLANCO)
    texto_titulo_rect = texto_titulo.get_rect(
        center=(ANCHO/2, ALTO/2 - 50))  # Centrar el texto en la pantalla

    # Cargar la fuente para el texto secundario
    fuente_secundaria = pygame.font.Font("Font/Nulshock_bd.otf", 20)

    # Texto secundario inicialmente transparente
    texto_secundario_alpha = 0  # Opacidad inicial del texto secundario
    texto_secundario = fuente_secundaria.render(
        "By TEAM FLDSMDFR", True, (255, 255, 255, texto_secundario_alpha))
    texto_secundario_rect = texto_secundario.get_rect(
        center=(ANCHO/2, ALTO/2 + 15))  # Centrar el texto en la pantalla

    # Variables para el efecto de zoom del texto principal
    tamano = 1
    aumento = True

    # Variables para la barra de carga
    carga_completa = False
    progreso_carga = 0
    duracion_carga = 8000  # Duración de la carga en milisegundos (8 segundos)
    ancho_barra = ANCHO
    alto_barra = 20
    pos_barra_x = 0
    pos_barra_y = ALTO - alto_barra

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
                    pygame.display.flip()
                    Pantalla_Final()

        # Mover las estrellas
        estrellas = mover_estrellas(estrellas)

        # Dibujar la pantalla
        pantalla.fill(NEGRO)

        # Dibujar las estrellas
        for estrella in estrellas:
            pygame.draw.circle(pantalla, BLANCO, estrella,
                               1)  # Dibujar estrella

        # Efecto de zoom para el texto principal
        if aumento:
            tamano += 0.1
            fuente_titulo = pygame.font.Font("Font/Space_age.ttf", int(tamano))
            texto_titulo = fuente_titulo.render(
                "SpaceBioScope", True, BLANCO)
            texto_titulo_rect = texto_titulo.get_rect(
                center=(ANCHO/2, ALTO/2 - 50))
            if tamano >= 80:  # Tamaño final del texto principal
                aumento = False

        # Mostrar el texto principal
        pantalla.blit(texto_titulo, texto_titulo_rect)

        # Efecto de aparición gradual para el texto secundario
        if not aumento:
            if texto_secundario_alpha < 255:
                texto_secundario_alpha += 1  # Aumentar gradualmente la opacidad
                texto_secundario = fuente_secundaria.render(
                    "By TEAM FLDSMDFR", True, (255, 255, 255, texto_secundario_alpha))
            # Mostrar el texto secundario
            pantalla.blit(texto_secundario, texto_secundario_rect)

            # Calcular progreso de la carga
            if not carga_completa:
                # Incrementar progreso en función del tiempo de fotograma
                progreso_carga += 1000 / 200
                if progreso_carga >= duracion_carga:
                    progreso_carga = duracion_carga
                    carga_completa = True

            # Dibujar la barra de carga
            pygame.draw.rect(pantalla, VERDE, (pos_barra_x, pos_barra_y, int(
                ancho_barra * progreso_carga / duracion_carga), alto_barra))

            # Mostrar el progreso de la carga (número y porcentaje)
            fuente_carga = pygame.font.Font(None, 24)
            texto_progreso = fuente_carga.render(
                f"Cargando: {int(progreso_carga / duracion_carga * 100)}%", True, BLANCO)
            pantalla.blit(texto_progreso, (ANCHO // 2 -
                          texto_progreso.get_width() // 2, pos_barra_y - 30))

        pygame.display.flip()

        # Cuando la carga está completa, abrir la siguiente ventana
        if carga_completa:
            Advertencia()
            break

    # Salir de Pygame
    pygame.quit()
    sys.exit()


# Ejecutar la función principal
if __name__ == "__main__":
    Inicio()