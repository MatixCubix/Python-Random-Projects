Names = ["Diego","Matias","Carlos","Micha","Carlita","Samantha","Eduardo","Camila","Fabricio","Brayatan"]
StationNames = ["Mordor","Narnia","Pluton","Alfa Centauri"]
StationPosition = [0, 2000, 5000, 8000]
LineName = "1"
Annex = [(0,1),(1,2),(2,3)]

class Train:
    def __init__(self, number, max_speed, direction, door_length, door_time, length, acceleration, initialPosition = 0):
        self.passangers = []
        self.max_speed = max_speed
        self.door_length = door_length
        self.door_time = door_time
        self.direction = direction
        self.speed = 0
        self.position = initialPosition
        self.number = number
        self.length = length
        self.capacity = 10*length
        self.acceleration = acceleration
        self.doors_open = False
        self.timer = 0
        self.stopped = True
        self.docked = False
        self.station_docked = None
        self.target = []

    def accelerate(self,n,dt):
        if not self.docked:
            if self.speed <= self.max_speed*n:# 0<=n<=1
                self.speed += self.acceleration*dt

    def emergency_break(self, dt):
        u = dt * 10
        self.deaccelerate(self,u)

    def deaccelerate(self,dt):
        if not self.docked:
            if self.speed > 0:
                self.speed -= self.acceleration*dt

    def check_stop(self):
        if round(self.speed) == 0:
            self.speed = 0
            self.stopped = True
        else:
            self.stopped = False

    def move(self, dt, Line):
        if not self.docked:
            if self.position < Line.lenght + 1 and self.position > -1:
                if self.direction == 0:
                    self.position += self.speed*dt
                else:
                    self.position -= self.speed*dt
            else:
                self.change_directions()

    def open_doors(self):
        if self.speed == 0:
            self.doors_open = True

    def close_doors(self):
        self.doors_open = True

    def check_collision(self, Line):
        for train in Line.trains:
            if train is not self and train.direction == self.direction:
                if abs(self.position - train.position) <= (self.length + train.length)/2:
                    self.speed = 0
                    train.speed = 0
                    print("Crash")

    def change_directions(self):
        if not self.docked:
            if self.direction == 0:
                self.direction = 1
            else:
                self.direction = 0

    def open_close_doors(self,dt):
        if self.stopped and self.docked:
            self.open_doors()
            if self.timer < self.door_time:
                self.timer += dt
            else:
                self.close_doors()

    def dock_station(self, Line):
        if self.stopped:
            for station in Line.stations:
                if station.position == round(self.position):
                    if self.direction == 0 and station.docked_trains[0] == None:
                        station.docked_trains[0] = self
                        self.station_docked = station
                        self.docked = True
                    elif self.direction == 1 and station.docked_trains[1] == None:
                        station.docked_trains[1] = self
                        self.station_docked = station
                        self.docked = True
                break

    def undock_station(self,Line):
         if self.docked:
             if self.direction == 0:
                self.station_docked.docked_trains[0] = None
             else:
                self.station_docked.docked_trains[1] = None
             self.docked = False
             self.station_docked = None

    def set_target(self,Line):
        print("What")
        pass


    def go_to_target(self, Line, dt):
        pass


class Line:
    def __init__(self, name, length, stations = [], trains = []):
        self.lenght = length
        self.trains = trains
        self.name = name
        self.stations = []
        self.annex = []

    def define_annex(self,annex):
        self.annex = annex

    def add_station(self, name, position, number, isTerminal):
        self.stations.append(Station(position,name,number,isTerminal))

    def add_train(self, number, max_speed, direction, door_length, door_time, length, initialPosition, acceleration):
        self.trains.append(Train(number,max_speed,direction,door_length,door_time, length, acceleration, initialPosition))

class Station:
    def __init__(self, position, name, number, isTerminal, passangers = []):
        self.name = name
        self.number = number
        self.position = position
        self.passangers_waiting = passangers
        self.isTerminal = isTerminal
        self.docked_trains = [None,None]

class Passanger:
    def __init__(self, Name, start_station, end_station, age ):
        self.name = Name
        self.start_station = start_station
        self.end_station = end_station

class Global:
    def __init__(self, dt, lines = []):
        self.people = []
        self.lines = lines
    def set_line(self, name, lenght):
        self.lines.append(Line(name, lenght))





