import random
import math
import operator
import pygame


gray = (200,200,200) #RGB
white = (255,255,255)
black = (0,0,0)
red = (150,0,0)
green = (0,150,0)
blue = (0,0,175)
Width = 960
Height = 720
l = min(Width,Height) // 1.1# Largo de que de la malla en display 
x = (Width - l)//2 # Largo que separa la pantalla a la malla en el eje x
y = (Height - l)//2# Largo que separa la pantalla a la malla en el eje y
FPS = 7
fontl = 25

def neg():
    c = random.random()
    if c < 0.5:
        return -1
    return 1

class Especie:
    def __init__(self,angulo,capacidad = 0):
        self.angulo = angulo
        self.capacidad = capacidad
        
    def cross_over(self,especie):
        a = random.random()
        b = 1 - a
        angulo = self.angulo*a + especie.angulo*b
        return Especie(angulo)

    def mutacion(self,m=0.05):
        det = random.random()
        if det < m:
            u = neg()
            p = u*(360*m)
            self.angulo += p
            
    def determinar_capacidad(self,g,vi=1):
        a = (self.angulo*2*math.pi)/360
        self.capacidad = (2*math.cos(a)*math.sin(a)*(vi**2))/g

    def __str__(self):
        return str(self.angulo)

class Ambiente:
    def __init__(self,cantidad,Especies=[],g = 10):
        self.especies = Especies
        self.g = g
        self.cantidad = cantidad
            
    def generar_inicial(self):
        for i in range(self.cantidad):
            a = random.random()
            angulo = 360*a
            self.especies.append(Especie(angulo))
            
class Seleccion:
    def __init__(self,Ambiente,mortalidad,fertilidad):
        self.ambiente = Ambiente
        self.especies = Ambiente.especies
        self.mortalidad = mortalidad
        self.fertilidad = fertilidad
        self.promedio=0
        
    def det_promedio(self):
        for especie in self.especies:
            self.promedio+= especie.angulo
        self.promedio = self.promedio/len(self.especies)
        
    def determinar(self):
        self.capacidades = []
        for especie in self.especies:
            especie.determinar_capacidad(self.ambiente.g)
            self.capacidades.append([especie.capacidad,especie])  #[[3,object]]
            
    def eliminar(self):
        self.capacidades.sort(key = operator.itemgetter(0))
        factor = int(round(self.ambiente.cantidad*self.mortalidad))
        for s in range(factor):
            self.especies.remove(self.capacidades[0][1])
            self.capacidades.remove(self.capacidades[0])
            
    def generar(self):
        self.capacidades.sort(key = operator.itemgetter(0))
        factor = int(round(self.ambiente.cantidad*self.mortalidad))
        parejas = []
        while len(self.capacidades) % 2 != 0: 
            self.capacidades.remove(self.capacidades[0])
        for i in range(len(self.capacidades)//2):
            u = i*2
            parejas.append([self.capacidades[u][1],self.capacidades[u+1][1]])
            
        for pareja in parejas:
            for fertilidad in range(self.fertilidad):
                nueva_especie = pareja[1].cross_over(pareja[0])
                self.especies.append(nueva_especie)
    def mutacion(self):
        for especie in self.especies:
            especie.mutacion()


        
                
def evolucion(generaciones,mortalidad,fertilidad,cantidad,g=10):
    pygame.init()
    display = pygame.display.set_mode([Width,Height])
    font = pygame.font.SysFont(None, fontl)
    
    def message_to_screen(msg,color,x,y):
        screen_text = font.render(msg, True, color)
        display.blit(screen_text, [x,y])    
        
    pygame.display.set_caption("Nose")
    clock = pygame.time.Clock()
    gen = 0
    ambiente = Ambiente(cantidad)
    ambiente.generar_inicial()
    seleccion = Seleccion(ambiente,mortalidad,fertilidad)
    seleccion.determinar()
    simulacion = True
    while simulacion:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    simulacion = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        seleccion.determinar()
                        seleccion.eliminar()
                        seleccion.generar()
                        seleccion.mutacion()
                        seleccion.det_promedio()
                        gen += 1
        d = l/(len(ambiente.especies))
        display.fill(gray)
        display.fill(black, rect = [x,y,l,l])
        dx = x
        for especie in ambiente.especies:
            dy = (y+l)-((l*especie.angulo)/360)
            m = l+y-dy
            display.fill(white, rect = [dx,dy,d,m])
            dx += d
        message_to_screen(("Angulo del mejor: "+str(seleccion.capacidades[-1][1].angulo)),blue,((Width-(fontl*len("Angulo mejor    ")))*(5/6)),y/2)
        message_to_screen(("Gen: "+str(gen)),blue,((Width/15)),Height/2)
        message_to_screen(("Angulo Promedio: "+str(seleccion.promedio)),blue,(Width/20),Height*39/40)
        pygame.display.update()
        
evolucion(25,0.33,1,100)            
            
        
        
        
            
            
        
        
        
