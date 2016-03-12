import sudoku

print("Bienvenido a Sudoku")
print("Este juego consiste en que tienes que completar el cuadrado 9x9")
print("de tal manera que no se repitan los numeros de las columnas, de las filas")
print("y de los cuadrantes.")
print("Los 0 representan espacios vacios, y no puedes poner 0")
print("Pero uno es capaz de cambiar los numeros.")
print("                     ")
comienzo = True
turnos = 0
while comienzo == True:
    comienzo = input("¿Quieres Empezar? ")

    if  comienzo.upper() == "SI":
        print("                                ")
        print("Hay 3 modos Disponibles el Facil-(1) Medio-(2) Dificil-(3)")
        dificultad = input("ingresa la dificultad  ")
        dificultad = int(dificultad)            #Dificultad
        if dificultad>3 or dificultad<0:
            print("                   ")                  
            print("Error, vamos a suponer que es el nivel facil(Porque sabemos que eres n00b)")
            print("                   ")  
            dificultad = 1
        
        sudoku.cargarTablero(dificultad)
        
        Jugada = "1"
        
        while Jugada == "1":
            
            print("                           ") 
            turnos = turnos + 1
            print(" Jugada", turnos)   
            i = 0                                   
            print("                            ")
            print("    123 456 789   (C)")  
            print("    --- --- --- ")
            
            while i < 9:
                if i == 3 or i == 6:
                    print("    --- --- --- ")
                print(i+1 ,"|",sudoku.obtener(i,0),end="")    #Impresion de sudoku
                print(sudoku.obtener(i,1), end="")
                print(sudoku.obtener(i,2), end="")
                print("",sudoku.obtener(i,3), end="")
                print(sudoku.obtener(i,4), end="")
                print(sudoku.obtener(i,5), end="")
                print("",sudoku.obtener(i,6), end="")
                print(sudoku.obtener(i,7), end="")
                print(sudoku.obtener(i,8),"|")
                
                i = i + 1
            print ("(F)")
            
            print("                              ")
            
                                                       
            Jugada = (input(" ¿Que quieres hacer? 1- Jugar. 2-Salir.  "))  #Primer input del jugador en el juego
            idiota_x = True
            idiota_y = True
            idiota_valor = True
            f = True # La variable f sirve si el usario pone otra cosa ademas de 1 o 2, le asigne jugada a 1 para no generar error y no perder datos 
            
            while f == True:
                
                if Jugada == "1":
                    
                    k = 0
                    Buscador_Error = True
                    
                    while Buscador_Error == True: #si es true le va preguntar al usuario la columna y la fila y el valor, si es false va imprimir el sudoku, continuando el juego
                        
                        x = -1
                        while idiota_x == True: # Las variables idiotas sirven si el usuario se equivoca en poner una valor al las columnas, o a las filas, o al mismo valor

                            jugada_x = int(input(" Ingrese columna: "))
                            jugada_x = jugada_x - 1 # el -1 sirve para asignar la columna 0 a la columna 1, para que sea mas amistoso para el usuario, Igual para la fila
                            
                            if jugada_x > 8 or jugada_x < 0:    
                                k = 1 + k # la variable K sirve como para variar la conversacion si el usuario comente multiples errores
                                if k == 4:
                                    print("                             ")  
                                    print("   Sabes lo que es una columna?!")
                                    print("                             ")  
                                elif k >= 5 and k != 9:
                                    print("                                     ") 
                                    print("   Para de joder y anda ver a wikipedia!, o lo que sea")
                                    print("                                     ")
                                elif k == 9:
                                    print("                                     ")
                                    print("   Por Dios...")
                                    print("                                     ")    
                                else:    
                                    print("         ")
                                    print("   Idiota ")
                                    print("         ")
                            else:
                                idiota_x = False
                                k = 0
                                
                        while idiota_y == True:

                            jugada_y = int(input(" Ingrese fila: "))
                            jugada_y = jugada_y - 1
                            
                            if jugada_y > 8 or jugada_y < 0:
                                k = 1 + k
                                if k == 4:
                                    print("                             ")  
                                    print("   Sabes lo que es una fila?!")
                                    print("                             ")  
                                elif k >= 5 and k != 9:
                                    print("                                     ") 
                                    print("   Para de joder y anda ver a wikipedia!, enserio, se que lo haces con razones malas")
                                    print("                                     ")
                                elif k == 9:
                                    print("                                     ")
                                    print("   Por Dios...")
                                    print("                                     ")
                                else:
                                    print("       ")  
                                    print("   Idiota ")
                                    print("       ")
                                  
                            else:
                                idiota_y = False
                                k = 0

                        while idiota_valor == True:
                            
                            valor = int(input(" Ingrese el valor: "))
                            
                            if valor >= 10 or valor < 0:
                                k = 1 + k
                                if k == 4:
                                    print("                             ")  
                                    print("   Como no entiendes que son numeros de el 0 hasta el 9?!")
                                    print("                             ")  
                                elif k >= 5 and k <= 6:
                                    print("                                     ") 
                                    print("   Que acaso estas en kinder?! (ni siquiera)")
                                    print("                                     ")
                                elif k == 9:
                                    print("                                     ")
                                    print("   Por Dios...")
                                    print("                                     ")
                                else:    
                                    print("       ")
                                    print("   Idiota ")
                                    print("        ")
                            else:
                                idiota_valor= False
                                k = 0

                        m = True # Luego de pasar por el proceso de verificar si no hay ningun valor igual en el quadrante, la fila o la columna, m es True,
                                   # y permite que se le asigne el valor a la matriz en esa posicion, en otras palabras el programa verifica si hay un valor igual y si no lo asigna
                                   
                        

                        while x < 8: # debido a que son 9 columnas y filas 
                            
                            x = x + 1
                            
                                
                            if valor == sudoku.obtener(jugada_y,x): # varia en columnas manteniedo constante la fila
                                
                                if valor == sudoku.obtener(jugada_y,jugada_x): #Este if sirve para poder cambiar los numeros en una misma posicion
                                    Buscador_Error = False
                                    f = False
                                    m = True
                                else:
                                    Buscador_Error = True
                                    print("                          ")
                                    print("   Esta malo, aprende a jugar, hay un valor igual en la misma columna, o fila")
                                    print("                         ")
                                    x = 9
                                    idiota_y = True
                                    idiota_valor = True
                                    idiota_x = True
                                    m = False
                                        
                            elif valor == sudoku.obtener(x,jugada_x):# varia en filas manteniendo constante la columna
                                
                                if valor == sudoku.obtener(jugada_y,jugada_x):
                                    Buscador_Error = False
                                    f = False
                                    m = True
                                else:
                                    Buscador_Error = True
                                    print("                          ")
                                    print("   Esta malo, aprende a jugar, hay un valor igual en la misma columna, o fila")
                                    print("                         ")
                                    x = 9
                                    idiota_y = True
                                    idiota_valor = True
                                    idiota_x = True
                                    m = False
                                   
                                    
                        if 0<=jugada_y<=2: 
						#De aqui en adelante el pograma Analisa en donde esta la variable del usiario y determina un intervalo segun quadrante y ve si hay valores iguales
                            if 0<=jugada_x<=2:
                                t = 0              #Decidi crear una variable t por comodidad para realizar este otro loop de Análisis si me equivocaba y tenia que poner otra variable
                                while t <= 2:
                                    if valor == sudoku.obtener(0,t) or valor == sudoku.obtener(1,t) or valor == sudoku.obtener(2,t):
                                        if valor == sudoku.obtener(jugada_y,jugada_x):
                                            Buscador_Error = False
                                            f = False
                                            m = True    
                                        else:
                                            Buscador_Error = True
                                            print("                          ")
                                            print("   Esta malo, aprende a jugar, hay un valor igual en el quadrante")
                                            print("                         ")
                                            t = 10
                                            x = 9
                                            idiota_y = True
                                            idiota_valor = True
                                            idiota_x = True
                                            m = False
                                            
                                    t = t + 1
                                
                            elif 3<=jugada_x<=5:
                                t = 3
                                while t <= 5:
                                    if valor == sudoku.obtener(0,t) or valor == sudoku.obtener(1,t) or valor == sudoku.obtener(2,t):                                                  
                                        if valor == sudoku.obtener(jugada_y,jugada_x):
                                            Buscador_Error = False
                                            f = False
                                            m = True    
                                        else:
                                            
                                            Buscador_Error = True
                                            print("                          ")
                                            print("   Esta malo, aprende a jugar, hay un valor igual en el quadrante")
                                            print("                         ")
                                            t = 10
                                            x = 9
                                            idiota_y = True
                                            idiota_valor = True
                                            idiota_x = True
                                            m = False
                                            
                                    t = t + 1
                            
                            elif 6<=jugada_x<=8:
                                t = 6
                                while t <= 8:
                                    if valor == sudoku.obtener(0,t) or valor == sudoku.obtener(1,t) or valor == sudoku.obtener(2,t):
                                        if valor == sudoku.obtener(jugada_y,jugada_x):
                                            Buscador_Error = False
                                            f = False
                                            m = True    
                                        else:
                                            
                                            Buscador_Error = True
                                            print("                          ")
                                            print("   Esta malo, aprende a jugar, hay un valor igual en el quadrante")
                                            print("                         ")
                                            t = 10
                                            x = 9
                                            idiota_y = True
                                            idiota_valor = True
                                            idiota_x = True
                                            m = False
                                            
                                    t = t + 1
                              
                        elif 3<=jugada_y<=5:
                        
                            if 0<=jugada_x<=2:
                                t = 0
                                while t <= 2:
                                    if valor == sudoku.obtener(3,t) or valor == sudoku.obtener(4,t) or valor == sudoku.obtener(5,t):
                                        if valor == sudoku.obtener(jugada_y,jugada_x):
                                            Buscador_Error = False
                                            f = False
                                            m = True    
                                        else:
                                              
                                            Buscador_Error = True
                                            print("                          ")
                                            print("   Esta malo, aprende a jugar, hay un valor igual en el quadrante")
                                            print("                         ")
                                            t = 10
                                            x = 9
                                            idiota_y = True
                                            idiota_valor = True
                                            idiota_x = True
                                            m = False
                                            
                                    t = t + 1
           
                            elif 3<=jugada_x<=5:
                                t = 3
                                while t <= 5:
                                    if valor == sudoku.obtener(3,t) or valor == sudoku.obtener(4,t) or valor == sudoku.obtener(5,t):
                                        if valor == sudoku.obtener(jugada_y,jugada_x):
                                            Buscador_Error = False
                                            f = False
                                            m = True
                                        
                                        else:
                                            
                                            Buscador_Error = True
                                            print("                          ")
                                            print("   Esta malo, aprende a jugar, hay un valor igual en el quadrante")
                                            print("                         ")
                                            t = 10
                                            x = 9
                                            idiota_y = True
                                            idiota_valor = True
                                            idiota_x = True
                                            m = False
                    
                                    t = t + 1
                            
                            elif 6<=jugada_x<=8:
                                t = 6
                                while t <= 8:
                                    if valor == sudoku.obtener(3,t) or valor == sudoku.obtener(4,t) or valor == sudoku.obtener(5,t):
                                        if valor == sudoku.obtener(jugada_y,jugada_x):
                                            Buscador_Error = False
                                            f = False
                                            m = True    
                                        else:
                                            
                                            Buscador_Error = True
                                            print("                          ")
                                            print("   Esta malo, aprende a jugar, hay un valor igual en el quadrante")
                                            print("                         ")
                                            t = 10
                                            x = 9
                                            idiota_y = True
                                            idiota_valor = True
                                            idiota_x = True
                                            m = False
                                        
                                    t = t + 1
                            
                        elif 6<=jugada_y<=8:
                        
                            if 0<=jugada_x<=2:
                                t = 0
                                while t <= 2:
                                    if valor == sudoku.obtener(6,t) or valor == sudoku.obtener(7,t) or valor == sudoku.obtener(8,t):
                                        if valor == sudoku.obtener(jugada_y,jugada_x):
                                            Buscador_Error = False
                                            f = False
                                            m = True    
                                        else:
                                            
                                            Buscador_Error = True
                                            print("                          ")
                                            print("   Esta malo, aprende a jugar, hay un valor igual en el quadrante")
                                            print("                         ")
                                            t = 10
                                            x = 9
                                            idiota_y = True
                                            idiota_valor = True
                                            idiota_x = True
                                            m = False
                                          
                                    t =t + 1
                            
                            elif 3<=jugada_x<=5:
                                t = 3
                                while t <= 5:
                                    if valor == sudoku.obtener(6,t) or valor == sudoku.obtener(7,t) or valor == sudoku.obtener(8,t):
                                        if valor == sudoku.obtener(jugada_y,jugada_x):
                                            Buscador_Error = False
                                            f = False
                                            m = True
                                         
                                        else:
                                            
                                            Buscador_Error = True
                                            print("                          ")
                                            print("   Esta malo, aprende a jugar, hay un valor igual en el quadrante")
                                            print("                         ")
                                            t = 10
                                            x = 9
                                            idiota_y = True
                                            idiota_valor = True
                                            idiota_x = True
                                            m = False
                                           
                                    t = t + 1
                               
                            elif 6<=jugada_x<=8:
                                t = 6
                                while t <= 8:
                                    if valor == sudoku.obtener(6,t) or valor == sudoku.obtener(7,t) or valor == sudoku.obtener(8,t):
                                        if valor == sudoku.obtener(jugada_y,jugada_x):
                                            Buscador_Error = False
                                            f = False
                                            m = True    
                                        else:
                                            
                                            Buscador_Error = True
                                            print("                          ")
                                            print("   Esta malo, aprende a jugar, hay un valor igual en el quadrante")
                                            print("                         ")
                                            t = 10
                                            x = 9
                                            idiota_y = True
                                            idiota_valor = True
                                            idiota_x = True
                                            m = False
                                          
                                    t = t + 1
                                        
                        if m == True:
                            sudoku.definir(jugada_y,jugada_x,valor)
                            Buscador_Error = False #Esta bien la jugada si se cumple el este Else, y M true
                            f = False # f false para que termine de preguntar eh imprima sudoku nuevo
                            m = True
                                
                elif Jugada == "2": #Pregunta si quiere salir de verdad
                    print("                   ")
                    g = input("Estas Seguro? D: ")
                    print("                   ")
                    if g.upper()== "SI":
                        print(" Adios, Espero no haberte aburrido ")
                        print("                   ")
                        f = False
                        Buscador_Error = False
                        comeinzo = False
                    elif g.upper()== "NO":
                        f = True
                        print(" Ok :)")
                        print("                ")
                        Jugada = "1"
                else: # si el usuario pone cualquier cosa
                    Jugada = "1"
                    f = True
                
    elif comienzo.upper() == "NO":
        print("                   ")
        print("Que Pena D:")
        print("                   ")
        comienzo = False
        
    else:
                      
        print("No pongas cualquier cosa profavor, que soy tonto y no entiendo")
                    
                 
            
        
    

     

    

    
  
