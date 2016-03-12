tablero1=[
[0,0,0,0,0,6,0,0,8],
[0,0,5,4,0,2,7,0,6],
[8,7,6,9,5,3,4,0,0],
[0,4,8,2,0,0,0,7,3],
[0,0,0,8,0,5,2,0,0],
[0,2,0,7,3,0,6,0,0],
[0,8,0,6,4,7,3,0,0],
[0,0,4,3,2,0,8,6,0],
[0,6,3,0,9,8,0,2,4]
]

tablero2=[
[0,0,7,3,6,0,0,5,0],
[0,0,0,0,0,5,4,0,0],
[4,0,2,0,0,8,6,0,7],
[8,0,3,5,0,7,2,6,0],
[0,0,0,6,0,0,0,7,4],
[0,0,0,0,3,0,0,0,0],
[0,2,0,4,0,3,0,0,9],
[0,0,0,0,2,1,5,0,6],
[0,0,0,0,0,0,8,0,3]
]

tablero3=[
[0,0,0,0,0,6,4,0,0],
[0,0,0,0,0,3,5,0,0],
[0,0,5,2,0,0,0,3,0],
[0,8,0,0,0,0,0,9,5],
[6,0,2,3,0,0,0,7,1],
[9,0,7,0,0,2,0,0,0],
[0,4,0,6,0,0,0,0,0],
[0,0,3,0,0,0,0,0,0],
[7,6,0,0,4,0,0,0,0]
]

class Sudoku:
    def __init__(self):
        self.nivel=-1
        self.tableros=[0,0,0]
        self.tableros[0]=tablero1
        self.tableros[1]=tablero2
        self.tableros[2]=tablero3
        self.cargarTablero(1)

    def obtener(self,i,j):
        return self.tablero[i][j]

    def es_celda_fija(self,i,j):
        if self.tableros[self.nivel][i][j] == 0:
            return False
        else:
            return True

    def definir(self,i,j,valor):
        self.tablero[i][j]=valor

    def cargarTablero(self,num_dificultad):
        if num_dificultad < 1 or num_dificultad > 3:
            num_dificultad=1
        self.nivel=num_dificultad-1
        self.tablero=[]
        for i in range(0,9):
            self.tablero.append(self.tableros[self.nivel][i].copy())

juego=Sudoku()


def obtener(i,j):
    return juego.obtener(i,j)

def definir(i,j,valor):
    return juego.definir(i,j,valor)

def cargarTablero(num_dificultad):
    return juego.cargarTablero(num_dificultad)
