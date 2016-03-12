import pygame
from random import random
from math import sqrt
import copy

gray = (200,205,220) #RGB
white = (255,255,255)
black = (0,0,0)
red = (150,0,0)
green = (0,150,0)
cyan = (50,100,150)
Width = 1000 #Ancho de la ventana
Height = 800 #Alto de la ventana
fontl = 25
FPS = 1000

def neg():
    u = random()
    if u < 0.5:
        return -1
    return 1

def distancia(P1,P2):
    d = sqrt(((P1[0]-P2[0])**2)+((P1[1]-P2[1])**2)+(((P1[2]-P2[2])**2)))
    return d

def energia(p):
    Ex = 0.5 * p.masa * p.v[0]**2
    Ey = 0.5 * p.masa * p.v[1]**2
    return [Ex,Ey]

def momentum(p):
    Px = p.masa * p.v[0]
    Py = p.masa * p.v[1]
    return [Px,Py]
    

class particula:
    def __init__(self,xy,v,m,r):
        self.xy = xy
        self.v = v
        self.masa = m
        self.radio = r
        
    def desplazar(self,dt):
        self.xy[0] += dt*self.v[0]
        self.xy[1] += dt*self.v[1]
        self.xy[2] += dt*self.v[2]
        
    def acelerar(self,dt,g):
        self.v[0] += dt*g[0]
        self.v[1] += dt*g[1]
        self.v[1] += dt*g[1]
        
    def wall_hit(self,A,B):
        if self.xy[0]-self.radio <= A:
            self.v[0] = -self.v[0]
            d = A-(self.xy[0]-self.radio)
            self.xy[0] += d
            return [[1,0],[0,0],[0,0]]
        elif self.xy[0]+self.radio >= B:
            self.v[0] = -self.v[0]
            d = B-(self.xy[0]+self.radio)
            self.xy[0] += d
            return [[0,1],[0,0],[0,0]]
        
        if self.xy[1]-self.radio <= A:
            self.v[1] = -self.v[1]
            d = A-(self.xy[1]-self.radio)
            self.xy[1] += d
            return [[0,0],[1,0],[0,0]]
        elif self.xy[1]+self.radio >= B:
            self.v[1] = -self.v[1]
            d = B-(self.xy[1]+self.radio)
            self.xy[1] += d
            return [[0,0],[0,1],[0,0]]    
                    
        if self.xy[2]-self.radio <= A:
            self.v[2] = -self.v[2]
            d = A-(self.xy[2]-self.radio)
            self.xy[2] += d
            return [[0,0],[0,0],[1,0]] 
        elif self.xy[2]+self.radio >= B:
            self.v[2] = -self.v[2]
            d = B-(self.xy[2]+self.radio)
            self.xy[2] += d
            return [[0,0],[0,0],[0,1]] 
            
            
    def ball_hit(self,particulas):
        for particula in particulas:
            if particula != self:
                d = distancia(self.xy,particula.xy)    
                if d <= self.radio + particula.radio:
                    vi = [copy.deepcopy(self.v[0]),copy.deepcopy(self.v[1]),copy.deepcopy(self.v[2])]
                    self.v[0] = (self.v[0] * (self.masa - particula.masa) + (2 * particula.masa * particula.v[0])) / (self.masa + particula.masa)
                    self.v[1] = (self.v[1] * (self.masa - particula.masa) + (2 * particula.masa * particula.v[1])) / (self.masa + particula.masa)
                    self.v[2] = (self.v[2] * (self.masa - particula.masa) + (2 * particula.masa * particula.v[2])) / (self.masa + particula.masa)
                    particula.v[0] += (self.masa/particula.masa)*(vi[0]-self.v[0])
                    particula.v[1] += (self.masa/particula.masa)*(vi[1]-self.v[1])
                    particula.v[2] += (self.masa/particula.masa)*(vi[2]-self.v[2])
                    e = d-(self.radio+particula.radio)
                    self.x_col = ((self.xy[0] * particula.radio) + (particula.xy[0] * self.radio)) / (particula.radio + self.radio) 
                    self.y_col = ((self.xy[1] * particula.radio) + (particula.xy[1] * self.radio)) / (particula.radio + self.radio)
                    self.z_col = ((self.xy[2] * particula.radio) + (particula.xy[2] * self.radio)) / (particula.radio + self.radio)  
                    dx = e * (self.xy[0]-self.x_col)/(self.radio)
                    dy = e * (self.xy[1]-self.y_col)/(self.radio)
                    dz = e * (self.xy[2]-self.z_col)/(self.radio)
                    self.xy[0] -= dx
                    self.xy[1] -= dy
                    self.xy[2] -= dz
                    particula.xy[0] += dx
                    particula.xy[1] += dy
                    particula.xy[2] += dz 
                    
