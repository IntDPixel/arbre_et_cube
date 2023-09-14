import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *

# Paramètres de la fenêtre Pygame
WINDOW_SIZE = (800, 600)
FRAMERATE = 60

# Paramètres de la caméra
CAMERA_DISTANCE = 10.0
CAMERA_ANGLE_X = 0.0
CAMERA_ANGLE_Y = 0.0

# Paramètres de la planète
PLANET_RADIUS = 1.0
PLANET_SEGMENTS = 32
PLANET_TEXTURE_FILE = "earth.jpg"

def load_texture(filename):
    """ Charge une texture depuis un fichier """
    surface = pygame.image.load(filename)
    texture_data = pygame.image.tostring(surface, "RGB", True)
    width, height = surface.get_rect().size
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id

def draw_sphere(radius, segments, texture_id):
    """ Dessine une sphère de rayon `radius` et avec `segments` segments """
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_TRIANGLE_STRIP)
    for j in range(segments):
        theta1 = j * 2 * pi / segments
        theta2 = (j + 1) * 2 * pi / segments
        for i in range(segments + 1):
            phi = i * pi / segments
            x = cos(theta2) * sin(phi)
            y = sin(theta2) * sin(phi)
            z = cos(phi)
            glTexCoord2f(j / segments, i / segments)
            glVertex3f(radius * x, radius * y, radius * z)
            x = cos(theta1) * sin(phi)
            y = sin(theta1) * sin(phi)
            z = cos(phi)
            glTexCoord2f((j + 1) / segments, i / segments)
            glVertex3f(radius * x, radius * y, radius * z)
    glEnd()

def main():
    # Initialisation Pygame
    pygame.init()
    pygame.display.set_mode(WINDOW_SIZE, pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("Planète 3D")

    # Chargement de la texture
    texture_id = load_texture(PLANET_TEXTURE_FILE)

    # Boucle principale
    clock = pygame.time.Clock()
    while True:
        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # Mise à jour de la caméra
        keys = pygame.key.get_pressed()
        CAMERA_ANGLE_X -= keys[pygame.K_LEFT] * 5
        CAMERA_ANGLE_X += keys[pygame.K_RIGHT] * 5
        CAMERA_ANGLE_Y -= keys[pygame.K_UP] * 5
        CAMERA_ANGLE_Y += keys[pygame.K_DOWN] * 5
        CAMERA_DISTANCE += keys[pygame.K_PAGEUP] * 0.1
