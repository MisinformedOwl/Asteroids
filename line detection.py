"""
This was the pretesting of line detection before implementing it into the asteroids program.
It uses pretty much exactly the same methods as the game however there have been some iteration changes since then.
This is a good place to see how to sight lines function as the game lines are ratehr scuffed due to the fact they can travel over the screen.
"""
import pygame
import math
import threading
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from queueThreads import queue

#Calculate the X cordinate after rotation and velocity is applied
def velXcalc(rot, velx, boost):
    rot = rot % 360
    x = velx + math.sin(rot/57.2)*boost
    return x

#Calculate the Y cordinate after rotation and velocity is applied
def velYcalc(rot, vely, boost):
    rot = rot % 360
    y = vely + math.cos(rot/57.2)*boost
    return y

def direction(rot, boost):
    d = math.sin(rot)
    d2 = math.cos(rot)
    
    return d, d2

def fixPos(x,y):
    if x > 500:
        x = 0
    elif x < 0:
        x = 500
    if y > 500:
        y = 0
    elif y < 0:
        y = 500
    
    return x, y

##############################################################################

def detection(width, height, rot):
    distance = 0
    x = width
    y = height
    orgy = 0
    orgx = 0
    while x < win.get_width() and y < win.get_height():
        x = velXcalc(rot, x, 1)
        y = velYcalc(rot, y, 1)
        x,y = fixPos(x,y)
        try:
            if (255,0,0,255) == win.get_at((round(x),round(y))):
                pygame.draw.line(win,(255,255,255),(width,height),(round(x),round(y)))
                orgy = y - height
                orgx = x - width
                distance = math.sqrt(orgx ** 2 + orgy ** 2)
                q.add(distance)
                break
        except:
            pygame.draw.line(win,(255,255,255), (width,height), (round(x),round(y)))
            orgy = y - height
            orgx = x - width
            distance = math.sqrt(orgx ** 2 + orgy ** 2)
            q.add(500)
            break

pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("intersect")

ballorg = 250
count = 0
running = True
    
threadlist = []
lineAmmount = 8
incrementLine = 360/lineAmmount

rot = 0

global q
q = queue()

closeness = ctrl.Antecedent((np.arange(0, 500, 1)), "Closeness")
meteorCount = ctrl.Antecedent(np.arange(0,50,1), "Meteors")

danger = ctrl.Consequent(np.arange(0,100,1), "Danger")

meteorCount['lots'] = fuzz.trapmf(meteorCount.universe, [30,50,100, 100])
meteorCount['many'] = fuzz.trimf(meteorCount.universe, [15,40,100])
meteorCount['few'] = fuzz.trimf(meteorCount.universe, [0,10,20])

closeness['close'] = fuzz.trimf(closeness.universe, [0,100,200])
closeness['distant'] = fuzz.trimf(closeness.universe, [100,250,400])
closeness['far'] = fuzz.trimf(closeness.universe, [350,500,500])

danger['low'] = fuzz.trimf(danger.universe, [0,0,30])
danger['med'] = fuzz.trimf(danger.universe, [20,50,100])
danger['high'] = fuzz.trimf(danger.universe, [75,100,100])

rule1 = ctrl.Rule(closeness['close'] & meteorCount['few'], danger['med'])
rule2 = ctrl.Rule(closeness['close'] & meteorCount['many'], danger['high'])
rule3 = ctrl.Rule(closeness['close'] & meteorCount['lots'], danger['high'])

rule4 = ctrl.Rule(closeness['distant'] & meteorCount['few'], danger['low'])
rule5 = ctrl.Rule(closeness['distant'] & meteorCount['many'], danger['med'])
rule6 = ctrl.Rule(closeness['distant'] & meteorCount['lots'], danger['high'])

rule7 = ctrl.Rule(closeness['far'] & meteorCount['few'], danger['low'])
rule8 = ctrl.Rule(closeness['far'] & meteorCount['many'], danger['low'])
rule9 = ctrl.Rule(closeness['far'] & meteorCount['lots'], danger['med'])

dangerControl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9])
dangerLevel = ctrl.ControlSystemSimulation(dangerControl)

dangerLevel.input['Meteors'] = 1

while running:
    x = 250
    y = 250
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    bally = ballorg + (math.sin(count / 500) * 150)
    ballx = ballorg + (math.cos(count / 500) * 150)
    count += 1
    pygame.draw.ellipse(win, (255,0,0), (ballx,bally,20,20))
    rot = math.sin(count/1000) * 45 + 90
    
    for i in range(lineAmmount):
        t = threading.Thread(target=detection, args=[x, y, rot + (incrementLine*i)])
        threadlist.append(t)
    
    for t in threadlist:
        try:
            t.start()
        except:
            continue
    
    for t in threadlist:
        t.join()
    
    print()
    for x in range(q.size()):
        close = q.nextItem()
        dangerLevel.input['Closeness'] = close
        dangerLevel.compute()
        print(f"Danger level: {round(dangerLevel.output['Danger'])}%")
    
    
    
    pygame.display.update()
    win.fill((0,0,0))

pygame.quit()