from random import random

def neg():
    u = random()
    if u < 0.5:
        return -1
    return 1

class particula:
    """ particula Infinitesimalmente chica que tiene como atributos
        la posicion xyz, su masa, y su velocidad[Vx,Vy,Vz].
        
        Tiene como metodos la deteccion de colision con paredes
        de largo b-a. 
    """    
       
    def __init__(self,xyz,m,v): #a ------------ b
        self.xyz = xyz
        self.m = m
        self.v = v
        
    def hit_x(self,a,b):
        """ Funcion que permite detectar
            si la particula self a colisionado
            con la pared en X, retorna una lista
            indicando en que pared choco, ademas
            asume que es una colsion elastica y
            cambia el sentido de la velocidad.
        """    
        if self.xyz[0] >= b: 
            self.v[0] = -self.v[0]
            self.xyz[0] = b - 0.001 
            return [0,1]  
            
        if self.xyz[0] <= a:
            self.v[0] = -self.v[0]
            self.xyz[0] = a + 0.001
            return [1,0]
        return [0,0]
    
    def hit_y(self,a,b):
        """ Lo mismo pero en Y.
        """  
        if self.xyz[1] >= b:
            self.v[1] = -self.v[1]
            self.xyz[1] = b - 0.001
            return [0,1]
        if self.xyz[1] <= a:
            self.v[1] = -self.v[1]
            self.xyz[1] = a + 0.001
            return [1,0]
        return [0,0]
    
    def hit_z(self,a,b):
        """ Lo mismo pero en Z.
        """
        if self.xyz[2] >= b:
            self.v[2] = -self.v[2]
            self.xyz[2] = b - 0.001        
            return [0,1]
        if self.xyz[2] <= a:
            self.v[2] = -self.v[2]
            self.xyz[2] = a + 0.001
            return [1,0] 
        return [0,0]
    
class cubo:
    """ Cubo de lado b-a, que
        contiene instancias de objetos particula.

        Tiene la capacidad de generar particulas aleatorias.
    """    
        
    def __init__(self,a,b,particulas = []):
        self.a = a
        self.b = b
        self.particulas = particulas
        self.volumen = (b-a)**3
        self.area = (b-a)**2
        
    def generar(self,vli,m,n):
        """ Genera aleatoriamente n particulas
            de masa m y con velocidad maxima de vli.
        """
        self.vli = vli
        for i in range(0,n):
            vx = vli*random()*neg()
            vy = vli*random()*neg()
            vz = vli*random()*neg()
            x = random()
            y = random()
            z = random()
            x = x*(self.b-self.a)+ self.a
            y = y*(self.b-self.a)+ self.a
            z = z*(self.b-self.a)+ self.a
            u = particula([x,y,z],m,[vx,vy,vz])
            self.particulas.append(u)

