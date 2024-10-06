import pygame
import random
import math
import os
from .Pantalla_Final import Pantalla_Final

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
pantalla_info = pygame.display.Info()
ANCHO, ALTO = pantalla_info.current_w, pantalla_info.current_h
pygame.display.set_caption("Cargando catálogo")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Clase para las estrellas parpadeantes


class Estrella:
    def __init__(self):
        self.x = random.randint(0, ANCHO)
        self.y = random.randint(0, ALTO)
        self.tamano = random.randint(1, 3)
        self.velocidad = random.uniform(0.1, 0.5)
        self.parpadeo = random.uniform(0.1, 0.9)
        self.brillo = random.uniform(1, 1)

    def mover(self):
        self.y += self.velocidad
        if self.y > ALTO:
            self.y = 0
            self.x = random.randint(0, ANCHO)

    def dibujar(self, pantalla):
        brillo = (self.brillo +
                  math.sin(pygame.time.get_ticks() * self.parpadeo)) / 2
        color = (int(BLANCO[0] * brillo), int(BLANCO[1]
                 * brillo), int(BLANCO[2] * brillo))
        pygame.draw.circle(pantalla, color, (self.x, self.y), self.tamano)


def Seleccion_Imagen(Seleccion_Menu):
    case = random.randint(0, 9)
    if (Seleccion_Menu == "Mamiferos"):
        directorio_imagenes = "Imagenes/Pantalla_Carga/Mamiferos"
        imagen_carga = ["Carga_Mamifero_01.jpg", "Carga_Mamifero_02.jpg", "Carga_Mamifero_03.jpg", "Carga_Mamifero_04.jpg", "Carga_Mamifero_05.jpg",
                        "Carga_Mamifero_06.jpg", "Carga_Mamifero_07.jpg", "Carga_Mamifero_08.jpg", "Carga_Mamifero_09.jpg", "Carga_Mamifero_10.jpg", ]
    elif (Seleccion_Menu == "Semillas"):
        directorio_imagenes = "Imagenes/Menu_Principal"
        imagen_carga = ["Menu_Semillas.jpg", "Menu_Semillas.jpg", "Menu_Semillas.jpg", "Menu_Semillas.jpg", "Menu_Semillas.jpg",
                        "Menu_Semillas.jpg", "Menu_Semillas.jpg", "Menu_Semillas.jpg", "Menu_Semillas.jpg", "Menu_Semillas.jpg"]
    elif (Seleccion_Menu == "Microbianos"):
        directorio_imagenes = "Imagenes/Menu_Principal"
        imagen_carga = ["Menu_Microbiano.jpg", "Menu_Microbiano.jpg", "Menu_Microbiano.jpg", "Menu_Microbiano.jpg", "Menu_Microbiano.jpg",
                        "Menu_Microbiano.jpg", "Menu_Microbiano.jpg", "Menu_Microbiano.jpg", "Menu_Microbiano.jpg", "Menu_Microbiano.jpg"]
    elif (Seleccion_Menu == "Humanos"):
        directorio_imagenes = "Imagenes/Menu_Principal"
        imagen_carga = ["Menu_Humano.jpeg", "Menu_Humano.jpeg", "Menu_Humano.jpeg", "Menu_Humano.jpeg", "Menu_Humano.jpeg",
                        "Menu_Humano.jpeg", "Menu_Humano.jpeg", "Menu_Humano.jpeg", "Menu_Humano.jpeg", "Menu_Humano.jpeg"]
    return os.path.join(directorio_imagenes, imagen_carga[case])


def Carga_Catalogo(Seleccion_Menu):
    # Variables locales en lugar de globales
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()
    carga_completa = False
    ejecutando = True

    # Variables para la carga
    inicio_carga = pygame.time.get_ticks()
    duracion_carga = 4000  # Duración de la carga en milisegundos (4 segundos)

    # Generar estrellas
    num_estrellas = 200
    estrellas = [Estrella() for _ in range(num_estrellas)]

    # Cargar la imagen y redimensionarla
    imagen = pygame.image.load(Seleccion_Imagen(Seleccion_Menu))
    nuevo_ancho, nuevo_alto = 640, 360  # Nuevas dimensiones
    imagen = pygame.transform.scale(imagen, (nuevo_ancho, nuevo_alto))
    imagen_rect = imagen.get_rect(center=(ANCHO // 2, ALTO // 2))

    while ejecutando:
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

        # Dibujar fondo y estrellas
        pantalla.fill(NEGRO)
        for estrella in estrellas:
            estrella.mover()
            estrella.dibujar(pantalla)

        # Aplicar movimiento suave a la imagen
        offset_x = 100 * math.cos(pygame.time.get_ticks() / 500)
        offset_y = 5 * math.sin(pygame.time.get_ticks() / 500)

        # Dibujar imagen que se revela de izquierda a derecha
        ancho_revelado = int(
            (progreso_carga / duracion_carga) * imagen_rect.width)
        if 0 < ancho_revelado <= imagen_rect.width:
            imagen_cortada = imagen.subsurface(
                (0, 0, ancho_revelado, imagen_rect.height))
            pantalla.blit(imagen_cortada, (imagen_rect.x +
                          offset_x, imagen_rect.y + offset_y))

        # Dibujar texto de carga con efecto de zoom
        tiempo = pygame.time.get_ticks() / 500
        zoom = 1 + 0.1 * math.sin(tiempo * 2)
        fuente_zoom = pygame.font.Font(
            "Font/Best_In_Class_V.1.ttf", int(80 * zoom))
        texto = fuente_zoom.render("Cargando...", True, BLANCO)
        texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 1.1))
        pantalla.blit(texto, texto_rect)

        pygame.display.flip()
        reloj.tick(60)

        if carga_completa:
            ejecutando = False


if __name__ == "__main__":
    Carga_Catalogo()
