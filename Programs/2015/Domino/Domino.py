from random import shuffle
class ficha:
    def __init__(self,ficha):
        self.Iz = ficha[0]
        self.De = ficha[1]
        
    def __str__(self):
        return ("-(" + str(self.Iz) + "|"+ str(self.De)+ ")-")
    
    def valor(self):#valor numerico
        return self.Iz + self.De
    
    def rotar(self):#Rota la ficha
        u = []
        u.append(self.De)
        u.append(self.Iz)
        return u

class pila:
    def __init__(self):
        self.pila = []
        
    def generar(self):#Genera pila y la desordena
        for i in range(7):
            for k in range(i,7):
                self.pila.append((i,k))
        shuffle(self.pila)
        
    def sacar_ficha(self):#Saca ficha de pila desordenada
        u = self.pila[0]
        self.pila.remove(u)
        return u
    
    def repartir(self,jugadores): #Reparte fichas para N jugadores/c
        n = 28//len(jugadores)
        for i in range(n):
            for k in range(len(jugadores)):
                jugadores[k].mano.append(self.sacar_ficha())
class mesa:
    def __init__(self):
        self.mesa = []
        
    def imprimir(self):
        k = 0
        print("\n")
        print("|||->",end="")
        for i in self.mesa:
            if k == 10:
                print(" ")
            if k == 20:
                print(" ")
            u = ficha(i)
            print(u,end="")
            k +=1
        print("<-|||")    
        print(" ")
        print(" ")
        
    def poner(self,ficha_lado): #recibe el lado y la ficha a poner
        if self.mesa == []: #Principio
            self.mesa.append(ficha_lado[0])
        else:
            u = ficha(ficha_lado[0]) #Asignar objeto
            l = len(self.mesa) 
            beg = self.mesa[0][0]
            end = self.mesa[l-1][1]
            if ficha_lado[1] == "R":
                if ficha_lado[0][0] == end:
                    self.mesa.append(ficha_lado[0])
                elif ficha_lado[0][1] == end:
                    u = u.rotar()
                    self.mesa.append(u)
            elif ficha_lado[1] == "L":
                if ficha_lado[0][1] == beg:
                    self.mesa.insert(0,ficha_lado[0])
                elif ficha_lado[0][0] == beg:
                    u = u.rotar()
                    self.mesa.insert(0,u)
                         
