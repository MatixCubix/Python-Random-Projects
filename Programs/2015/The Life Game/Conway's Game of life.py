from random import randint
from random import choice
import pygame
import copy

pygame.init()
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
n = 150 # Numero de celulas en el lado 
fontl = 25 # Tamaño de la fuente
max_r = 500 #Recusiones max
direcciones = [[1,0],[0,1],[1,1],[-1,0],[0,-1],[-1,-1],[1,-1],[-1,1]]

class The_life_game:
    def __init__(self,initial,n = 15):
        self.celulas = []
        self.initial = initial #[[2,3],[2,5],[4,2]], [2,3] indica en X = 2 e Y = 3 viva
        self.n = n
        
    def generate_cells(self): #Genera malla de celulas muertas, [(x = 0)[0,0,(y = 2)0,0,0,0,0],(x = 1)[0,0,0,0,0,0,0]]
        for k in range(self.n):
            self.celulas.append([])
            for i in range(self.n):
                self.celulas[k].append(0)
        
    def mod(self):# celulas[X][Y], input del usuario, jugada inicial
        for i in self.initial:
            x = i[0]
            y = i[1]
            if out(x,y,self.n) == True:
                pass
            else:
                self.celulas[x][y] = 1
                
    def vivas(self): #Devuelve lista de posicion de vivas
        self.posicion_vivas = []
        for i in range(len(self.celulas)): #Busca vivas
            for k in range(len(self.celulas[i])):
                if self.celulas[i][k] == 1:
                    self.posicion_vivas.append([i,k])
                    
    def vecinos(self): #Devuelve lista de listas de posicion de vecinos(8 max por celula viva)
        self.L_vecinos = []
        for i in range(len(self.posicion_vivas)):
            self.L_vecinos.append([self.posicion_vivas[i],[]])
            for k in range(len(direcciones)):
                u = self.posicion_vivas[i][0] + direcciones[k][0]
                v = self.posicion_vivas[i][1] + direcciones[k][1]
                if out(u,v,self.n) == False:
                    self.L_vecinos[i][1].append([u,v])#([[2,3],[[2,2],[3,2]]],[[5,3],[[4,2],[3,2]]])
