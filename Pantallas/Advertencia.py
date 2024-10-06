import pygame
import sys
import random
from .Menu_Principal import Menu_Principal
from .Pantalla_Final import Pantalla_Final


# Inicializar Pygame
pygame.init()

# Obtener información de la pantalla
info_pantalla = pygame.display.Info()
ANCHO, ALTO = info_pantalla.current_w, info_pantalla.current_h

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Clase para una partícula de la nebulosa


class ParticulaNebulosa:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.randint(100, 255), random.randint(
            100, 200), random.randint(150, 255))
        self.radio = random.randint(1, 3)
        self.velocidad = random.uniform(0.1, 0.5)

    def mover(self):
        self.x += random.uniform(-self.velocidad, self.velocidad)
        self.y += random.uniform(-self.velocidad, self.velocidad)
        if self.x < 0:
            self.x = ANCHO
        elif self.x > ANCHO:
            self.x = 0
        if self.y < 0:
            self.y = ALTO
        elif self.y > ALTO:
            self.y = 0

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color,
                           (int(self.x), int(self.y)), self.radio)

# Generar partículas de la nebulosa


def generar_nebulosa(cantidad):
    nebulosa = []
    for _ in range(cantidad):
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        nebulosa.append(ParticulaNebulosa(x, y))
    return nebulosa

# Bucle principal de la función de nebulosa


def efecto_nebulosa():
    # Crear la pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Advertencia de uso")

    # Generar partículas de la nebulosa
    particulas_nebulosa = generar_nebulosa(500)

    # Bucle principal
    ejecutando = True
    while ejecutando:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q or evento.key == pygame.K_ESCAPE:
                    Pantalla_Final()
                    ejecutando = False

        # Dibujar la pantalla de nebulosa
        pantalla.fill(NEGRO)

        # Mover y dibujar las partículas de la nebulosa
        for particula in particulas_nebulosa:
            particula.mover()
            particula.dibujar(pantalla)

        pygame.display.flip()

    # Salir de Pygame
    pygame.quit()
    sys.exit()


# Texto de advertencia
Texto_Advertencia = [
    "Este programa, SpaceBioScope, es una creación propia desarrollada",
    "por TEAM FLDSMDFR con fines educativos y de aprendizaje personal.",
    "Las visualizaciones generadas en este programa han sido diseñadas",
    "exclusivamente por el equipo, utilizando datos de los experimentos",
    "realizados en la Estación Espacial Internacional, incluyendo OSD-379",
    "y OSD-665.",
    "",
    "Los datos utilizados en este programa han sido obtenidos de fuentes",
    "oficiales de la NASA y están destinados para fines educativos",
    "y no comerciales. Todos los derechos son reservados y este programa",
    "no está afiliado, patrocinado ni respaldado por la NASA.",
    "",
    "Se prohíbe la reproducción, distribución o uso comercial de este programa",
    "sin el consentimiento expreso de TEAM FLDSMDFR. Al utilizar este programa,",
    "aceptas que el contenido se presenta tal cual y que el equipo no se",
    "responsabiliza por cualquier daño o perjuicio derivado del uso de este software."
]

# Bucle principal de la función de advertencia


def Advertencia():
    # Crear pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Advertencia de uso.")

    # Cargar fuente del texto en pantalla
    fuente_titulo = pygame.font.Font("Font/Nulshock_bd.otf", 70)

    # Texto del título
    texto_titulo = fuente_titulo.render("Advertencia de uso:", True, BLANCO)
    texto_titulo_rect = texto_titulo.get_rect(
        center=(ANCHO/2, ALTO/4.5))  # Centrar el texto

    # Generar partículas de la nebulosa
    particulas_nebulosa = generar_nebulosa(500)

    # Cargar la fuente del texto de advertencia
    fuente_secundaria = pygame.font.Font("Font/PROXON.ttf", 25)

    # Variables para posible barra de carga
    carga_completa = False
    inicio_carga = pygame.time.get_ticks()  # Tiempo de inicio de carga
    # Duración de la carga en milisegundos (4 segundos)
    duracion_carga = 4000

    # Bucle principal
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    Pantalla_Final()
                    ejecutando = False

        # Calcular progreso de la carga
        tiempo_actual = pygame.time.get_ticks()
        progreso_carga = tiempo_actual - inicio_carga
        if progreso_carga >= duracion_carga:
            carga_completa = True

        # Dibujar la pantalla
        pantalla.fill(NEGRO)

        # Dibujar las partículas de la nebulosa
        for particula in particulas_nebulosa:
            particula.mover()
            particula.dibujar(pantalla)

        # Dibujar el título
        pantalla.blit(texto_titulo, texto_titulo_rect)

        # Dibujar el texto de advertencia
        for i, linea in enumerate(Texto_Advertencia):
            texto_linea_render = fuente_secundaria.render(linea, True, BLANCO)
            texto_linea_rect = texto_linea_render.get_rect(
                topleft=(ANCHO/2 - 515, ALTO/2 - 100 + i * 20))
            pantalla.blit(texto_linea_render, texto_linea_rect)

        pygame.display.flip()

        if carga_completa:
            ejecutando = False
            Menu_Principal()

    # Salir de Pygame
    pygame.quit()
    sys.exit()


# Ejecutar la función principal
if __name__ == "__main__":
    Advertencia()
