####################################################################################
#### Eindopdracht
#### `Les 7`/`Eindopdracht.py`
####
#### Thijs Dregmans 
#### Gemaakt op 2024-01-15
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

DEFAULT_CAR_SIZE = 10
CAR_TRACK_MARGIN = 5

CORNER_MARGIN = 10

MAX_SPEED = 30
MAX_SPEED_IN_CORNER = 20
MAX_ACCELERATION = 10

SCOREBOARD_POSITION = (-250, 250)

####################################################################################
# Help functions

def getOrientationRoad(road):
    point1 = road[1]
    point2 = road[0]

    x = point2[1] - point1[1]
    y = point2[0] - point1[0]

    # Calculate the orientation of the road
    return (math.atan2(x,y)/math.pi*180) - 90

def getDistanceBetween(point1, point2):
    # Calculate the distance between the two points
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

    def getShape(self, id):
        
        shape = tr.Shape('compound')

        # Build blueprint for car
        turtle = tr.Turtle(visible=False)
        turtle.speed('fastest')
        turtle.penup()

        if id == 0:
            transformation = (DEFAULT_CAR_SIZE - (CAR_TRACK_MARGIN / 2)) 
        elif id == 1:
            transformation =  -1 * (DEFAULT_CAR_SIZE - (CAR_TRACK_MARGIN / 2))

        # car silhouette
        turtle.goto(-20, -5 + transformation)
        turtle.begin_poly()
        turtle.goto(-20, 5 + transformation)
        turtle.goto(10, 5 + transformation)
        turtle.goto(10, -5 + transformation)
        turtle.goto(-20, -5 + transformation)
        turtle.end_poly()
        shape.addcomponent(turtle.get_poly(), self.__color)

        # car roof
        turtle.goto(-10, -4 + transformation)
        turtle.begin_poly()
        turtle.goto(-10, 4 + transformation)
        turtle.goto(5, 4 + transformation)
        turtle.goto(5, -4 + transformation)
        turtle.goto(-10, -4 + transformation)
        turtle.end_poly()
        shape.addcomponent(turtle.get_poly(), f'dark{self.__color}')

        # car front window
        turtle.goto(0, -4 + transformation)
        turtle.begin_poly()
        turtle.goto(0, 4 + transformation)
        turtle.goto(5, 4 + transformation)
        turtle.goto(5, -4 + transformation)
        turtle.goto(0, -4 + transformation)
        turtle.end_poly()
        shape.addcomponent(turtle.get_poly(), 'lightblue')

        # car back window
        turtle.goto(-15, -4 + transformation)
        turtle.begin_poly()
        turtle.goto(-15, 4 + transformation)
        turtle.goto(-12, 4 + transformation)
        turtle.goto(-12, -4 + transformation)
        turtle.goto(-15, -4 + transformation)
        turtle.end_poly()
        shape.addcomponent(turtle.get_poly(), 'lightblue')

        # car headlight 1
        turtle.goto(10, -6 + transformation)
        turtle.begin_poly()
        turtle.circle(2)
        turtle.end_poly()
        shape.addcomponent(turtle.get_poly(), 'yellow')

        # car headlight 2
        turtle.goto(10, 2 + transformation)
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
        
        # Calulate the next place on the track

        # Get current road
        road = track.roads[self.__roadPointer]
        roadOrientation = getOrientationRoad(road)
        # Set the orientation of the car the same as that of the current road
        self.turtle.tiltangle(roadOrientation)

        endOfRoad = track.roads[self.__roadPointer][1]
        if getDistanceBetween(self.__position, endOfRoad) <= CORNER_MARGIN:
            # Car is close to the end of the road, so put car on next road
            if ENABLE_FLYING_OF_TRACK and self.__speed > MAX_SPEED_IN_CORNER:
                # Car has flown of the track
                # Continue on current trajectory
                # Potential improvement: Make the MAX_SPEED_IN_CORNER dependent on the angle of the two roads
                angle = math.radians(roadOrientation)
                radius = self.__speed * deltaTime

                dx = (radius * math.cos(angle))
                dy = (radius * math.sin(angle))

                self.__position = (self.__position[0] + dy, self.__position[1] - dx)
            else:
                # Car hasn't flown of the track
                # Either because flying of the track is disabled or the car has a low speed
                self.__roadPointer += 1

                if self.__roadPointer > len(track.roads) - 1:
                    # Reset roadPointer if it points to non-existing road (because the loop is closed, go to the first road)
                    self.__roadPointer = 0
                
                startOfNewRoad = track.roads[self.__roadPointer][0]
                self.__position = startOfNewRoad

        else:
            # Car is not close to the end of the road, so continue driving
            # Calculate nex position on road
            # Uused resource: https://stackoverflow.com/questions/35402609/point-on-circle-base-on-given-angle

            angle = math.radians(roadOrientation)
            radius = self.__speed * deltaTime

            dx = (radius * math.cos(angle))
            dy = (radius * math.sin(angle))

            self.__position = (self.__position[0] + dy, self.__position[1] - dx)

    def assignShape(self):
        self.turtle.shape(f'{self.__color}Car')
        self.turtle.showturtle()
    
    def draw(self, leaveTrail = True):
        if not leaveTrail:
            self.turtle.up()

        self.turtle.goto(self.getPosition())
        
        if not leaveTrail:
            self.turtle.down()