#for x in neightuple:
#   cont+= cel((i+x(0))%len_x)((j+x(1))%len_y)
                    
    def vecinosU(self):#Devuelve lista de vecinos pero de todos
        self.L_vecinosU = []
        for i in range(len(self.L_vecinos)):
            for k in range(len(self.L_vecinos[i][1])):
                self.L_vecinosU.append(self.L_vecinos[i][1][k])     
                    
    def repeticiones(self):# Determina numero de repeticiones en vecinosU y las asigna a una lista
        self.L_repeticiones = []
        for i in range(len(self.L_vecinosU)):
            u = self.L_vecinosU.count(self.L_vecinosU[i])
            if self.L_repeticiones.count([self.L_vecinosU[i],u]) == 0:
                self.L_repeticiones.append([self.L_vecinosU[i],u])
             
                    
    def revivir(self):#Busca si hay mas de 3 vecinos relativos en algun punto en el tablero de celulas muertas, las agrega a una lista de la forma [[2,3],[2,5]]
        self.L_revivir = []
        for i in self.L_repeticiones:
            x = i[0][0]
            y = i[0][1]
            if i[1] == 3 and self.celulas[x][y] == 0:
                self.L_revivir.append([x,y])

    def matar(self):# Mata celulas 
        self.L_matar = []
        for i in self.L_vecinos: # i toma [[2,3],[[2,4],[2,5],[1,4]]] por ej
            v = 0 #Vivas 
            for k in range(len(i[1])): #Largo vecinos de la celula i[0]
                if self.celulas[i[1][k][0]][i[1][k][1]] == 1:
                    v += 1
            if v == 2 or v == 3:#vive
                pass
            else:#muere
                self.L_matar.append(i[0])
                
    def aplicar(self):#aplica cambios de matar() y revivir()
        for i in range(len(self.L_matar)):
            x = self.L_matar[i][0]
            y = self.L_matar[i][1]
            self.celulas[x][y] = 0
        for i in range(len(self.L_revivir)):
            x = self.L_revivir[i][0]
            y = self.L_revivir[i][1]
            self.celulas[x][y] = 1
            
    def cambio(self,i,f):#Compara en el lapso de 1n
        self.dvdn = f - i

    def mensaje_final(self):
        print("\n**Simulacion Terminada**")
        Q = input("\nQuieres guardar la jugada? ")
        if Q.upper() == "SI":
            jugadas = open("Jugadas_aleatorias.txt","a")
            a = "\nN = "+ str(self.N) 
            jugadas.write(str(self.initial))
            jugadas.write(a)
            jugadas.write("\n--------------------------------------------------------------------\n") 
            jugadas.close()      
        input("\nEnter para salir.")
        quit()

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
        
    def start(self,end = False):
       #
        def message_to_screen(msg,color,x,y):#def funcion que imprime en pantalla
            screen_text = font.render(msg, True, color)
            Display.blit(screen_text, [x,y]) #Posicion
        
        def update_logic():#
            a = copy.deepcopy(self.posicion_vivas)
            a = len(a)
            #-----------------------
            self.vivas()
            self.vecinos()
            self.vecinosU()
            self.repeticiones()
            self.revivir()
            self.matar()
            self.aplicar()
            #------------------------
            b = len(self.posicion_vivas)
            self.cambio(b,a)
        #   
        Display = pygame.display.set_mode((Width,Height)) #Objeto Canvas
        pygame.display.set_caption("Conway's Game Of Life")
        self.generate_cells()#Generar malla
        self.mod()#Insertar jugada
        self.vivas()
        self.N = 0#Definir N inicial
        simulacion = True
        clock = pygame.time.Clock()#Objeto Clock
        font = pygame.font.SysFont(None, fontl)#Objeto font
        d = l / self.n #Definir distancia entre celulas
        self.dvdn = 0 #Definir cambio de vida (variable temporal)
        
        while simulacion:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    simulacion = False
                    pygame.quit()
                    self.mensaje_final()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause()
                        
            #---------------------------------------------------------------------------            
            Display.fill(gray)
            Display.fill(black, rect = [x,y,l,l])
            message_to_screen(str(self.N),blue,(Width-l-(3*x/2)),(Height - (y/2)))
            message_to_screen("Conway's Game Of Life",blue,((Width-(fontl*len("Conway's Game Of Life")))*(5/6)),y/2)
            message_to_screen(("Vivas: "+str(len(self.posicion_vivas))),blue,(x/5),Height/2)
            message_to_screen(("dV/dN: "+str(self.dvdn)),blue,(x/5),Height*(3/5))
            message_to_screen(("FPS: "+str(round(clock.get_fps()))),blue,(Width-(x*(2/3))),(y/5))
            #---------------------------------------------------------------------------
            xi = x
            for i in range(len(self.celulas)):
                yi = y
                for k in range(len(self.celulas[i])):
                    if self.celulas[i][k] == 1:
                        Display.fill(white, rect = [xi,yi,d,d])
                    yi += d
                xi += d
                
            pygame.display.update()
            update_logic()
            clock.tick(FPS)
            self.N += 1
#####-------------------------------------------------------------------------------------fin de clase
            
def out(x,y,n): #Detecta si una jugada esta fuera de la malla
        if x > (n-1) or y > (n-1) or x < 0 or y < 0:
            return True
        else:
            return False            
            
def desplazar(l,x,y):#Desplaza celulas de muestra 
    for i in range(len(l)):
        l[i][0] += x
        l[i][1] += y

