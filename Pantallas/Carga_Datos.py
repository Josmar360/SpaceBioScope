import pygame
import random
import math
from .Pantalla_Final import Pantalla_Final

# Inicializar Pygame
pygame.init()

# Obtener información de la pantalla
info_pantalla = pygame.display.Info()
ANCHO, ALTO = info_pantalla.current_w, info_pantalla.current_h
pygame.display.set_caption("Cargado información")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
COLORES = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0),
           (0, 0, 255), (238, 130, 238)]

# Clase para crear efectos de la nebula


class Nebula:
    def __init__(self):
        self.x = random.randint(0, ANCHO)
        self.y = random.randint(0, ALTO)
        self.tamano = random.randint(2, 6)
        self.color = (random.randint(100, 255), random.randint(
            50, 200), random.randint(50, 200))
        self.velocidad = random.uniform(0.1, 0.5)

    def actualizar(self):
        self.tamano += self.velocidad
        if self.tamano > 8:
            self.tamano = random.randint(2, 6)
            self.x = random.randint(0, ANCHO)
            self.y = random.randint(0, ALTO)

    def dibujar(self, surface):
        alpha = int(255 * (8 - self.tamano) / 6)
        s = pygame.Surface((self.tamano * 2, self.tamano * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha),
                           (self.tamano, self.tamano), self.tamano)
        surface.blit(s, (self.x - self.tamano, self.y - self.tamano))


nebula_particula = [Nebula() for _ in range(100)]


def Carga_Datos():
    # Crear la pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()
    carga_completa = False
    ejecutando = True
    angulo = 0
    radio = 0

    # Variables de carga
    inicio_carga = pygame.time.get_ticks()
    duracion_carga = 4000  # Duración de la carga en milisegundos (4 segundos)

    # Bucle principal
    while ejecutando:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                    Pantalla_Final()

        # Calcular progreso de carga
        tiempo_actual = pygame.time.get_ticks()
        progreso_carga = min(tiempo_actual - inicio_carga, duracion_carga)
        carga_completa = progreso_carga == duracion_carga

        pantalla.fill(NEGRO)

        # Actualizar y dibujar partículas de la nebulosa resplandeciente
        for particula in nebula_particula:
            particula.actualizar()
            particula.dibujar(pantalla)

        # Dibujar texto de carga con efecto de zoom
        tiempo = pygame.time.get_ticks() / 500
        zoom = 1 + 0.1 * math.sin(tiempo * 2)
        fuente_zoom = pygame.font.Font(
            "Font/Best_In_Class_V.1.ttf", int(80 * zoom))
        texto = fuente_zoom.render("Cargando...", True, BLANCO)
        texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 1.1))
        pantalla.blit(texto, texto_rect)

        # Dibujar la espiral de colores
        for i, color in enumerate(COLORES):
            pygame.draw.circle(pantalla, color, (int(ANCHO // 2 + radio * math.cos(
                angulo + i * math.pi / 3)), int(ALTO // 2 + radio * math.sin(angulo + i * math.pi / 3))), 10)

        angulo += 0.08 # 0.02
        radio += 0.75 # 0.5

        # Reiniciar la espiral
        if radio > max(ANCHO, ALTO):
            radio = 0

        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(60)

        if carga_completa:
            ejecutando = False


if __name__ == "__main__":
    Carga_Datos()