class box:
    def __init__(self,A,B,g = [0,0],particulas = []):
        self.a = A 
        self.b = B
        self.g = g 
        self.particulas = particulas
        self.volumen = (B-A)**3
        self.area = (B-A)**2
        
    def generar(self, n, velocidad, radio, densidad):
        v_max = velocidad[0]
        v_min = velocidad[1]
        r_max = radio[0]
        r_min = radio[1]
        for i in range(0,n):
            vx = ((random()*(v_max-v_min))+v_min)*neg()
            vy = ((random()*(v_max-v_min))+v_min)*neg()
            vz = ((random()*(v_max-v_min))+v_min)*neg()
            x = random()*(self.b-self.a)+ self.a
            y = random()*(self.b-self.a)+ self.a
            z = random()*(self.b-self.a)+ self.a
            r = random()*(r_max-r_min)+ r_min
            m = r * densidad
            u = particula([x,y,z],[vx,vy,vz],m,r)
            self.particulas.append(u)        

class sim:
    def __init__(self,t,dt,box):
        self.t_sim = t
        self.dt = dt
        self.box = box
        self.particulas = box.particulas
        self.d = self.box.b - self.box.a
        self.N = len(self.particulas)
        self.colisiones = [[0,0],[0,0],[0,0]]
        
    def set_pygame(self):
        pygame.init()
        self.display = pygame.display.set_mode((Width,Height)) 
        pygame.display.set_caption("Pelotas de la Muerte")
        self.clock = pygame.time.Clock()

            
    def pause(self):
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    simulacion = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False
            
        
    def start_sim(self):
        t = 0 
        self.VxA = [] 
        self.VxB = []
        self.VyA = []
        self.VyB = []
        self.VzA = []
        self.VzB = []
        while t <= self.t_sim:
            for particula in self.particulas:
                particula.desplazar(self.dt)
                particula.acelerar(self.dt,self.box.g)
                particula.ball_hit(self.particulas)
                u = particula.wall_hit(self.box.a,self.box.b)
                for i in range(3):
                    for k in range(2):
                        self.colisiones[i][k] += u[i][k]
                if u[0][0] == 1:
                    self.VxA.append(particula.v[0])
                if u[0][1] == 1:
                    self.VxB.append(particula.v[0])
                if u[1][0] == 1:
                    self.VyA.append(particula.v[1])
                if u[1][1] == 1:
                    self.VyB.append(particula.v[1])
                if u[2][0] == 1:
                    self.VzA.append(particula.v[2])
                if u[2][1] == 1:
                    self.VzB.append(particula.v[2])
    
            t += self.dt
            
        self.colisionesT = 0 #Colisiones totales
        for i in range(3):
            for k in range(2):
                self.colisionesT += self.colisiones[i][k]
        print("\n**Simulacion Terminada**\n")
       
    def velocidad_promedio(self):
        """Determina la velocidad promedio de las particulas
           el momento que es invocado.
        """   
        u_x = 0
        u_y = 0
        u_z = 0
        for i in range(self.N):
            u_x += self.particulas[i].v[0]
            u_y += self.particulas[i].v[1]
            u_z += self.particulas[i].v[2]
        self.p_vx = u_x /self.N
        self.p_vy = u_y /self.N
        self.p_vz = u_z /self.N
        self.p_v =  self.p_vx + self.p_vy + self.p_vz
        
    def velocidad_promedio2(self):
        """Determina el promedio de las velocidades^2 de las particulas
           el momento que es invocado.
        """ 
        u_x = 0
        u_y = 0
        u_z = 0
        for i in range(self.N):
            u_x += (self.particulas[i].v[0])**2
            u_y += (self.particulas[i].v[1])**2
            u_z += (self.particulas[i].v[2])**2
        self.p_vx2 = u_x /self.N
        self.p_vy2 = u_y /self.N
        self.p_vz2 = u_z /self.N
        self.p_v2 =  self.p_vx2 + self.p_vy2 + self.p_vz2
        
    def masa_promedio(self):
        m = 0
        for particula in self.particulas:
            m += particula.masa 
        m /= self.N
        return m
        
    def presion_teorica(self):
        """Determina la presion teorica usando
           la teoria cinetica de las gases ideales.
        """ 
        self.velocidad_promedio2()
        V = self.box.volumen
        self.m = self.masa_promedio()
        v2 = self.p_v2
        self.P_teorica = (N*self.m*v2)/(3*V)
        return self.P_teorica
    
    def presion(self):
        """Determina la presion dada en una pared en
           cada unidad de tiempo(1s), y luego la promedia
           (En otras palabras es Presion/t)(note que en la
           presion teorica no se encuentra el tiempo como variable)
        """   
        VxA = sum(self.VxA)
        VxB = sum(self.VxB)
        VyA = sum(self.VyA)
        VyB = sum(self.VyB)
        VzA = sum(self.VzA)
        VzB = sum(self.VzB)
        A = self.box.area
        m = self.m
        self.PxA = (2*m*VxA)/(self.t*A)
        self.PxB = (2*m*VxB)/(self.t*A)
        self.PyA = (2*m*VyA)/(self.t*A)
        self.PyB = (2*m*VyB)/(self.t*A)
        self.PzA = (2*m*VzA)/(self.t*A)
        self.PzB = (2*m*VzB)/(self.t*A)
        self.PA = (abs(self.PxA) + abs(self.PyA) + abs(self.PzA))/3
        self.PB = (abs(self.PxB) + abs(self.PyB) + abs(self.PzA))/3
        self.P = (self.PA + self.PB)/2
        return self.P    

