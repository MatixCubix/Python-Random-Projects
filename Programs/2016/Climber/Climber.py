import math
Dir1 = [[1],[-1]]
Dir2 = [[1,0],[0,1],[0.707,0.707],[-0.707,0.707],[0.707,-0.707],[-0.707,-0.707],[-1,0],[0,-1]]
Dir3 = [[1,0,0],[0,1,0],[0,0,1],[0.577,0.577,0.577],[-1,0,0],[0,-1,0],[0,0,-1],[-0.577,0.577,0.577]
        ,[0.577,-0.577,0.577],[0.577,0.577,-0.577],[-0.577,-0.577,0.577],[-0.577,0.577,-0.577]
        ,[0.577,-0.577,-0.577],[-0.577,-0.577,-0.577]]
DirList = [Dir1,Dir2,Dir3]

def Sum(vector1,vector2):
    u = []
    for i in range(len(vector1)):
        u.append(vector1[i]+vector2[i])
    return u

def Scale(vector,a):
    u = []
    for i in range(len(vector)):
        u.append(vector[i]*a)
    return u

class Climber:
    def __init__(self,d):
        self.dx = d

    def walk_max(self,surface,start_pos):
        self.pos = start_pos
        n = len(surface.data)
        Dir = DirList[n-1]
        while True:
            value = surface.give_value(self.pos)
            field = []
            for i in range(len(Dir)):
                field.append(surface.give_value(Sum(self.pos,Scale(Dir[i],self.dx))))
            maximun_field = max(field)
            if maximun_field < value:
                print("*******************")
                print("local maximun at:", self.pos)
                print("Valued at: ", value)
                break
            else:
                index = field.index(maximun_field)
                deltaPos = Scale(Dir[index],self.dx)
                self.pos = Sum(self.pos,deltaPos)

class Polinom:
    def __init__(self,data):
        self.data = data

    def give_value(self,pos):
        value = 0
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                value += self.data[i][j]*(math.pow(pos[i],j))
        return value

if __name__ == "__main__":
    Surface = Polinom([[3,-1,5,0,-5],[1,3,-5,0,-4]])
    Walker = Climber(0.0001)
    Walker.walk_max(Surface,[-5.5,.53])




