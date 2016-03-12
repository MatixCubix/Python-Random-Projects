import os
from time import sleep
from random import randint
from random import choice
import copy

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def imprimir(tab,n):
    for i in range(n):
        for k in range(n):
            if tab[k][i] == 1:
                print(" O ",end="")
            else:
                print(" . ",end="")
        print("\n")       

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
        direcciones = [[1,0],[0,1],[1,1],[-1,0],[0,-1],[-1,-1],[1,-1],[-1,1]]
        for i in range(len(self.posicion_vivas)):
            self.L_vecinos.append([self.posicion_vivas[i],[]])
            for k in range(len(direcciones)):
                u = self.posicion_vivas[i][0] + direcciones[k][0]
                v = self.posicion_vivas[i][1] + direcciones[k][1]
                if out(u,v,self.n) == False:
                    self.L_vecinos[i][1].append([u,v])#([[2,3],[[2,2],[3,2]]],[[5,3],[[4,2],[3,2]]])
                    
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
            if v == 3 or v == 2:#vive
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
        
    def start(self,end = False):
        self.generate_cells()
        self.mod()
        self.N = 0
        while True:
            imprimir(self.celulas,self.n)
            self.vivas()
            self.vecinos()
            self.vecinosU()
            self.repeticiones()
            self.revivir()
            self.matar()
            self.aplicar()
            print("\n",self.N)
            sleep(0.1)
            cls()
            self.N += 1

                
def out(x,y,n): #Detecta si una jugada esta fuera de la malla
        if x > (n-1) or y > (n-1) or x < 0 or y < 0:
            return True
        else:
            return False            
            
            
def desplazar(l,x,y):#Desplaza celulas de muestra 
    for i in range(len(l)):
        l[i][0] += x
        l[i][1] += y

def randomGen(n,m):
    j = []
    direcciones = [[1,0],[0,1],[1,1],[-1,0],[0,-1],[-1,-1],[1,-1],[-1,1]]
    rootX = randint((n//2)-(n//7),(n//2)+(n//7))
    rootY = randint((n//2)-(n//7),(n//2)+(n//7))
    j.append([rootX,rootY])
    for i in range(1,m):
        d = choice(direcciones)
        rootX += d[0]
        rootY += d[1]
        if out(rootX,rootY,n) == False:
            j.append([rootX,rootY])
        else: #Mejorar esto***
            pass
    return j
    


    
#Mejorar Termino ya que empieza a oscilar y no detecta que termina(talvez no se pueda, pueden formarese sistemas muy complejos)***

#---------------------------------------------------------
        #Agregar mas aqui(forma [x,y])
pulsar = [[0,0],[0,1],[0,2],[0,3],[0,4],[4,0],[4,1],[4,2],[4,3],[4,4],[2,0],[2,4]]#1
LWSS = [[3,0],[2,1],[2,2],[2,3],[3,3],[4,3],[5,3],[6,2],[6,0]]#2
blinker = [[0,0],[0,1],[0,2]]#3
toad = [[0,1],[1,1],[2,1],[1,0],[2,0],[3,0]]#4
beacon = [[0,0],[1,0],[0,1],[2,3],[3,3],[3,2]]#5
acorn = [[0,2],[1,2],[1,0],[3,1],[4,2],[5,2],[6,2]]#6

#--------------------------------------------------------
lista = [pulsar,LWSS,blinker,toad,beacon,acorn] #asegurase de hacer cambios aqui
lista_mostrar = ["Pulsar","LWSS","Blinker","Toad","Beacon","Acorn"]
#--------------------------------------------------------
n = 26
#--------------------------------------------------------

print("Bienvenido a The Life Game ( n =",n,")\n")

Q = int(input("Jugada al azar(1), Jugada con muestra(2): ")) #[x,y]
    
if Q == 2:
    print("\n")
    print("Muestras incluyen:\n",end="")
    for i in range(len(lista_mostrar)):
        print(lista_mostrar[i],end="")
        print("(",str(i+1),") ",end="")
        if i == 10:
            print("\n")
    print("\n")
    J = int(input("Ingrese jugada aqui: "))
    x = int(input("\nIngrese desplazamiento en el eje x: "))
    y = int(input("\nIngrese desplazamiento en el eje y: "))
    desplazar(lista[J-1],x,y)
    J = lista[J-1]
    
if Q == 1:
    print("\n")
    largo = int(input("Ingresa la cantidad de celulas vivas iniciales max: "))
    J = randomGen(n,largo)

game = The_life_game(J,n)
input("\n(Enter)")
print("\n*-----------------------------------------------*")
game.start()

        
        
                 

