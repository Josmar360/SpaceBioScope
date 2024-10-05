import pygame

def catalog_screen(screen, font):
    screen.fill((255, 255, 255))
    draw_text("Catalog", font, (0, 0, 0), screen, screen.get_width() // 2, screen.get_height() // 3)
    draw_text("Press ESC to go back to Menu", font, (0, 0, 0), screen, screen.get_width() // 2, screen.get_height() // 2)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
