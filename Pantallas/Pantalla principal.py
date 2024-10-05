import pygame
import sys
from menu_pantalla import menu_screen
from catalog_pantalla import catalog_screen

# Inicializa Pygame
pygame.init()

# Configura la pantalla
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SpaceBioScope")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Estados de la pantalla
PANTALLA_MENU = 0
PANTALLA_CATALOGO = 1
pantalla_actual = PANTALLA_MENU

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
        if event.type == pygame.KEYDOWN:
            if pantalla_actual == PANTALLA_CATALOGO and event.key == pygame.K_ESCAPE:  # Regresa al menú
                pantalla_actual = PANTALLA_MENU
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pantalla_actual == PANTALLA_MENU:
                mouse_pos = event.pos  # Obtiene la posición del mouse
                if button_rect.collidepoint(mouse_pos):  # Verifica si se hizo clic en el botón
                    pantalla_actual = PANTALLA_CATALOGO

    # Rellena la pantalla con blanco
    screen.fill(WHITE)

    # Renderiza la pantalla actual
    if pantalla_actual == PANTALLA_MENU:
        button_rect = menu_screen(screen, font, GREEN)  # Llama a la función del menú
    elif pantalla_actual == PANTALLA_CATALOGO:
        catalog_screen(screen, font)  # Llama a la función del catálogo

    # Actualiza la pantalla
    pygame.display.flip()
