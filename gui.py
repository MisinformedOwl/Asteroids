import tkinter as tk
from tkinter import colorchooser
from PIL import Image
import game
import threading

def bootTraining():
    start = threading.Thread(target=game.train, args=(debugSelected.get(), asteroidColor), daemon=True)
    start.start()
    window.destroy()
    
def bootGame():
    start = threading.Thread(target=game.play, args=(debugSelected.get(), asteroidColor), daemon=True)
    start.start()
    window.destroy()
    

playerX, playerY = 150,150
droneX, droneY = 250,175

global asteroidColor
asteroidColor = (139,69,19)


playerPoints = [playerX, playerY, playerX+40, playerY+80, playerX, playerY+60, playerX-40, playerY+80]
dronePoints = [droneX, droneY, droneX+(40/3), droneY+(80/3), droneX-(40/3), droneY+(80/3)]

#https://www.youtube.com/watch?v=NDCirUTTrhg
def colorAsteroids():
    global asteroidColor
    color = colorchooser.askcolor()
    color = color[1] #Grab hex encoding
    asteroidColor = color
    
    #https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    asteroidColor = asteroidColor.lstrip('#')
    lv = len(asteroidColor)
    asteroidColor = tuple(int(asteroidColor[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    
    drawAsteroids(color)
    
def colorPlayer():
    color = colorchooser.askcolor()
    color = color[1] #Grab hex encoding
    color = '0x' + color[1:]
    changeShipColor(r"sprites/playerDefault.png", color, playerPoints)
    
#For some reason the drone refuses to be the same colour even though it goes through the exact same process as the other ship. and in the files has this same color.
def colorDrone():
    color = colorchooser.askcolor()
    color = color[1] #Grab hex encoding
    color = '0x' + color[1:]
    changeShipColor(r"sprites/droneDefault.png", color, dronePoints)

def drawAsteroid(x,y,w,h, color):
    canvas.create_oval(x, y, w, h, outline=color, fill=color, width=2)

def drawAsteroids(color):
    drawAsteroid(10, 10, 100, 100, color)
    drawAsteroid(110, 10, 180, 80, color)
    drawAsteroid(190, 10, 230, 50, color)
    drawAsteroid(240, 10, 255, 25, color)
    
#https://stackoverflow.com/questions/765736/how-to-use-pil-to-make-all-white-pixels-transparent
def changeShipColor(ship, color, points):
    colorPoints = color[2:]
    colorPoints = '#' + colorPoints 
    canvas.create_polygon(points, outline='#222222', fill=colorPoints, width=5)
    
    #https://stackoverflow.com/questions/4296249/how-do-i-convert-a-hex-triplet-to-an-rgb-tuple-and-back/4296263
    R, G, B = color[0:4], '0x' + color[4:6], '0x' + color[6:8]
    r, g , b = int(R, 16), int(G, 16), int(B, 16)
    img = Image.open(ship)
    img = img.convert("RGBA")
    datas = img.getdata()
    
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255 and item[3] == 255:
            newData.append((r, g, b, 255))
        else:
            newData.append(item)
    
    img.putdata(newData)
    ship = ship.replace("Default.png", ".png")
    img.save(ship)


window = tk.Tk()
window.title("Config")

canvas = tk.Canvas(window, background="black")
#Code from: https://stackoverflow.com/questions/3380726/converting-a-rgb-color-tuple-to-a-six-digit-code-in-python
canvas.grid(column=0,row=0,columnspan=3)


asteroidColorButton = tk.Button(window, text="Choose color of asteroids", command=colorAsteroids)
asteroidColorButton.grid(column=0,row=3,columnspan=1)

playerColorButton = tk.Button(window, text="Choose color of player", command=colorPlayer)
playerColorButton.grid(column=1,row=3,columnspan=1)

droneColorButton = tk.Button(window, text="Choose color of drone", command=colorDrone)
droneColorButton.grid(column=2,row=3,columnspan=1)


color = '#%02x%02x%02x' % (139, 69, 19)
canvas.create_polygon(playerPoints, outline='#222222', fill='#ffffff', width=5)
canvas.create_polygon(dronePoints, outline='#222222', fill='#ffffff', width=2)
drawAsteroids(color)

debugSelected = tk.IntVar()
debugMode = tk.Checkbutton(text="Debug mode? (Warning will cause the program to slow down)", variable=debugSelected, onvalue=True, offvalue=False)
debugMode.grid(column=0,row=4,columnspan=3)

LaunchButton = tk.Button(window, text="Train", command=lambda: bootTraining())
LaunchButton.grid(column=0,row=5,columnspan=1)

LaunchButton = tk.Button(window, text="Play", command=lambda: bootGame())
LaunchButton.grid(column=2,row=5,columnspan=1)

#Reset player and drone ship color
changeShipColor(r"sprites/playerDefault.png", "0xffffff", playerPoints)
changeShipColor(r"sprites/droneDefault.png", "0xffffff", dronePoints)


window.mainloop()