#----------------------------------------------------------------------------------------------------------------------------------------------------------------    
l = float(input("\n->Ingresa el largo de el cubo(m): "))
g = float(input("\n->Ingresa la gravedad de el cubo(m): "))
b = l
cubo = box(0,b,[0,g])#Esto puede ser diferente 
rmax = float(input("\n->Ingresa r max(m): "))
rmin = float(input("\n->Ingresa r min(m): "))
d = float(input("\n->Ingresa d(kg/radio): "))
N = int(input("\n->Ingresa la cantidad de particulas(Muchas pueden usar mucha memoria): "))
vmax = float(input("\n->Ingresa la velocidad maxima de las particulas(m/s): "))
vmin = float(input("\n->Ingresa la velocidad minima de las particulas(m/s): "))
cubo.generar(N,(vmax,vmin),(rmax,rmin),d)#Genera particulas
t = float(input("\n->Ingresa el tiempo de la simulacion(s): "))
dt = float(input("\n->Ingresa el largo de cada tiempo de salto(s)(0.01s es recomendado): "))
sim = sim(dt,t,cubo)
pt = sim.presion_teorica()
v2 = sim.p_v2
sim.velocidad_promedio()
print("\n->La presion teorica es de ",pt," pa")
print("\n->La velocidad promedio^2 de las particulas es de",v2,"m^2/s^2")
print("\n->La velocidad promedio de las particulas es de",sim.p_v,"m/s")
input("\n*Comenzar Simulacion(Enter):")

sim.start_sim()

print("\n*-----------------------------------------------------------------*\n")
print("la cantidad de colisiones con la pared estan dados en la lista(X(a,b),Y(a,b),Z(a,b))")
print(" ")
print(sim.colisiones)
p = sim.presion()
print(" ")
print("la presion calculada experimentalmente: ",p,"pa")
input()        
