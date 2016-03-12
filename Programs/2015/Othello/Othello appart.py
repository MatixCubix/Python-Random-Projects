def JugadorRestante(tablero):
    negro = 0
    blanco = 0
    for i in range(0,8):
        for k in range(0,8):
            if tablero[i][k] == " X ":
                negro += 1
            elif tablero[i][k] == " O ":
                blanco += 1
    if blanco == 0 or negro == 0:
        return False
    else:
        return True

def CeldasRestantes(tablero):
    contador = 0
    for i in range(0,8):
        for k in range(0,8):
            if tablero[k][i]== " . ":
                contador += 1
    return contador

def DeterminarGanador(tablero):
    Negro = 0
    Blanco = 0
    for i in range(0,8):
        for k in range(0,8):
            if tablero[k][i] == " X ":
                Negro += 1
            elif tablero[k][i] == " O ":
                Blanco += 1
    if Negro > Blanco:
        c = "negro"
    elif Blanco > Negro:
        c = "blanco"
    elif Blanco == Negro:
        c = "none"
    return c

def Transcribir(Jugada):
    error = False
    Dicc = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}
    if Jugada[1].isdigit() == True:
        y = int(Jugada[1])- 1
    else:
        
        error = True
        y = "none"
    if Jugada[0].isalpha()== True and Jugada[0].upper()<="H" and Jugada[0].upper()>="A":
        x = Dicc[Jugada[0].upper()]
    else:
        error = True
        x = "none"
    return x, y, error

def Ahogado(Omisiones):
    if Omisiones == 2:
        return True

def Fuera(x,y):
    if x > 7 or y > 7:
        return True
    else:
        return False
    
def Comprobar(x,y,tablero,turno):
    Direcciones = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
    cambio = []
    if tablero[x][y] != " . ":
        return False , cambio
    if Fuera(x,y) == True:
        return False , cambio
    

    for i in range(0,8):
        uy = y
        ux = x
        ux += Direcciones[i][0]
        uy += Direcciones[i][1]
        
        while not Fuera(ux,uy) and tablero[ux][uy] == alturn_sign:
            ux += Direcciones[i][0]
            uy += Direcciones[i][1]
            if tablero[ux][uy] == turn_sign:
                while True:
                    ux -=Direcciones[i][0]
                    uy -=Direcciones[i][1]
                    if ux == x and uy == y:
                        break
                    cambio.append([ux,uy])
            
    if len(cambio) == 0:
        return False , cambio
    else:
        return True, cambio
   
        
def Transformar(x,y,tablero,cambio):
    tablero[x][y] = turn_sign
    for i in range(len(cambio)):
        ux = cambio[i][0]
        uy = cambio[i][1]
        tablero[ux][uy] = turn_sign
    
    
print("Hola Bienvenido a Othello")
print("Este juego se juega de dos jugadores.")
print(" ")
print("El X es el jugador negro y el O es el jugador blanco.")
print("El . representa un espacio vacio.")
print("Las jugadas se ingresan de la forma A2, H4, etc.")
print(" ")
print("Si los jugadores omiten de manera seguida hasta 2 veces,")
print("el juego se acaba y el que mas tiene gana.")
print(" ")

tablero = [[" . "," . "," . "," . "," . "," . "," . "," . "],[" . "," . "," . "," . "," . "," . "," . "," . "],
           [" . "," . "," . "," . "," . "," . "," . "," . "],[" . "," . "," . "," . "," . "," . "," . "," . "],
           [" . "," . "," . "," . "," . "," . "," . "," . "],[" . "," . "," . "," . "," . "," . "," . "," . "],
           [" . "," . "," . "," . "," . "," . "," . "," . "],[" . "," . "," . "," . "," . "," . "," . "," . "]]

tablero[3][3] = " O "
tablero[4][4] = " O "
tablero[3][4] = " X "
tablero[4][3] = " X "


turno = "N" # Caracteristicas iniciales
Omisiones = 0
Juego = True
Ronda = 1
Dicc1 = {"N":"B","B":"N"}
Dicc2 = {"N":" X ", "B":" O "}

while Juego == True:
    
    alturn = Dicc1[turno]
    turn_sign = Dicc2[turno]
    alturn_sign = Dicc2[alturn]
    
    
    if CeldasRestantes(tablero) == 0 or Ahogado(Omisiones) == True or JugadorRestante(tablero)== False:
        Juego = False
        L = DeterminarGanador(tablero)
        if L == "negro":
            print(" ")
            print("***** Felicitaciones al jugador Negro, Gano! *****")
        if L == "blanco":
            print(" ")
            print("***** Felicitaciones al jugador Blanco, Gano! *****")
        if L == "none":
            print(" ")
            print("***** Bueno eso es inesperado y poco probable, Empataron. *****")
            
    else:
        Control = True
        print(" ")
        print("    "," A", " B"," C"," D"," E"," F"," G"," H")
        print("    --------------------------")
        for y in range(0,8):
            print(y+1," | ",end="")
            for x in range(0,8):
                if x < 7:
                    print(tablero[x][y],end="")
                else:
                    print(tablero[x][y], "|")
        print("    --------------------------")
        print(" ")
        print("Ronda: ",Ronda)
        DiccTurno = {"N":"Turno : Jugador X ","B":"Turno : Jugador O "}
        print(" ")
        print(DiccTurno[turno])
        print(" ")
        
        while Control == True:
            Control = False
            if turno == "N":
                Comp = False
                Jugada = input("*Ingrese jugada(Enter para omitir): ")
                if not Jugada.isalnum():
                    Omisiones += 1
                    turno = "B"
                    Ronda += 1
                else:
                    Omisiones = 0
                    if Transcribir(Jugada)[2] == False:  
                        x = Transcribir(Jugada)[0]
                        y = Transcribir(Jugada)[1]
                        Comp = Comprobar(x,y,tablero,turno)[1]              
                        
                    if Comp == False or Transcribir(Jugada)[2] == True:                        
                        Control = True
                        print(" ")
                        print("*Jugada no valida*")
                        print(" ")
                        
                    else:
                        Ronda += 1
                        Transformar(x,y,tablero,Comp)
                        turno = "B"
                    
            elif turno == "B":
                Comp = False
                Jugada = input("*Ingrese jugada(Enter para omitir): ")
                if not Jugada.isalnum():
                    Omisiones += 1
                    turno = "N"
                    Ronda += 1
                else:
                    Omisiones = 0
                    if Transcribir(Jugada)[2] == False:  
                        x = Transcribir(Jugada)[0]
                        y = Transcribir(Jugada)[1]
                        Comp = Comprobar(x,y,tablero,turno)[1]              
                        
                    if Comp == False or Transcribir(Jugada)[2] == True:                        
                        Control = True
                        print(" ")
                        print("*Jugada no valida*")
                        print(" ")
                        
                    else:
                        Ronda += 1
                        Transformar(x,y,tablero,Comp)
                        turno = "N"
                    














            
        
