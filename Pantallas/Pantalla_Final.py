import pygame
import random
import math
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
pantalla_info = pygame.display.Info()
ANCHO, ALTO = pantalla_info.current_w, pantalla_info.current_h
pygame.display.set_caption("Pantalla Final")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
PURPURA = (128, 0, 128)
CYAN = (0, 255, 255)

# Crear un grupo de partículas de explosión
numero_particulas = 2000
particulas = []
for _ in range(numero_particulas):
    angulo = random.uniform(0, 2 * math.pi)
    velocidad = random.uniform(2, 6)
    radio = 0
    tamano = random.randint(1, 3)
    color = random.choice([BLANCO, AZUL, PURPURA, CYAN])
    particulas.append([angulo, velocidad, radio, tamano, color])


def Pantalla_Final():
    # Variables para centro de la pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()
    carga_completa = False
    ejecutando = True

    # Variables para la carga
    inicio_carga = pygame.time.get_ticks()
    duracion_carga = 6000  # Duración de la carga en milisegundos (6 segundos)

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q or evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                    pygame.quit()
                    sys.exit()

        # Dibujar fondo
        pantalla.fill(NEGRO)

        # Mover y dibujar partículas de la explosión
        for particula in particulas:
            particula[2] += particula[1]
            x = int((ANCHO // 2) + particula[2] * math.cos(particula[0]))
            y = int((ALTO // 2) + particula[2] * math.sin(particula[0]))

            if x < 0 or x > ANCHO or y < 0 or y > ALTO:
                angulo = random.uniform(0, 2 * math.pi)
                velocidad = random.uniform(2, 6)
                radio = 0
                tamano = random.randint(1, 3)
                color = random.choice([BLANCO, AZUL, PURPURA, CYAN])
                particula[:] = [angulo, velocidad, radio, tamano, color]

            pygame.draw.circle(pantalla, particula[4], (x, y), particula[3])

        # Calcular progreso de carga
        tiempo_actual = pygame.time.get_ticks()
        progreso_carga = min(tiempo_actual - inicio_carga, duracion_carga)
        carga_completa = progreso_carga == duracion_carga

        # Dibujar texto de carga efecto de zoom
        tiempo = pygame.time.get_ticks() / 500
        zoom = 1 + 0.1 * math.sin(tiempo * 2)
        fuente_zoom = pygame.font.Font("Font/galaxy_1.ttf", int(80 * zoom))
        texto = fuente_zoom.render("Hasta la próxima", True, BLANCO)
        texto_rect = texto.get_rect(
            center=(ANCHO // 2.4, ALTO // 2.3))
        pantalla.blit(texto, texto_rect)

        zoom_secundario = 1 + 0.1 * math.sin(tiempo * 2)
        fuente_zoom_secundario = pygame.font.Font(
            "Font/galaxy_1.ttf", int(80 * zoom_secundario))
        texto_secundario = fuente_zoom_secundario.render(
            "misión visual.", True, BLANCO)
        texto_rect_secundario = texto_secundario.get_rect(
            center=(ANCHO // 1.5, ALTO // 1.7))
        pantalla.blit(texto_secundario, texto_rect_secundario)

        pygame.display.flip()
        reloj.tick(60)

        if carga_completa:
            ejecutando = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    Pantalla_Final()
