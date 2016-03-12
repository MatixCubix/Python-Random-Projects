import pygame
from random import random

gray = (200,200,200) #RGB
white = (255,255,255)
black = (0,0,0)
red = (150,0,0)
green = (0,150,0)
blue = (0,0,175)
Width = 960 #Ancho de la ventana
Height = 720 #Alto de la ventana
FPS = 60

def neg():
    u = random()
    if u < 0.5:
        return -1
    return 1

class particula:
    def __init__(self,xy,v): #a ------------ b
        self.xy = xy
        self.v = v
        
    def hit_x(self,a,b):
        if self.xy[0] >= b: 
            self.v[0] = -self.v[0]
            self.xy[0] = b - 0.001
            return [0,1]  
            
        if self.xy[0] <= a:
            self.v[0] = -self.v[0]
            self.xy[0] = a + 0.001
            return [1,0]
        return [0,0]
    
    def hit_y(self,a,b): 
        if self.xy[1] >= b:
            self.v[1] = -self.v[1]
            self.xy[1] = b - 0.001
            return [0,1]
        if self.xy[1] <= a:
            self.v[1] = -self.v[1]
            self.xy[1] = a + 0.001
            return [1,0]
        return [0,0]

class cuadrado:
    def __init__(self,a,b):
        self.a = a
        self.b = b
        self.particulas = []
        
    def generar(self,vli,n):
        self.vli = vli
        for i in range(0,n):
            vx = vli*random()*neg()
            vy = vli*random()*neg()
            x = random()
            y = random()
            x = x*(self.b-self.a)+ self.a
            y = y*(self.b-self.a)+ self.a
            u = particula([x,y],[vx,vy])
            self.particulas.append(u)

class sim:
    def __init__(self,dt,t,cuadrado):
        self.dt = dt
        self.t = t
        self.cuadrado = cuadrado
        self.particulas = cuadrado.particulas
        self.N = len(cuadrado.particulas)
        self.d = self.cuadrado.b - self.cuadrado.a
    
    def set_pygame(self):
        pygame.init()
        self.display = pygame.display.set_mode((Width,Height)) #Objeto Canvas
        pygame.display.set_caption("Display de Gas")
        self.clock = pygame.time.Clock()
        
    def update_logic(self):
        for i in range(len(self.particulas)):
            self.particulas[i].xy[0] += self.dt * self.particulas[i].v[0]
            self.particulas[i].xy[1] += self.dt * self.particulas[i].v[1]
            self.particulas[i].hit_x(self.cuadrado.a,self.cuadrado.b) # [1,0] si hit A/ [0,1] si hit B
            self.particulas[i].hit_y(self.cuadrado.a,self.cuadrado.b)
        
    def pause(self):
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    simulacion = False
                    pygame.quit()
                    self.mensaje_final()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False    
        
    def start(self):
        t = 0
        self.set_pygame()
        while t <= self.t:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    t = self.t + self.dt
                    pygame.quit()
                    input()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause()
                        
            self.display.fill(white)
            for particula in self.particulas:
                pygame.draw.circle(self.display,red,((int((particula.xy[0])*(Width/self.d))),(int((particula.xy[1])*(Height/self.d)))),3)
        
            self.clock.tick(FPS)               
            self.update_logic()
            pygame.display.update()    
            t += self.dt
        pygame.quit()
        
l = int(input("->Ingresa largo del cuadrado: "))
n = int(input("->Ingresa la cantidad de particulas a generar: "))
v = int(input("->Ingresa la velocidad limite para la generacion: "))
input("Apreta enter(Puedes ponerle pausa con P) ")
cuadrado = cuadrado(0,l)
cuadrado.generar(v,n)
sim = sim(0.001,10,cuadrado)
sim.start()
