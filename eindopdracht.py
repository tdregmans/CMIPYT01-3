####################################################################################
#### Eindopdracht
#### `Les 7`/`Eindopdracht.py`
####
#### Thijs Dregmans 
#### Gemaakt op 2023-12-28
#### 
#### Zie http://wiztech.nl/module_inleiding_programmeren_in_python/les_7_object_modellering/overig_lesmateriaal/eindopdracht/eindopdracht.pdf voor beschrijving
####

####################################################################################

# Libaries
import math
import time as tm
import turtle as tr

# Constants and Settings

ENABLE_FLYING_OF_TRACK = True

DEFAULT_TRACK_SIZE = 30
DEFAULT_TRACK_COORDS = [(-250, 250), (250, 250), (250, -250), (-250, -250)]

CORNER_MARGIN = 10

MAX_SPEED = 30
MAX_SPEED_IN_CORNER = 10
MAX_ACCELERATION = 10

# Help functions

def getOrientationRoad(road):
    point1 = road[1]
    point2 = road[0]

    x = point2[1] - point1[1]
    y = point2[0] - point1[0]

    return (math.atan2(x,y)/math.pi*180) - 90

def getDistanceBetween(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

####################################################################################

class Car:
    def __init__(self, color):
        self.__color = color
        self.__position = (0, 0)

        self.__speed = 0
        self.__acceleration = 0

        self.__roadPointer = 0

        self.turtle = tr.Turtle(visible=False)

    def getShape(self):
        
        shape = tr.Shape('compound')

        # Build blueprint for car
        turtle = tr.Turtle(visible=False)
        turtle.speed('fastest')
        turtle.penup()

        # car silhouette
        turtle.goto(-20, -5)
        turtle.begin_poly()
        turtle.goto(-20, 5)
        turtle.goto(10, 5)
        turtle.goto(10, -5)
        turtle.goto(-20, -5)
        turtle.end_poly()
        shape.addcomponent(turtle.get_poly(), self.__color)

        # car roof
        turtle.goto(-10, -4)
        turtle.begin_poly()
        turtle.goto(-10, 4)
        turtle.goto(5, 4)
        turtle.goto(5, -4)
        turtle.goto(-10, -4)
        turtle.end_poly()
        shape.addcomponent(turtle.get_poly(), f'dark{self.__color}')

        # car front window
        turtle.goto(0, -4)
        turtle.begin_poly()
        turtle.goto(0, 4)
        turtle.goto(5, 4)
        turtle.goto(5, -4)
        turtle.goto(0, -4)
        turtle.end_poly()
        shape.addcomponent(turtle.get_poly(), 'lightblue')

        # car back window
        turtle.goto(-15, -4)
        turtle.begin_poly()
        turtle.goto(-15, 4)
        turtle.goto(-12, 4)
        turtle.goto(-12, -4)
        turtle.goto(-15, -4)
        turtle.end_poly()
        shape.addcomponent(turtle.get_poly(), 'lightblue')

        # car headlight 1
        turtle.goto(10, -6)
        turtle.begin_poly()
        turtle.circle(2)
        turtle.end_poly()
        shape.addcomponent(turtle.get_poly(), 'yellow')

        # car headlight 2
        turtle.goto(10, 2)
        turtle.begin_poly()
        turtle.circle(2)
        turtle.end_poly()
        shape.addcomponent(turtle.get_poly(), 'yellow')
        
        turtle.reset()
        
        return shape
    
    def getColor(self):
        return self.__color
    
    def getPosition(self):
        return self.__position
    
    def getSpeed(self):
        return self.__speed
    
    def getAcceleration(self):
        return self.__acceleration
    
    def goto(self, position):
        self.__position = position
    
    def accelerate(self, amount = 1):
        self.__acceleration += amount
        
        if self.__acceleration > MAX_ACCELERATION:
            self.__acceleration = MAX_ACCELERATION
        
        elif self.__acceleration < - MAX_ACCELERATION:
            self.__acceleration = - MAX_ACCELERATION

    def decelerate(self, amount = 1):
        self.__acceleration -= amount
        
        if self.__acceleration > MAX_ACCELERATION:
            self.__acceleration = MAX_ACCELERATION
        
        elif self.__acceleration < - MAX_ACCELERATION:
            self.__acceleration = - MAX_ACCELERATION
    
    def drive(self, track, deltaTime):
        self.__speed += (self.__acceleration * deltaTime)

        if self.__speed > MAX_SPEED:
            self.__speed = MAX_SPEED
        
        # calulate the next place on the track

        road = track.roads[self.__roadPointer]
        roadOrientation = getOrientationRoad(road)

        self.turtle.tiltangle(roadOrientation)

        endOfRoad = track.roads[self.__roadPointer][1]
        if getDistanceBetween(self.__position, endOfRoad) <= CORNER_MARGIN:
            # close to the end of the road, so put car on next road
            if ENABLE_FLYING_OF_TRACK and self.__speed > MAX_SPEED_IN_CORNER:
                # car has flown of the track
                # idea: make the MAX_SPEED_IN_CORNER dependent on the angle of the two roads
                print("Car went off road!") # Car stops on the track
            else:
                self.__roadPointer += 1

                if self.__roadPointer > len(track.roads) - 1:
                    # reset roadPointer if it points to the last road
                    self.__roadPointer = 0
                
                print("put on new road")
                startOfNewRoad = track.roads[self.__roadPointer][0]
                self.__position = startOfNewRoad

        else:
            # on normal road
            # Calculate nex position on road
            # https://stackoverflow.com/questions/35402609/point-on-circle-base-on-given-angle

            angle = math.radians(roadOrientation)
            radius = self.__speed * deltaTime

            dx = (radius * math.cos(angle))
            dy = (radius * math.sin(angle))

            self.__position = (self.__position[0] + dy, self.__position[1] - dx)

    def assignShape(self):
        self.turtle.shape(f'{self.__color}Car')
        self.turtle.showturtle()
    
    def draw(self):
        self.turtle.goto(self.getPosition())

####################################################################################

class Track:
    def __init__(self, name, trackCoordinates):
        self.name = name
        self.corners = []

        self.roads = []

        # build track with coords
        for coord in trackCoordinates:
            self.corners.append((coord[0], coord[1]))
        # Add first coord for a second time to close the track
        self.corners.append((trackCoordinates[0][0], trackCoordinates[0][1]))

        # define roads
        for i in range(len(self.corners) - 1):
            self.roads.append((self.corners[i], self.corners[i + 1]))
        
        self.__length = 0
        for road in self.roads:
            self.__length += getDistanceBetween(road[0], road[1])

    def draw(self, turtle):
        defaultPensize = turtle.pensize()
        turtle.speed('fastest')

        turtle.up()
        turtle.pensize(DEFAULT_TRACK_SIZE)
        for corner in self.corners:
            turtle.goto(corner[0], corner[1])
            turtle.down()
        
        # reset pen
        turtle.up()
        turtle.home()
        turtle.pensize(defaultPensize)

####################################################################################

class World:
    def __init__ (self):
        self.screen = tr.Screen ()
        self.screen.listen ()
        self.screen.onkey (self.accelerateCar1, 'a')
        self.screen.onkey (self.decelerateCar1, 'z')
        self.screen.onkey (self.accelerateCar2, 'k')
        self.screen.onkey (self.decelerateCar2, 'm')
        self.time = tm.time ()

        self.turtle = tr.Turtle()

        self.track = Track("Main track", DEFAULT_TRACK_COORDS)

        self.cars = [Car("red"), Car("blue")]

        for car in self.cars:
            self.screen.register_shape(f'{car.getColor()}Car', car.getShape())
            car.assignShape()
        
    def accelerateCar1 (self):
        self.cars[0].accelerate()

    def decelerateCar1 (self):
        self.cars[0].decelerate()
    
    def accelerateCar2 (self):
        self.cars[1].accelerate()

    def decelerateCar2 (self):
        self.cars[1].decelerate()
        
    def run (self):

        # standard corners
        self.track.draw(self.turtle)
        for car in self.cars:
            car.goto(self.track.corners[0]) # go to start (first point in track)
        
        while True:
            # get deltaTime
            self.oldTime = self.time
            self.time = tm.time ()
            self.deltaTime = self.time - self.oldTime

            for car in self.cars:
                print(f"{car.getColor()} car position: {car.getPosition()}")
                print(f"{car.getColor()} car speed: {car.getSpeed()}")
                print(f"{car.getColor()} car acceleration: {car.getAcceleration()}")

                car.drive(self.track, self.deltaTime)
                car.draw()

            print (self.deltaTime)
            self.screen.update ()
            tm.sleep (0.02)

# Run world
world = World ()
world.run ()
