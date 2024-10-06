import pygame

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (10, 10, 50)
LIGHT_BLUE = (70, 130, 180)
GREY = (200, 200, 200)

def catalog_screen(screen, font):
    # Rellena la pantalla con un color de fondo oscuro
    screen.fill(DARK_BLUE)

    # Dibuja el título del catálogo
    draw_text("Catalog", font, LIGHT_BLUE, screen, screen.get_width() // 2, screen.get_height() // 4)

    # Dibuja la instrucción para volver al menú
    draw_text("Press ESC to go back to Menu", font, GREY, screen, screen.get_width() // 2, screen.get_height() // 2)

    # Dibuja un botón estilizado para volver al menú
    draw_button(screen, "Back to Menu", font, screen.get_width() // 2, screen.get_height() // 1.5)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)    
    surface.blit(textobj, textrect)

def draw_button(surface, text, font, x, y):
    # Dibuja un botón con bordes redondeados
    button_width, button_height = 300, 80
    button_rect = pygame.Rect(x - button_width // 2, y - button_height // 2, button_width, button_height)

    # Colores del botón
    button_color = LIGHT_BLUE
    hover_color = (100, 180, 255)

    # Dibuja el botón
    pygame.draw.rect(surface, button_color, button_rect, border_radius=15)
    draw_text(text, font, BLACK, surface, x, y)

    return button_rect  # Devuelve el rectángulo del botón

