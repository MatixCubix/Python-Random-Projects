from OpenGL.GL import *
from OpenGL.GLU import *

class triangle:
    def __init__(self,puntos,color = (0,0.7,0)):
        self.puntos = puntos
        self.color = color
    def draw(self):
        glBegin(GL_TRIANGLES)
        glColor3fv(self.color)
        for punto in self.puntos:
            glVertex3fv(punto)
        glEnd()

            
            