class jugador:
    def __init__(self,nombre,mano,AI):
        self.nombre = nombre
        self.mano = mano
        self.AI = AI
        self.dicc = []
        
    def __str__(self):
        return self.nombre
    
    def validar(self,jugada,lado): #Recibe Str, valida jugada usario
        if self.dicc[lado] == []: #diccionario que devuelve lista
            return False
        if jugada.isdigit() == False:
            return False
        if int(jugada)-1 > len(self.mano)-1:
            return False
        if int(jugada)-1 < 0:
            return False
        return True
    
    def valor_mano(self):#valor de la mano
        val = 0
        v = 0
        for i in range(len(self.mano)):
            u = ficha(self.mano[i])
            u = u.valor()
            v += u
        return v
    
    def buscar(self,mesa):  #Devuelve lista de las jugadas posibles(asigna a jugador)
        self.fichas_derechas = []
        self.fichas_izquierdas = []
        if mesa == []: # Principio
            self.fichas_derechas = self.mano
            self.fichas_izquierdas = self.mano
            return
        else:
            l = len(mesa)
            beg = mesa[0][0]
            end = mesa[l-1][1]
            for i in range(len(self.mano)): # -(u,v)-
                u = self.mano[i][0]
                v = self.mano[i][1]
                if u == end or v == end: 
                    self.fichas_derechas.append(self.mano[i])
                if u == beg or v == beg:
                    self.fichas_izquierdas.append(self.mano[i])
            
    def jugar(self): #Elje una ficha de las dos listas asignada(saca de la mano)
        self.dicc = {1:self.fichas_derechas,2:self.fichas_izquierdas} #Diccionario
        if self.AI == False:
            print("(Real)")
            print(" ")
            print("*Tu mano: ",end="")
            for i in self.mano:
                h = ficha(i)
                print(h,end="")
            print(" ")
            print(" ")
            print("EL valor de tu mano: ",self.valor_mano(),"\n")
            control = True
            while control == True:
                control = False
                L = int(input("--> Ingresa lado(1 : Derecha | 2 : Izquierda): "))
                if L == 1 or L == 2:
                    print(" ")
                    print("--> Tus jugadas posibles: ",end="")
                    for i in range(len(self.dicc[L])):
                        h = ficha(self.dicc[L][i])
                        print(h,end="")
                    print(" ")
                    print(" ")
                    Q = input("--> Ingresa Jugada(1,2...,n)(Enter para omitir): ")
                    if Q.upper() == "":
                        print("****",self.nombre,"Omite****")
                        print("-----------------------------------------------")
                        return []
                    A = self.validar(Q,L)
                    if A == False:
                        control = True
                        print("-------")
                        print("**Error**")
                        print("-------")
                    if A == True:
                        T = {1:"R",2:"L"}
                        Q = int(Q)
                        jugada = self.dicc[L][Q-1],T[L]
                        self.mano.remove(self.dicc[L][Q-1])
                        print("-----------------------------------------------")
                        return jugada #Lado siendo la ficha y dicc el lado
                else:
                    control = True
                    print("-------")
                    print("**Error**")
                    print("-------")
                
        if self.AI == True:
            print("(AI)\n")
            input("Presiona Enter: ")
            if self.fichas_derechas == [] and self.fichas_izquierdas == []:#Omite
                print("****",self.nombre,"Omite****")
                print("-----------------------------------------------")
                return []
            valores_derecha = []
            valores_izquierda = []
            for i in self.fichas_derechas:#para evitar que una lista sea vacia
                u = ficha(i)
                u = u.valor()
                valores_derecha.append(u)
            for i in self.fichas_izquierdas:# %
                u = ficha(i)
                u = u.valor()
                valores_izquierda.append(u)
            if valores_derecha != []:
                Vmax_derecha = max(valores_derecha)
            else:
                Vmax_derecha = -1
            if valores_izquierda != []:
                Vmax_izquierda = max(valores_izquierda)
            else:
                Vmax_izquierda = -1
            if Vmax_izquierda >= Vmax_derecha: #determina con que lista juega
                index = valores_izquierda.index(Vmax_izquierda)
                jugada = self.fichas_izquierdas[index],"L"
                self.mano.remove(self.fichas_izquierdas[index])
                print("-----------------------------------------------")
                return jugada
            elif Vmax_derecha >= Vmax_izquierda:
                index = valores_derecha.index(Vmax_derecha)
                jugada = self.fichas_derechas[index],"R"
                self.mano.remove(self.fichas_derechas[index])
                print("-----------------------------------------------")
                return jugada
            
                