#--------------------------------------------------------------------------------
def gen_root(n): #Funcion para metodo 2
    j = []
    rootX = randint((n//2)-(n//7),(n//2)+(n//7))
    rootY = randint((n//2)-(n//7),(n//2)+(n//7))
    j.append([rootX,rootY])
    return j
        
def rand_gen1(n,m): #Metodo 1 pero, pero usa menos memoria, y puede tener una mayor poblacion, pero con repeticiones que despues se ignoran
    j = []
    rootX = randint((n//2)-(n//7),(n//2)+(n//7))
    rootY = randint((n//2)-(n//7),(n//2)+(n//7))
    j.append([rootX,rootY])
    for i in range(1,m):
        d = choice(direcciones)
        rootX += d[0]
        rootY += d[1]
        if out(rootX,rootY,n) == False:
            j.append([rootX,rootY])
        else:
            pass
    return j

def rand_gen2(root,k,n,max_r): #Metodo 2 mejor, pero usa mas memoria, y menor poblacion
    u = choice(direcciones)
    dx = u[0] + root[0][0]
    dy = u[1] + root[0][1]
    if root.count([dx,dy]) == 0:
        if not out(dx,dy,n):
            root.insert(0,[dx,dy])
            k -= 1
    if k > 1 and max_r > 0:
        max_r -= 1
        rand_gen2(root,k,n,max_r)
    else:
        pass
    return root


#-----------------------------------------------------------------------------------
        #Agregar mas aqui(forma [x,y])
pulsar = [[0,0],[0,1],[0,2],[0,3],[0,4],[4,0],[4,1],[4,2],[4,3],[4,4],[2,0],[2,4]]#1
LWSS = [[3,0],[2,1],[2,2],[2,3],[3,3],[4,3],[5,3],[6,2],[6,0]]#2
blinker = [[0,0],[0,1],[0,2]]#3
toad = [[0,1],[1,1],[2,1],[1,0],[2,0],[3,0]]#4
beacon = [[0,0],[1,0],[0,1],[2,3],[3,3],[3,2]]#5
acorn = [[0,2],[1,2],[1,0],[3,1],[4,2],[5,2],[6,2]]#6
glider_gun = [[0,4],[0,5],[1,4],[1,5],[10,4],[10,5],[10,6],[11,3],[11,7],[12,2],[13,2],[12,8],[13,8],[14,5],[15,3],[15,7],[17,5],
              [16,4],[16,5],[16,6],[20,2],[20,3],[20,4],[21,2],[21,3],[21,4],[22,1],[22,5],[24,1],[24,0],[24,5],[24,6],[34,2],[35,2],[34,3],[35,3]]

#--------------------------------------------------------
lista = [pulsar,LWSS,blinker,toad,beacon,acorn,glider_gun] #asegurase de hacer cambios aqui
lista_mostrar = ["Pulsar","LWSS","Blinker","Toad","Beacon","Acorn","Glider_gun"]
#--------------------------------------------------------

#Programa principal
print("Bienvenido a The Game of Life ( n =",n,")\n")

V = True
while V:
    V = False
    Q = int(input("Jugada al azar(1), Jugada con muestra(2): ")) #[x,y]
    if Q > 2 or Q < 1:
        V = True
        print("\nError\n") 
    
if Q == 2:
    print("\n")
    print("Muestras incluyen:\n",end="")
    for i in range(len(lista_mostrar)):
        print(lista_mostrar[i],end="")
        print("(",str(i+1),") ",end="")
        if i == 5:
            print("\n")
    print("\n")
    V = True
    while V:
        V = False
        J = int(input("Ingrese jugada aqui: "))
        if J > len(lista) or J < 1:
            V = True
            print("\nError\n") 
    des_x = n // 2
    des_y = n // 2
    desplazar(lista[J-1],des_x,des_y)
    J = lista[J-1]
    
if Q == 1:
    V = True
    while V:
        V = False
        v = True
        print("\n")
        while v:
            v = False
            p = int(input("Metodo 1, o Metodo 2?: "))
            if p > 2 or p < 1:
                v = True
                print("\nError\n")
        print("\n")        
        largo = int(input("Ingresa el numero max de Poblacion inicial: "))
        if p == 1:
           J = rand_gen1(n,largo)
           
        elif p == 2:
            root = gen_root(n)
            J = rand_gen2(root,largo,n,max_r)
            
        else:
            control = True
            print("\nError\n") 

game = The_life_game(J,n)
          
if Q == 1:
    print("\nLa jugada aleatoria es la siguiente:\n")
    print(J)
input("\n(Enter)")

game.start()

        
        
                 

