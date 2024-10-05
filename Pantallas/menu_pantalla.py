import pygame

def menu_screen(screen, font, button_color):
    screen.fill((255, 255, 255))
    draw_text("SpaceBioScope", font, (0, 0, 0), screen, screen.get_width() // 2, screen.get_height() // 3)

    # Dibuja el botón
    button_rect = pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() // 2 - 40, 300, 80)
    pygame.draw.rect(screen, button_color, button_rect)
    draw_text("Entrar al Catálogo", font, (0, 0, 0), screen, screen.get_width() // 2, screen.get_height() // 2)

    return button_rect  # Devuelve el rectángulo del botón

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
