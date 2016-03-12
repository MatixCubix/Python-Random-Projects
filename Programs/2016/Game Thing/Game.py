import msvcrt
import os
import time
clear = lambda: os.system('cls')

def sum(v1,v2):
    u = []
    for i in range(len(v1)):
        u.append(v1[i]+v2[i])
    return u

def is_out(n,m,pos):
    if pos[0]<0 or pos[0]>=n:
        return True
    elif pos[1]<0 or pos[1]>=m:
        return True
    return False

class Grid:
    def __init__(self, n, m):  # n=x m=y
        self.n = n
        self.m = m
        self.map = []
        self.TeamA = []
        self.TeamB = []

    def init_map(self):
        for x in range(self.n):
            self.map.append([])
            for y in range(self.m):
                self.map[x].append(None)

    def init_soldiers(self):
        for i in range(len(self.TeamA)):
            self.map[self.TeamA[i].pos[0]][self.TeamA[i].pos[1]] = self.TeamA[i]
        for i in range(len(self.TeamB)):
            self.map[self.TeamB[i].pos[0]][self.TeamB[i].pos[1]] = self.TeamB[i]

    def add_obstacle(self, pos):
        self.map[pos[0]][pos[1]] = Obstacle()

    def add_sandbox(self,pos):
        self.map[pos[0]][pos[1]] = Sandbox()

    def add_soldier(self,Name,Team,pos):
        u = Soldier(Name,pos,Team)
        if Team == 0:
            self.TeamA.append(u)
        elif Team == 1:
            self.TeamB.append(u)

    def print(self):
        for i in range(self.m):
            print("   " * self.n)
            for j in range(self.n):
                if type(grid.map[j][i]) == Soldier:
                    if grid.map[j][i].team == 0:
                        print("| ¶  ", end= "")
                    else:
                        print("| ¶* ", end= "")
                elif type(grid.map[j][i]) == Obstacle:
                    print("| ██ ", end= "")
                elif type(grid.map[j][i]) == Sandbox:
                    print("| ▓▓  ", end= "")
                elif type(grid.map[j][i]) == Bullet:
                    print("| o  ", end= "")
                else:
                    print("|    ", end= "")
            print("|")
            print(" ___ " * self.n)

class Sandbox:
    def __init__(self, integrity=40):
        self.integrity = integrity

class Bullet:
    def __init__(self):
        pass

class Obstacle:
    def __init__(self, integrity=100):
        self.integrity = integrity

class Soldier:
    def __init__(self,Name,Pos,Team,Health = 100,Armour = 100,Grenades = 2,Move_skill = 7 ):
        self.name = Name
        self.health = Health
        self.pos = Pos
        self.armour = Armour
        self.grenades = Grenades
        self.move_skill = Move_skill
        self.team = Team

    def move(self,Grid):
        u = 0
        while u < self.move_skill:
            while True:
                if msvcrt.kbhit():
                    key = str(msvcrt.getch())
                    break
            if key == "b'd'":
                move = [1,0]
            elif key == "b's'":
                move = [0,1]
            elif key == "b'a'":
                move = [-1,0]
            elif key == "b'w'":
                move = [0,-1]
            else:
                continue
            newPos = sum(self.pos,move)
            if is_out(grid.n,grid.m,newPos) == False and grid.map[newPos[0]][newPos[1]] is None:
                Grid.map[self.pos[0]][self.pos[1]] = None
                self.pos = newPos
                Grid.map[newPos[0]][newPos[1]] = self
            else:
                u -= 1
            clear()
            grid.print()
            u += 1

    def shoot(self,Grid):
        bullet = Bullet()
        keyCheck = True
        while True:
            while keyCheck:
                if msvcrt.kbhit():
                    key = str(msvcrt.getch())
                    keyCheck = False
            if key == "b'd'":
                    dir = [1,0]
                    break
            elif key == "b's'":
                    dir = [0,1]
                    break
            elif key == "b'a'":
                    dir = [-1,0]
                    break
            elif key == "b'w'":
                    dir = [0,-1]
                    break
            else:
                keyCheck = True
                continue
        pos = sum(dir,self.pos)
        while is_out(grid.n,grid.m,pos) == False and grid.map[pos[0]][pos[1]] is None:
            grid.map[pos[0]][pos[1]] = bullet
            grid.print()
            time.sleep(0.5)
            clear()
            grid.map[pos[0]][pos[1]] = None
            pos = sum(pos,dir)
        if type(grid.map[pos[0]][pos[1]]) == Soldier
            if grid.map[pos[0]][pos[1]].team == 0:
                grid.TeamA.remove(grid.map[pos[0]][pos[1]])
            else:
                grid.TeamB.remove(grid.map[pos[0]][pos[1]])
            grid.map[pos[0]][pos[1]] = None
        grid.print()

grid = Grid(10, 10)
grid.init_map()
grid.add_obstacle([2,3])
grid.add_obstacle([0,3])
grid.add_obstacle([4,2])
grid.add_obstacle([4,3])
grid.add_obstacle([4,0])
grid.add_obstacle([4,1])
grid.add_obstacle([3,3])
grid.add_sandbox([5,5])
grid.add_soldier("Josh",0,[0,0])
grid.add_soldier("Mark",1,[5,6])
grid.init_soldiers()
grid.print()
grid.TeamA[0].move(grid)
grid.TeamA[0].shoot(grid)
input()