import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Triangle import triangle

vertices = ( #Vertices ordenados de 0 a 7
    (0,0,0),
    (1,0,0),
    (1,1,0),
    (0,1,0),
    (0,1,1),
    (1,1,1),
    (1,0,1),
    (0,0,1))

lineas =( #Lineas de el cubo indicando los vertices
    (0,1),
    (0,3),
    (0,7),
    (2,1),
    (2,3),
    (2,5),
    (6,7),
    (6,5),
    (6,1),
    (4,5),
    (4,3),
    (4,7),
    )
superficies =(
    (0,3,2,1),
    (1,6,7,0),
    (0,7,4,3),
    (3,4,5,2),
    (2,5,6,1),
    (5,4,7,6),
    )
    
colores = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,0,0),
    (1,1,1),
    (0,1,1)
    )
x = (
    (0,0,0),
    (1,0,0),
    (0.5,1,0),
    )
a = triangle(x)

def cube():
    glBegin(GL_QUADS)
    i = 0
    for superficie in superficies:
        
        for vertice in superficie:
            glColor3fv(colores[i])
            glVertex3fv(vertices[vertice])
            i += 1
        i = 0    
    glEnd()
    
    glBegin(GL_LINES)
    for linea in lineas:
        for vertice in linea:
            glVertex3fv(vertices[vertice])
    glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(50,(800/600), 0.1, 50.0)

    glTranslatef(-0,-0, -5)

    glRotatef(0,0,0,0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        matrix_pos = glGetDoublev(GL_MODELVIEW_MATRIX)        
        glRotatef(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        cube()
##        a.draw()
        pygame.display.flip()
        pygame.time.wait(10)
        
main()
    