class sim:
    """ Simulacion que tiene como atributos
        un objeto cubo(Que ademas contiene objetos particula)
        el tiempo de simulacion t, y los saltos de tiempo dt.

        Contiene diversos metodos, como el start que permite que
        se corra una simulacion, y varios que calculan la presion
        teorica y la experimental usando metodos de promedio.
    """    
       
    def __init__(self,dt,t,cubo): 
        self.dt = dt
        self.t = t
        self.cubo = cubo
        self.particulas = cubo.particulas
        self.N = len(cubo.particulas)
        
    def start(self):
        """ Empeiza la simulacion en el cubo y registra
            la cantidad de colisiones.  
        """
        self.colisiones = [[0,0],[0,0],[0,0]] #X(a,b), Y(a,b), Z(a,b) --> A ------- B
        t = 0 
        self.VxA = [] #Listas que indican que particulas han chocado con la pared(pueden repetirse)
        self.VxB = []
        self.VyA = []
        self.VyB = []
        self.VzA = []
        self.VzB = []
        while t <= self.t:
            for i in range(len(self.particulas)):
                self.particulas[i].xyz[0] += self.dt * self.particulas[i].v[0]
                self.particulas[i].xyz[1] += self.dt * self.particulas[i].v[1]
                self.particulas[i].xyz[2] += self.dt * self.particulas[i].v[2]
                x = self.particulas[i].hit_x(self.cubo.a,self.cubo.b) # [1,0] si hit A/ [0,1] si hit B
                y = self.particulas[i].hit_y(self.cubo.a,self.cubo.b)
                z = self.particulas[i].hit_z(self.cubo.a,self.cubo.b)
                self.colisiones[0][0] += x[0]
                self.colisiones[0][1] += x[1]
                self.colisiones[1][0] += y[0]
                self.colisiones[1][1] += y[1]
                self.colisiones[2][0] += z[0]
                self.colisiones[2][1] += z[1]
                if x[0] == 1:#Debido a esto la cantidad de memoria usada es mayor en cada unidad de tiempo. 
                    self.VxA.append(self.particulas[i].v[0])
                if x[1] == 1:
                    self.VxB.append(self.particulas[i].v[0])
                if y[0] == 1:
                    self.VyA.append(self.particulas[i].v[1])
                if y[1] == 1:
                    self.VyB.append(self.particulas[i].v[1])
                if z[0] == 1:
                    self.VzA.append(self.particulas[i].v[2])
                if z[1] == 1:
                    self.VzB.append(self.particulas[i].v[2])
            t += self.dt
            
        self.colisionesT = 0 #Colisiones totales
        for i in range(3):
            for k in range(2):
                self.colisionesT += self.colisiones[i][k]

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
        
    def presion_teorica(self):
        """Determina la presion teorica usando
           la teoria cinetica de las gases ideales.
        """ 
        self.velocidad_promedio2()
        V = self.cubo.volumen
        m = self.particulas[0].m
        N = self.N
        v2 = self.p_v2
        self.P_teorica = (N*m*v2)/(3*V)
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
        A = self.cubo.area
        m = self.particulas[0].m
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
    
    def factor(self):
        """Determina un factor de computo arbitrario
        """
        f = (self.N*self.t)/self.dt
        return f    

    def temperatura(self):
        """Determina la temperatura usando
           la teoria cinetica de los gases
        """     
        kb = 1.3806504e-23
        m = self.particulas[0].m
        v2 = self.p_v2
        T = (m*v2)/(kb*3)
        return T
#----------------------------------------------------------------------------------------------------------------------------------------------------------------    
l = float(input("\n->Ingresa el largo de el cubo(m): "))
b = l
cubo = cubo(0,b)#Esto puede ser diferente 
m = float(input("\n->Ingresa masa de las particulas(kg): "))
N = int(input("\n->Ingresa la cantidad de particulas(Muchas pueden usar mucha memoria): "))
vli = float(input("\n->Ingresa la velocidad maxima de las particulas(m/s): "))
cubo.generar(vli,m,N)#Genera particulas
t = float(input("\n->Ingresa el tiempo de la simulacion(s): "))
dt = float(input("\n->Ingresa el largo de cada tiempo de salto(s)(0.01s es recomendado): "))
sim = sim(dt,t,cubo)
pt = sim.presion_teorica()
v2 = sim.p_v2
sim.velocidad_promedio()
print("\n->La presion teorica es de ",pt," pa")
print("\n->La temperatura teorica es de",sim.temperatura()," K")
print("\n->La velocidad promedio^2 de las particulas es de",v2,"m^2/s^2")
print("\n->La velocidad promedio de las particulas es de",sim.p_v,"m/s")
print("\n->El Factor de computo es de",sim.factor())
input("\n*Comenzar Simulacion(Enter):")

sim.start()

print("\n*-----------------------------------------------------------------*\n")
print("la cantidad de colisiones con la pared estan dados en la lista(X(a,b),Y(a,b),Z(a,b))")
print(" ")
print(sim.colisiones)
p = sim.presion()
print(" ")
print("la presion calculada experimentalmente: ",p,"pa")
input()

#Seria interesante ver como cambia esto si se le agrega gravedad, o si se cambia el contenedor, o si las particulas colisionaran entre ellas.

