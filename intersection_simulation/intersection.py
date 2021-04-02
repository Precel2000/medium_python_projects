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
