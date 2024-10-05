import pygame
import sys

# Inicializa Pygame
pygame.init()

# Configura la pantalla
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SpaceBioScope")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fuente y tamaño
font_size = 64
font = pygame.font.Font(None, font_size)

# Función para mostrar texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Bucle principal
while True:
    # Maneja eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Rellena la pantalla con blanco
    screen.fill(WHITE)

    # Dibuja el texto en el centro de la pantalla
    draw_text("SpaceBioScope", font, BLACK, screen, screen_width // 2, screen_height // 2)

    # Actualiza la pantalla
    pygame.display.flip()