class partida:
    def __init__(self,nombres,N_jugadoresAI,N_jugadoresR,turno=1):#cambia(simple)
        self.nombres = nombres
        self.N_jugadoresAI = N_jugadoresAI
        self.N_jugadoresR = N_jugadoresR
        self.Omisiones_Max = N_jugadoresAI + N_jugadoresR
        self.Omisiones = 0
        self.turno = turno
        
    def ahogado(self):#True si todos pasan, y determina ganador
        if self.Omisiones == self.Omisiones_Max:
            val = []
            u = 0
            for i in range(len(self.jugadoresP)):
                u = 0
                for k in range(2):
                    u += self.jugadoresP[i][k].valor_mano()
                val.append(u)    
            valmax = val.index(min(val))
            g = self.jugadoresP[valmax]
            g1 = g[0].nombre
            g2 = g[1].nombre
            print("\nHan ganado los jugadores",g1," y ",g2,"!!")
            return True
        
    def ganador(self):#True si un jugador se queda sin dominos
        for i in range(self.N_jugadoresAI+self.N_jugadoresR):
            mano = self.jugadores[i].mano
            if mano == []:
                g = self.jugadores[i]
                print("\nAh ganado el grupo del jugador",g," !!!")
                return True
                 
    def obtener_AI(self): #Devuelve lista de objetos jugador que son AI/c
        shuffle(self.nombres)
        self.AI = []
        for i in range(self.N_jugadoresAI):
            u = jugador(self.nombres[i],[],True)
            self.AI.append(u)
    def obtener_R(self): #Devuelve lista de objetos de jugadores que son reales/c 
        self.R = []
        for i in range(self.N_jugadoresR):
            print("---> Ingresa el nombre del jugador ",i+1,end=": ")
            Q = input("")
            u = jugador(Q,[],False)
            self.R.append(u)
    def obtener_jugadores(self): #Pone primero a los pj reales y luego a los AI/c
        self.jugadores = self.R + self.AI
        
    def determinar_parejas(self): #Tira True si no son parejas pares/c
        n = len(self.jugadores)//2
        print(" ")
        print(n,"Parejas.","\n")
        self.jugadoresP = [(self.R[0],self.AI[0])]
        u = self.jugadores
        u.remove(self.R[0])
        u.remove(self.AI[0])
        shuffle(u)
        for i in range(1,n):
            self.jugadoresP.append((u[0],u[1]))
            u.remove(u[1])
            u.remove(u[0])
        if len(u) != 0:
            print("\nse han eliminado",len(u)," Jugadores: ",u)
            print("Por favor, haga un grupo tal que sea par\n")
            return True
        
    def pasar_turno(self): #asigna turno
        if self.turno >= len(self.jugadores):
            self.turno = 1
        else:
            self.turno += 1          
    def __str__(self):# Permite imprimir
        s = ""
        for i in range(len(self.jugadoresP)):
            m = str(i+1)
            s+= "Grupo "+m+": ("
            for k in range(2):
                s += "|"+self.jugadoresP[i][k].nombre+ "|"
            s+= ") / "
        return s    
            
#------------------------------------

NombresMLG = ["Isaac Newton","Ludwig Boltzmann","Ada Lovelace","Alan Turing","James Clerk Maxwell"
              ,"Paul Dirac","Luis Dissett","Niels Bohr","Richard Feynman","Albert Einstein","Galileo Galilei","Wn Random"]
print("Bienvenido a Dominos!")
print("Este juego se juega en parejas, al momento de crear los jugadores tienen que formar parejas perfectas!")
print("Tambien tiene que haber al menos una computadora y un jugador\n")
mesa = mesa()
pila = pila()    
pila.generar()
control = True
while control == True:#/c
    control = False
    A = int(input("Ingresa el numero de jugadores Reales: "))
    B = int(input("Ingresa el numero de jugadores AI: "))
    if (A + B) % 2 != 0:
        control = True
        print("\nError, tienen que formar parejas perfectas\n")
Juego = partida(NombresMLG,B,A)#/c
Juego.obtener_R()#/c
Juego.obtener_AI()#/c
Juego.obtener_jugadores()
Juego.determinar_parejas()
print(Juego)
Juego.obtener_jugadores()#se borran al determinar parejas/c
jugadores = Juego.jugadores
pila.repartir(jugadores)#/c
partida = True
print("-------------------------------------------------------------")
while partida == True:
    turno = Juego.turno
    mesa.imprimir()
    ahogado = Juego.ahogado()
    ganador = Juego.ganador()
    if ahogado == True or ganador == True:
        partida = False
        break
    print("Turno: ",turno)
    print("Jugador:",jugadores[turno-1].nombre,end="")
    jugadores[turno-1].buscar(mesa.mesa)
    jugada = jugadores[turno-1].jugar()
    if jugada == []:
        Juego.Omisiones+=1
    else:
        Juego.Omisiones = 0
        mesa.poner(jugada)
    Juego.pasar_turno()
    
    
           
    
        
        
