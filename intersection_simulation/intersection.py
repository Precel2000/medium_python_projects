import random
import time
import threading
import pygame
import sys

#default values of signal timers (s)
defaultRed = 150
defaultYellow=5
defaultGreen = {0:20, 1:20, 2:20, 3:20}

signals = []
noOfSignals = 4     # total no of signal lights at crossing

currentGreen = 0    # indicates which signal is green
nextGreen = (currentGreen+1) % noOfSignals      # find the next signal to be green
currentYellow = 0       #indicates if yellow on or off

speeds = {'car': 2.25, 'bus':1.8, 'truck':1.8, 'bike':2.5}

# Coordinates of vehicles’ start
x = {'right':[0,0,0], 'down':[755,727,697], 
    'left':[1400,1400,1400], 'up':[602,627,657]}

y = {'right': [348, 370, 398], 'down':[0,0,0], 
    'left':[498,466,436], 'up':[800,800,800]}

vehicles = {'right': {0:[], 1:[], 2:[], 'crossed': 0}, 
            'down': {0:[], 1:[], 2:[], 'crossed':0}, 
            'left': {0:[], 1:[], 2:[], 'crossed':0}, 
            'up': {0:[], 1:[], 2:[], 'crossed':0}}

vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'bike'}

directionNumbers = {0: 'right', 1: 'down', 2:'left', 3:'up'}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(530,230),(810,230),(810,570),(530,570)]
signalTimerCoods = [(530,210),(810,210),(810,550),(530,550)]

# Coordinates of stop lines
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}

# Gap between vehicles
stoppingGap = 15   
movingGap = 15   

# initialise pygame
pygame.init()
simulation = pygame.sprite.Group()

# define TrafficSignal class 
class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""    # value of timer to 
        
# define Vehicle class
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass            # car, bus, bike or truck
        self.speed = speeds[vehicleClass]           # speed according to class
        self.direction_number = direction_number    # direction its headed in 0-3
        self.direction = direction                  # name of direction
        self.x = x[direction][lane]                 # current x-coordinate of the vehicle
        self.y = y[direction][lane]                 # current y-coordinate of the vehicle
        self.crossed = 0      # has it crossed the intersection, defaults to 0
        self.index = len(vehicles[direction][lane]) - 1     # relative position of the vehicle among the vehicles moving in the same direction and the same lane
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.image = pygame.image.load(path)        # image to be rendered


        # check if other vehicles present on the same lane and direction
        if(len(vehicles[direction][lane])>1 
        and vehicles[direction][lane][self.index-1].crossed==0): 
            # change the stop coordinates to take into account the other 
            # vehicle and the stopping gap between them
            if(direction=='right'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                - vehicles[direction][lane][self.index-1].image.get_rect().width 
                - stoppingGap        
            elif(direction=='left'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                + vehicles[direction][lane][self.index-1].image.get_rect().width 
                + stoppingGap
            elif(direction=='down'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                - vehicles[direction][lane][self.index-1].image.get_rect().height 
                - stoppingGap
            elif(direction=='up'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                + vehicles[direction][lane][self.index-1].image.get_rect().height 
                + stoppingGap
        # if no other vehicles present set value of stop to the default one
        else:
            self.stop = defaultStop[direction]
            
        if(direction=='right'):
            temp = self.image.get_rect().width + stoppingGap    
            x[direction][lane] -= temp
        elif(direction=='left'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        elif(direction=='down'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif(direction=='up'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        simulation.add(self)

    # function to render image
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    # in this method we check if the vehicle has crossed the intersection or not. 
    # If yes then it can keep going regardless of the signal light.

    def move(self):
        if(self.direction=='right'):
            
            if(self.crossed==0 and self.x+self.image.get_rect().width>stopLines[self.direction]):
                self.crossed = 1
            
            if((self.x+self.image.get_rect().width<=self.stop 
            or self.crossed == 1 or (currentGreen==0 and currentYellow==0)) 
            and (self.index==0 or self.x+self.image.get_rect().width
            # check that it doesn't hit the car before it
            <(vehicles[self.direction][self.lane][self.index-1].x - movingGap))):
                # the coordinates of the vehicle is updated by incrementing them by the speed of the vehicle
                self.x += self.speed
        
        elif(self.direction=='down'):
            
            if(self.crossed==0 and self.y+self.image.get_rect().height>stopLines[self.direction]):
                self.crossed = 1
            
            if((self.y+self.image.get_rect().height<=self.stop 
            or self.crossed == 1 or (currentGreen==1 and currentYellow==0)) 
            and (self.index==0 or self.y+self.image.get_rect().height
            <(vehicles[self.direction][self.lane][self.index-1].y - movingGap))):
                self.y += self.speed
        
        elif(self.direction=='left'):
            
            if(self.crossed==0 and 
            self.x<stopLines[self.direction]):
                self.crossed = 1
            
            if((self.x>=self.stop or self.crossed == 1 
            or (currentGreen==2 and currentYellow==0)) 
            and (self.index==0 or self.x
            >(vehicles[self.direction][self.lane][self.index-1].x 
            + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width
            + movingGap))):                
                self.x -= self.speed    
        
        elif(self.direction=='up'):
            
            if(self.crossed==0 and 
            self.y<stopLines[self.direction]):
                self.crossed = 1
            
            if((self.y>=self.stop or self.crossed == 1 
            or (currentGreen==3 and currentYellow==0)) 
            and (self.index==0 or self.y
            >(vehicles[self.direction][self.lane][self.index-1].y 
            + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height
            + movingGap))):                
                self.y -= self.speed
