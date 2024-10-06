import pygame
import sys
import random
from menu_pantalla import menu_screen  # Importa la función del menú
from catalog_pantalla import catalog_screen  # Importa la función del catálogo

# Inicializa Pygame
pygame.init()

# Configura la pantalla
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SpaceBioScope")

# Colores
BLACK = (0, 0, 0)
LIGHT_BLUE = (70, 130, 180)
GREY = (200, 200, 200)
DARK_BLUE = (10, 10, 50)

# Estados de la pantalla
PANTALLA_MENU = 0
PANTALLA_CATALOGO = 1
pantalla_actual = PANTALLA_MENU

# Fuente y tamaño
font_size = 64
font = pygame.font.Font(None, font_size)

# Generar estrellas
def draw_stars(surface, num_stars):
    for _ in range(num_stars):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        size = random.randint(1, 3)  # Tamaño aleatorio para las estrellas
        pygame.draw.circle(surface, (255, 255, 255), (x, y), size)

# Función para mostrar texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Función para dibujar un botón
def draw_button(surface, text, font, x, y):
    button_width, button_height = 300, 80
    button_rect = pygame.Rect(x - button_width // 2, y - button_height // 2, button_width, button_height)

    # Colores del botón
    button_color = LIGHT_BLUE
    hover_color = (100, 180, 255)

    # Dibuja el botón
    pygame.draw.rect(surface, button_color, button_rect, border_radius=15)
    draw_text(text, font, BLACK, surface, x, y)

    return button_rect  # Devuelve el rectángulo del botón

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

    # Rellena la pantalla con negro
    screen.fill(BLACK)

    # Dibuja las estrellas
    draw_stars(screen, 200)  # Dibuja 200 estrellas

    # Renderiza la pantalla actual
    if pantalla_actual == PANTALLA_MENU:
        draw_text("SpaceBioScope", font, LIGHT_BLUE, screen, screen_width // 2, screen_height // 4)
        button_rect = draw_button(screen, "Entrar al Catálogo", font, screen_width // 2, screen_height // 2)  # Llama a la función del menú
    elif pantalla_actual == PANTALLA_CATALOGO:
        catalog_screen(screen, font)  # Llama a la función del catálogo

    # Actualiza la pantalla
    pygame.display.flip()
