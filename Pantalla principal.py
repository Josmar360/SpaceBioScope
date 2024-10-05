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

# Función para manejar la pantalla del menú
def menu_screen():
    screen.fill(WHITE)
    draw_text("SpaceBioScope", font, BLACK, screen, screen_width // 2, screen_height // 3)
    
    # Dibuja el botón
    button_rect = pygame.Rect(screen_width // 2 - 500, screen_height // 1.3 - 40, 300, 80)
    pygame.draw.rect(screen, GREEN, button_rect)
    draw_text("Catálogo", font, BLACK, screen, screen_width // 2- 400, screen_height // 1.3)

    return button_rect  # Devuelve el rectángulo del botón

# Función para manejar la pantalla del catálogo
def catalog_screen():
    screen.fill(WHITE)
    draw_text("Catalog", font, BLACK, screen, screen_width // 2, screen_height // 3)
    draw_text("[Esc]", font, BLACK, screen, screen_width // 2, screen_height // 2)

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

    # Renderiza la pantalla actual
    if pantalla_actual == PANTALLA_MENU:
        button_rect = menu_screen()  # Guarda el rectángulo del botón
    elif pantalla_actual == PANTALLA_CATALOGO:
        catalog_screen()

    # Actualiza la pantalla
    pygame.display.flip()
