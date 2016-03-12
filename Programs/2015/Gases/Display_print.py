import os
from time import sleep
from random import random

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def neg():
    u = random()
    if u < 0.5:
        return -1
    return 1

def tab():
    tab = []
    for k in range(15):
        tab.append([])
        for i in range(15):
            tab[k].append("  .  ")
    return tab

def imprimir(tab):
    for i in range(15):
        for k in range(15):
            print(tab[i][k],end="")
        print("\n")    

class particula:
    def __init__(self,xy,v): #a ------------ b
        self.xy = xy
        self.v = v
        
    def hit_x(self,a,b):
        if self.xy[0] >= b: #Colsion Lejana B
            self.v[0] = -self.v[0]
            self.xy[0] = b - 0.001 # Mejorar Esto.
            return [0,1]  
            
        if self.xy[0] <= a:#Colision Cercana A
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
        self.tab = tab()
        self.d = self.cuadrado.b - self.cuadrado.a
        
    def velocidad_promedio(self):
        u_x = 0
        u_y = 0
        u_z = 0
        for i in range(self.N):
            u_x += self.particulas[i].v[0]
            u_y += self.particulas[i].v[1]
        self.p_vx = u_x /self.N
        self.p_vy = u_y /self.N
        self.p_v =  self.p_vx + self.p_vy
        return self.p_v
        
    def start(self):
        self.colisiones = [[0,0],[0,0]] #X(a,b), Y(a,b), Z(a,b) --> A ------- B
        t = 0
        while t <= self.t:
            self.tab = tab()
            for i in range(len(self.particulas)):
                self.particulas[i].xy[0] += self.dt * self.particulas[i].v[0]
                self.particulas[i].xy[1] += self.dt * self.particulas[i].v[1]
                x = self.particulas[i].hit_x(self.cuadrado.a,self.cuadrado.b) # [1,0] si hit A/ [0,1] si hit B
                y = self.particulas[i].hit_y(self.cuadrado.a,self.cuadrado.b)
                self.colisiones[0][0] += x[0]
                self.colisiones[0][1] += x[1]
                self.colisiones[1][0] += y[0]
                self.colisiones[1][1] += y[1]
                for k in range(15):
                    if self.particulas[i].xy[0] <= (((k + 1)*(self.d))/15) +self.cuadrado.a and self.particulas[i].xy[0] >= ((k*self.d)/15) + self.cuadrado.a:
                        for w in range(15):
                            if self.particulas[i].xy[1] <= (((w + 1)*(self.d))/15)+self.cuadrado.a and self.particulas[i].xy[1] >= ((w*self.d)/15) + self.cuadrado.a:
                                self.tab[w][k] = "  O  "
            imprimir(self.tab)
            print("\n",self.particulas[0].xy,"X, Y")
            print("\n",self.particulas[0].v,"Vx, Vy")
            print("\n",self.velocidad_promedio())
            sleep(0.1)
            cls()
            t += self.dt
            
             
cuadrado = cuadrado(0,15)
cuadrado.generar(20,5)
sim = sim(0.1,10,cuadrado)
print(sim.particulas[0].xy," X,Y")
print(sim.particulas[0].v," m/s")
input()
sim.start()
print(sim.colisiones)
input()