####################################################################################

class Track:
    def __init__(self, name, trackCoordinates = []):
        self.name = name
        self.corners = []

        self.roads = []

        if len(trackCoordinates) > 0:
            # build track with coords
            for coord in trackCoordinates:
                self.corners.append((coord[0], coord[1]))
    
    def addCorner(self, x, y):
        self.corners.append((x, y))

    def setup(self):
        # Add first coord for a second time to close the track
        self.addCorner(self.corners[0][0], self.corners[0][1])

        # define roads
        for i in range(len(self.corners) - 1):
            self.roads.append((self.corners[i], self.corners[i + 1]))
        
        self.__length = 0
        for road in self.roads:
            self.__length += getDistanceBetween(road[0], road[1])

    def draw(self, turtle, noOfCars):
        defaultPensize = turtle.pensize()

        # Base the tracksize on the number of cars
        trackSize = noOfCars * (DEFAULT_CAR_SIZE + CAR_TRACK_MARGIN)
        turtle.speed('fastest') # 'fastest' is a keyword in the turtle library

        turtle.up()
        turtle.pensize(trackSize)
        for corner in self.corners:
            turtle.goto(corner[0], corner[1])
            turtle.down()
        
        # reset pen
        turtle.up()
        turtle.home()
        turtle.pensize(defaultPensize)

####################################################################################

class Scoreboard:
    def __init__(self, position):
        self.__position = position

        self.turtle = tr.Turtle()
        self.turtle.up()


    def draw(self, time):
        self.turtle.down()
        self.turtle.clear()
        self.turtle.goto(self.__position)

        self.turtle.write(
            str(tm.strftime('%H', time)).zfill(2)
            + ":"+str(tm.strftime('%M', time)).zfill(2)+":"
            + str(tm.strftime('%S', time)).zfill(2),
            font=("Arial Narrow", 35, "bold")
        )
        
        self.turtle.up()

####################################################################################

class World:
    def __init__ (self, cars):
        self.isSetUp = False
        # Screen variables
        self.screen = tr.Screen ()
        self.screen.listen ()
        self.screen.bgpic('grass.png')
        self.screen.onkey (self.accelerateCar1, 'a')
        self.screen.onkey (self.decelerateCar1, 'z')
        self.screen.onkey (self.accelerateCar2, 'k')
        self.screen.onkey (self.decelerateCar2, 'm')

        # Finish setup of track with 'Return' key
        self.screen.onkey(self.trackIsSetup, 'Return')
        self.time = tm.time ()
        # Add point of mouse as corner on the track when clicked during setup of track
        self.screen.onclick(self.addCorner)

        self.screen.onclick(self.addCorner)

        self.turtle = tr.Turtle()

        self.cars = cars

        self.track = Track("Main track")

        while not self.isSetUp:
            self.screen.update ()
            tm.sleep(0.1)

        self.track.setup()

        for id in range(len(self.cars)):
            car = self.cars[id]
            self.screen.register_shape(f'{car.getColor()}Car', car.getShape(id))
            car.assignShape()

        self.scoreboard = Scoreboard(SCOREBOARD_POSITION)

    def trackIsSetup(self):
        self.isSetUp = True
    
    def addCorner(self, x, y):
        self.track.addCorner(x, y)
        
    def accelerateCar1 (self):
        self.cars[0].accelerate()

    def decelerateCar1 (self):
        self.cars[0].decelerate()
    
    def accelerateCar2 (self):
        self.cars[1].accelerate()

    def decelerateCar2 (self):
        self.cars[1].decelerate()
        
    def run (self):
        # Draw the track
        self.track.draw(self.turtle, len(self.cars))
        # Put the cars on the track
        for car in self.cars:
            car.goto(self.track.corners[0]) # go to start (first point in track)
            car.draw(leaveTrail = False)
        
        while True:
            # get deltaTime
            self.oldTime = self.time
            self.time = tm.time ()
            self.deltaTime = self.time - self.oldTime

            # foreach car:
            for car in self.cars:
                print(f"{car.getColor()} car position: {car.getPosition()}")
                print(f"{car.getColor()} car speed: {car.getSpeed()}")
                print(f"{car.getColor()} car acceleration: {car.getAcceleration()}")

                # Drive the car
                car.drive(self.track, self.deltaTime)
                car.draw()

                # Draw the scoreboard with current time
                self.scoreboard.draw(tm.localtime())

            print (self.deltaTime)
            self.screen.update ()
            tm.sleep (0.02)

####################################################################################

# Run world with red and blue cars            
cars = [Car("red"), Car("blue")]

world = World (cars)
world.run ()
