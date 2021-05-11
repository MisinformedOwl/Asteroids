import pygame
import random
import math
import time
import threading
from queueThreads import queue
import memory
import ModelSave
from fuzzsetup import fuzzSetup

#Initialise global variables which are repeatedly used throughout the system
#Asteroid color is reguired to prevent crashes as the meteors need a color to work with. However setting that colour directly results in the
#Inability to change it later. Therefore this is required
asteroidColor = (139,69,19)
screenSize = 1000

#This section is for rule based learning functions
#%%
"""
Used to update the weights of the rules used.
"""
def update(rules, rulesUsed, score, endTime):
    #For every rule that was used
    for rule in rulesUsed.items():
        #If the rule was used a second before death
        if endTime - rule[1] < 1:
            rules[rule[0]].weight -= 10
        #else if the rule was not seen for longer than a second ago
        else:
            rules[rule[0]].weight += score - 10
    return rules

"""
This function updates the lines in memory so that they may be used in predict
"""
def updateMoves(dangerLevel, lines):
    #For exery line
    for line in range(1,q.size()+1):
        #Get the distance of that line from the global queue
        close = q.nextItem()
        dangerLevel.input['Closeness'] = close
        #A few cases where closeness was a null value This fixes the issue
        try:
            dangerLevel.compute()
            danger = round(dangerLevel.output['Danger'])
        except:
            danger = 50
        #Based on the danger value assign it a low, med or high danger value
        if danger <= 33:
            setattr(lines, f"line{line}", "low")
        elif danger <= 66:
            setattr(lines, f"line{line}", "med")
        else:
            setattr(lines, f"line{line}", "high")
    return lines

"""
This function is responcible for selecting which move gets used
"""
def predict(rules, lines):
    #Extreamly low highest value so that all moves are caught in the worst case scenario
    highest = -111111
    selected = ()
    #This variable is used to mark which rules get used
    rule = 0
    #For every rule in rules
    for i in range(len(rules)):
        #If the situation matches the rule
        if rules[i].antecedentA == lines.line1 and rules[i].antecedentB == lines.line2 and rules[i].antecedentC == lines.line3 and rules[i].antecedentD == lines.line4 and rules[i].antecedentE == lines.line5 and rules[i].antecedentF == lines.line6 and rules[i].antecedentG == lines.line7 and rules[i].antecedentH == lines.line8:
            #And is the highest valued move in terms of weighting
            if rules[i].weight > highest:
                #The highest is updated
                highest = rules[i].weight
                selected = rules[i].move
                rule = i
    
    #In the event that no rule is selected
    if rule == 0:
        #Make the bot do nothing
        selected = (0,0,0,0)
    return selected, rule


"""
This function is responcible for the sight lines extending from the AI drone
"""
def detection(width, height, rot):
    distance = 0
    x = width
    y = height
    #Used to determing the starting cordinates for pythagoras
    orgy = 0
    orgx = 0
    #Due to a bug in which the program got endlessly stuck in a loop a lifetime had to be added.
    lifetime = 0
    #While the x and y has not moved off screen and the lifetime has not surpassed 1000 iterations
    while x < win.get_width() and y < win.get_height() and lifetime < 1000:
        lifetime+=1
        #Move X and Y
        x = lineXcalc(rot, x, 1)
        y = lineYcalc(rot, y, 1)
        #Fix position to allow the line to travel to the other side of the screen as ships and asteroids can.
        #This was implemented due to the AI killing itself by being unableto see asteroids on the other side of the screen.
        #Resulting in bad performance and a lack of learning.
        x,y, moved = fixPos(x,y)
        #should the x and y leave the screen then catch this error and return nothing. (This still suprisingly works even though the x and y get reset)
        try:
            #If the asteroid color input by the GUi is spotted at that pixel. then
            if (asteroidColor[0], asteroidColor[1], asteroidColor[2]) == win.get_at((round(x),round(y))):
                if debug:
                    pygame.draw.line(win,(255,255,255),(width,height),(round(x),round(y)))
                #Perform pythagoras to determine the distance and add to the queue then break out of the while loop.
                orgy = y - height
                orgx = x - width
                distance = math.sqrt(orgx ** 2 + orgy ** 2)
                q.add(distance)
                break
        except:
            #Alternaticvly if nothing is spotted add 1000 to the queue and break.
            q.add(1000)
            break

#%%
"""
The game over screen, used to present to the user that they have died aswell as presenting to them their score.
"""
def GameOver(win, score):
    win.fill((0,0,0))
    font = pygame.font.Font("fonts/Slaytanic.ttf", screenSize//10)
    text = font.render('Game Over', True, (255,255,255), None)
    textRect = text.get_rect()
    textRect.center = (screenSize//2, screenSize//2-screenSize//10-10)
    
    text2 = font.render("Your score was...", True, (255,255,255))
    textRect2 = text2.get_rect()
    textRect2.center = (screenSize/2, screenSize//2)
    
    num = Fon.render(f"{score}", True, (255,255,255))
    numRect = num.get_rect()
    numRect.center = (screenSize/2, screenSize/2+screenSize//10+10)
    
    win.blit(text, textRect)
    win.blit(text2,textRect2)
    win.blit(num, numRect)
    
    pygame.display.update()
    
    #Stays on the screen for 4 seconds.
    time.sleep(4)
    

#%%
"""
This is the bullet class section. Responcible for managing the behaviour of fired bullets.
"""
#Class for bullets the ship shoots
class bullet():
    x = 0
    y = 0
    size = 10
    vel = 15
    direction = 0
    colour = (255,255,255)
    lifetime = 20
    alive = 0
    moved = False
    
    def __init__(self,x,y,direction, win):
        self.x = x
        self.y = y
        self.direction = direction
        self.draw(win)
        
#This subroutine draws the shot in relaiton to its direction and velocity
    def draw(self, win):
        xend = self.x - velXcalc(self.direction,self.x,self.vel)
        yend = self.y - velYcalc(self.direction,self.y,self.vel)
        pygame.draw.line(win, self.colour, (self.x, self.y), (xend,yend), 2)

#Moves over the shot, not to be confused with draw which simply extends out 
#from what is created here.
    def move(self, win):
        #Move x and y to new location
        self.x = self.x - velXcalc(self.direction,self.x,self.vel)
        self.y = self.y - velYcalc(self.direction,self.y,self.vel)
        self.x, self.y, self.moved = fixPos(self.x, self.y)
        #Return if the object is out of bounds. or is to be removed.
        if self.gone() and self.moved == True:
            return True
        elif self.moved == True and self.alive > self.lifetime:
            return True
        else:
            self.draw(win)
            return False

#Check if bullet has gone off the screen. or if the lifetime has expired
    def gone(self):
        if self.x > screenSize or self.x < 0:
            return True
        elif self.y > screenSize or self.y < 0:
            return True
        elif self.alive > self.lifetime:
            return True
        else:
            return False

#Thsi function returns if a bullet has entered a meterors range.
    def shot(self, mets):
        #Some errors occour and cause crashes, this try catch statement solves this issue and simply turns the crash into a miss.
        try:
            hit = False
            self.alive += 1
            #For every meteor
            for met in mets:
                x = met.x
                y = met.y
                distance = math.sqrt(math.pow(x-self.x,2) + math.pow(y-self.y,2))
                #Calculate the distance to the meteor. if in range then collide.
                if distance < met.size/2:
                    #Create 2 new meteors that have split from this meteor.
                    newMet = meteor(win, met, met.direction-30, 1)
                    #However if the met is too small do not create it.
                    if newMet.size < 15:
                        #Some crashes have occoured when attempting to remove meteors that dont exist anymore. this happens when multiple metoers are layered on each other and are shot
                        #To avoid this i simply state that the shot hit and move on.
                        try:
                            mets.remove(met)
                        except:
                            hit = True
                            continue
                        return mets, True
                    mets.append(newMet)
                    mets.append(meteor(win, met, met.direction+30, 1))
                    mets.remove(met)
                    hit = True
            return mets, hit
        except:
            return mets, False

#%%
"""
This is the meteor file section, this managed the creation of asteroids aswell as management.
On top of this there is a fucntion to detect collision by detecting the distance in pythagoras between
the 2 half radius' of both objects
"""
#Class for meteors.
class meteor():
    x = 0
    y = 0
    size = 0
    vel = 0
    direction = 0
    colour = asteroidColor
    
#Since python doesn't have a way of creating multipel construction
#methods i had to add a few extra parameters which automatically return None.
    def __init__(self, win, parent=None, rot=None, split=None):
        #If this is not the child of a previous asteroid which has been shot
        if split == None:
            
            #Choose which side the meteor will spawn
            side = random.randint(1,4)
            #Give a random rotation
            self.direction = random.randint(0,360)
            #Then assign the cordinates
            if side == 1:
                self.x = random.randint(0,screenSize)
            if side == 2:
                self.y = random.randint(0,screenSize)
            if side == 3:
                self.x = random.randint(0,screenSize)
                self.y = screenSize
            else:
                self.x = screenSize
                self.y = random.randint(0,screenSize)
            
            self.vel = random.uniform(0.5,3)
            self.direction = random.randint(0,359)
            self.size = random.randint(15, 50)
        #However if this is a child
        elif split != None:
            #And the size is greater than 15
            if parent.size/2 < 15:
                return
            #else create a new asteroid that is half of the size of the parent and is slightly slower
            #Which also goes in a slightly different direction
            self.size = parent.size/2
            self.x = parent.x
            self.y = parent.y
            self.vel = parent.vel/1.5
            self.direction = rot
        self.draw(win)
        
#Draws the meteor
    def draw(self, win):
        pygame.draw.ellipse(win, self.colour, 
                            (self.x-self.size/3, self.y-self.size/3, self.size, self.size))

#Moves the meteor and check if the meteor has gone off the screen.
    def move(self, win):
        self.x = self.x + self.vel*math.sin(self.direction/57.2)
        self.y = self.y + self.vel*math.cos(self.direction/57.2)
        self.x, self.y, moved = fixPos(self.x, self.y)
        #Moved is a variable which is not required at all here. however is needed by others who call this function.
        #Done this to save space
        del(moved)
        self.draw(win)

#Check if the meteor has collided with the player
    def collision(self,x,y, size):
        x = x + size/2
        y = y + size/2
        #Using pythagoras get the distance
        distance = math.sqrt(math.pow(x-self.x,2))+math.sqrt(math.pow(y-self.y,2))
        
        #Debug menu shows the distance from collision. 
        #Required as old collision was very bad.
        if debug:
            text = Fon.render(f"{round(distance - (size/2 + self.size-5))}", True, (255,255,255))
            textRect = text.get_rect()
            textRect.center = (self.x-20, self.y-20)
            win.blit(text,textRect)
        
        #If both halves are less than the distance between the objects then a collision has occoured.
        if distance < size/2 + self.size-5:
            return True

        return False

#%%
"""
The drone class. This contains alot of the functionality found in the AI.
"""
class drone:
    rot = 0
    x,y = 0,0
    velx,vely = 0,0
    
    #Custom drone image selected
    droneChar = pygame.image.load("sprites/drone.png")
    droneSize = droneChar.get_width()
    lines = memory.workingMemory()
    timeDelayBullet = 0
    threadlist = []
    lineAmmount = 8
    incrementLine = 360/lineAmmount
    dead = False
    
    def __init__(self, x, y, velx, vely, rot):
        self.x = x
        self.y = y
        self.rot = rot
        self.velx = velx
        self.vely = vely
        #creation time for when the bullets are allowed to fire
        self.timeDelayBullet = time.time()
        
    #Draws the drone
    def draw(self, win):
        cent = self.droneSize/2
        self.x, self.y = movePlayer(self.x,self.y,self.velx,self.vely)
        #Funnily enough there is no good rotate function in pygame. I therefore had to make my own. using some clever tricks to keep the ship in the center
        rotatePlayer(self.x,self.y,self.rot, self.droneChar, win, cent)
        
    #Moving using the save methods as before.
    def move(self,win):
        self.x = self.x + self.velx*math.sin(self.rot/57.2)
        self.y = self.y + self.vely*math.cos(self.rot/57.2)
        self.x, self.y, moved = fixPos(self.x, self.y)
        del(moved)
        self.draw(win)

#Check if the meteor has collided with the player
    def collision(self, mets):
        for met in mets:
            x = met.x + met.size/2
            y = met.y + met.size/2
            distance = math.sqrt(math.pow(x-self.x,2))+math.sqrt(math.pow(y-self.y,2))
            if distance < met.size/2 + self.droneSize:
                self.dead = True

    def MakeMove(self, move, bullets):
        #Decides what move the AI will make based on the next few class functions.
        if move[0] == 1:
            self.velx = self.velx + velXcalc(self.rot,self.velx,0.3)
            self.vely = self.vely + velYcalc(self.rot,self.vely,0.3)
            
        if move[3] == 1:
            self.velx = self.velx - self.velx/10
            self.vely = self.vely - self.vely/10
            
        if move[1] == 1:
            self.rot = self.rot + 5
        
        if move[2] == 1:
            self.rot = self.rot - 5
            
        #If it has been half a second since the last shot. shoot.
        if time.time() - self.timeDelayBullet > 0.5:
            bullets.append(bullet(self.x,self.y,self.rot,win))
            self.timeDelayBullet = time.time()
    
    #This function is used sort out danger and sight lines. which is then worked on by update moves aswell as predict.
    def dangerSense(self, ruleslist, dangerLevel, bullets):
        for i in range(self.lineAmmount):
            t = threading.Thread(target=detection, args=[self.x, self.y, self.rot + (self.incrementLine*i)], daemon=True)
            self.threadlist.append(t)
        
        for t in self.threadlist:
            try:
                t.start()
            except:
                continue
            
        for t in self.threadlist:
                t.join()
        
        self.lines = updateMoves(dangerLevel, self.lines)
        move, rule = predict(ruleslist,self.lines)
        #Since this AI is not learning we do not need the mark which rule was collected.
        del(rule)
        #Using the processed data we can now update the drone.
        self.MakeMove(move, bullets)

#%%
"""
This area manages game functionality. such as rotation and calculation velocity.
"""

"""
This section was used to calculate alot of the movement that is presented in this program.
"""
#Calculate the X cordinate after rotation and velocity is applied
def lineXcalc(rot, velx, boost):
    rot = rot % 360
    #Not sure why but 57.2 seems to be the golden number in regards to movement.
    #Got this number after alotof tweaking.
    x = velx + math.sin(rot/57.2)*boost
    return x

#Calculate the Y cordinate after rotation and velocity is applied
def lineYcalc(rot, vely, boost):
    rot = rot % 360
    y = vely + math.cos(rot/57.2)*boost
    return y


"""
This section like the last is similar however does not update the valocity. instead only returns the difference.
"""
#Calculate the X cordinate after rotation and velocity is applied
def velXcalc(rot, velx, boost):
    rot = rot % 360
    x = math.sin(rot/57.2)*boost
    return x



#Calculate the Y cordinate after rotation and velocity is applied
def velYcalc(rot, vely, boost):
    rot = rot % 360
    y = math.cos(rot/57.2)*boost
    return y



"""
Perhaps the biggest challenge in early development was this stage. Which had me scratching my head during lockdown.
Basically there is no turn function. The only turn function available turns the whole image around,
Essencailly meaning as the image turns the center of the image is moved. Resulting in the image neverstaying in place.
This was not acceptable therefore i came up with a solution for this problem.

The solution was to simply get the distance from the center and remove the differance as the object rotated. Therefore always keeping it central.
"""
def rotatePlayer(x,y,rot, playerChar, win, center):
    x = x - playerChar.get_width() / 2
    y = y - playerChar.get_height() / 2
    #Rotate
    playerChar = pygame.transform.rotate(playerChar, rot)
    
    #Grab how much needs to be moved in regards to the center of the image
    move = center - playerChar.get_width()/2
    
    #Apply this movement
    win.blit(playerChar, (x+move,y+move))



#Moves the player and check if they have gone off the screen.
def movePlayer(x,y,velx,vely):
    x = x - velx
    y = y - vely
    x,y, moved = fixPos(x,y)
    return x,y
    


"""
Fix position is incredibly important as if it used by everything in this game. as can be seen in past code
Its objective is the move one object to the other side of the screen. and mark if the object has been moved.
The moved variable is for sight lines aswell as bullets.
"""
def fixPos(x,y):
    moved = False
    if x > screenSize:
        moved = True
        x = 0
    elif x < 0:
        x = screenSize
        moved = True
    if y > screenSize:
        y = 0
        moved = True
    elif y < 0:
        y = screenSize
        moved = True
    
    
    return x, y, moved

"""
A very basic scoreboard which displays the score to the user as the game goes on.
"""
def scoreBoard(win, score):
    text = Fon.render(f"{score}", True, (255,255,255))
    textRect = text.get_rect()
    win.blit(text, textRect)

"""
A seperate function for managing drones. Originally you were supposed to have multiple drones on the screen, however due to performance problems aswell as crashes and difficulty incorporating this this was dropped.
"""
def droneManagement(drone, mets, bullets, ruleslist, dangerLevel):
    #If the drone exists
    if drone:
        drone.collision(mets)
        drone.dangerSense(ruleslist, dangerLevel, bullets)
        drone.move(win)

#%%
"""
This is the method used to train the drones
There is another method similar to this to play the game. However i wanted to split these up as i want the AI to be able to train on its own without any outside interferance.
For example the player. This functions just abouyt the same as the play function however has some added parts in regards to updating the AI aswell as saving it.
"""

#Contains the game loop aswell as player variables
def train(debugselected, asteroidColorSelected):
    #Using variables applied in the GUI
    global asteroidColor
    asteroidColor = asteroidColorSelected
    
    meteor.colour = asteroidColor
    
    #initialise game and fonts
    pygame.init()
    pygame.font.init()
    
    #Create the font to be used throughout the program.
    global Fon
    Fon = pygame.font.Font("fonts/Crashnumberinggothic-MAjp.ttf", 50)
    
    #Set screen size and screen name.
    global win
    win = pygame.display.set_mode((screenSize, screenSize))
    pygame.display.set_caption("Meteors")
    
    global debug
    debug = debugselected
    
    #Creates cutom global queue
    global q
    q = queue()
    
    #If there is a model available then sue that. Else, create one from scratch 
    #(If you wish to create one from scratch go into the files and either rename the model.pickle or delete it)
    try:
        ruleslist = ModelSave.loadModel()
    except:
        ruleslist = memory.Initialize()
    
    #Create the lines memory
    lines = memory.workingMemory()
    
    #Setup fuzzy logic danger detection.
    dangerLevel = fuzzSetup()
    
    
    epoch = 1
    
    #Permenantly run the program until it is closed.
    while True:
        #This is repeated upon failing the game, and therefore many variables here are wiped clean.
        x = screenSize/2
        y = screenSize/2
        velx,vely = 0,0
        rot = 0
        score = 0
        mets = []
        bullets = []
        playerChar = pygame.image.load("sprites/player.png")
        playerSize = playerChar.get_width()
        timeDelayMet = time.time()
        timeDelayBullet = time.time()
        
        
        #Creates however many lines are being used, aswell as their equally seperated rotation.
        threadlist = []
        lineAmmount = 8
        incrementLine = 360/lineAmmount
        
        rulesUsed = {}
        
        startTime = time.time()
        
        run = True
        #When the game is actually being played.
        while run:
            #This is a time delay to slow down the frame rate. Important to get right as bullets are based on time, where as the speed of the game is linked to the frame rate
            #Too fast and asteroids are flying too quick to shoot. Too slow and you end up with the most boring game of bullet hell.
            pygame.time.delay(23)
            
            #For every meteor, move it and check for any collision with the player
            for mete in mets:
                mete.move(win)
                #If collided end the game loop
                if mete.collision(x-playerSize/2,y-playerSize/2,playerSize):
                    run = False
            
            #Draw collision area if debug is on.
            if debug:
                pygame.draw.ellipse(win, (255,0,0),(x-playerSize/2,y-playerSize/2, playerSize,playerSize))
            
            #Added one due to it causing an error. 
            dangerLevel.input['Meteors'] = len(mets)+1
            
            #Threading to sevearly improve performance. This is where the sight lines are called and used.
            for i in range(lineAmmount):
                t = threading.Thread(target=detection, args=[x, y, rot + (incrementLine*i)])
                threadlist.append(t)
            
            #For every thread created for every line of sight
            for t in threadlist:
                try:
                    t.start()
                except:
                    continue
            
            #Wait for the threads to finish before continuing.
            for t in threadlist:
                t.join()
            
            #Update the lines in memeory with new values
            lines = updateMoves(dangerLevel, lines)
            
            #Based on this change in lines, predict the best move
            move, rule = predict(ruleslist,lines)
            
            #Because we are training we must mark when the rule was used.
            rulesUsed.update({rule : time.time()})
            
            #If the x is clicked then save the model and quit.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            #Move AI based on prediction
            if move[0] == 1:
                velx = velx + velXcalc(rot,velx,0.3)
                vely = vely + velYcalc(rot,vely,0.3)
                
            if move[3] == 1:
                velx = velx - velx/10
                vely = vely - vely/10
                
            if move[1] == 1:
                rot = rot + 5
            
            if move[2] == 1:
                rot = rot - 5
            
            #Create a time delay on how fast bullets can be fired. 
            #due to it being too long to train (Literally doubles the rules available)
            #The ability to choose to fire was not implemented.
            if time.time() - timeDelayBullet > 0.5:
                bullets.append(bullet(x,y,rot,win))
                timeDelayBullet = time.time()
            
            #For every bullet, check if it is out of bounds and if it has hit anything
            for bull in bullets:
                oob = bull.move(win)
                mets, hit = bull.shot(mets)
                if hit:
                    score += 1
                    bullets.remove(bull)
                elif oob:
                    bullets.remove(bull)
            
            #if the time hits the time mark, spawn meteors
            #Also check if there are less than 50 meteors.
            if time.time() - timeDelayMet > 1 and len(mets) < 50:
                timeDelayMet = time.time()
                try:
                    mets.append(meteor(win, asteroidColor))
                except:
                    print("There was a error")
                    pass
            
            #Update the on screen information aswell as moving the player to the new position.
            ammount = Fon.render(f"{len(mets)}", True, (255,255,255))
            win.blit(ammount, (300,100,0,0))
            epochText = Fon.render(f"{epoch}", True, (255,255,255))
            win.blit(epochText, (300,0,0,0))
            scoreBoard(win, score)
            
            #Score              Epoch
            #                   Meteor count
            
            
            cent = playerSize/2
            x, y = movePlayer(x,y,velx,vely)
            rotatePlayer(x,y,rot, playerChar, win, cent)
            pygame.display.update()
            win.fill((0,0,0))
        
        #When the AI inevitably crashes
        #Grab the time the game ended (Used in updating rules)
        endTime = time.time()
        #Show the game over screen
        GameOver(win, score)
        #Update the score based on time survived. and update the rules list.
        score = score * (((time.time()  - startTime) / 30) + 1)
        ruleslist = update(ruleslist, rulesUsed, score, endTime)
        ModelSave.saveModel(ruleslist)
        epoch = epoch + 1

"""
A seperate function for shooting bullets. This is due to bullets hitting performance hard, this fixes the issue by sending the problem to be managed by threads.
This is used in the play function due to there being double the bullets.
"""
def shootBullet(bull):
    global mets
    global score
    #oob = object out of bounds
    oob = bull.move(win)
    mets, hit = bull.shot(mets)
    if hit:
        score += 1
        bullets.remove(bull)
    elif oob:
        bullets.remove(bull)
        
#%%
"""
This method is the main method to play asteroids with drone AI
"""

#Contains the game loop aswell as player variables
def play(debugselected, asteroidColorSelected):
    global asteroidColor
    asteroidColor = asteroidColorSelected
    
    meteor.colour = asteroidColor
    
    #initialise game and fonts
    pygame.init()
    pygame.font.init()
    
    global Fon
    Fon = pygame.font.Font("fonts/Crashnumberinggothic-MAjp.ttf", 50)
    
    #Set screen size and screen name.
    global win
    win = pygame.display.set_mode((screenSize, screenSize))
    pygame.display.set_caption("Meteors")
    
    global debug
    debug = debugselected
    
    global q
    q = queue()
    
    global mets
    
    global bullets
    
    global score
    score = 0
    
    modelPre = True
    if modelPre:
        ruleslist = ModelSave.loadModel()
    else:
        ruleslist = memory.workingMemory.Initialize()
        
    lines = memory.workingMemory()
    
    dangerLevel = fuzzSetup()
    
    while True:
        mets = []
        bullets = []
        x = screenSize/2
        y = screenSize/2
        velx,vely = 0,0
        rot = 0
        playerChar = pygame.image.load("sprites/player.png")
        playerSize = playerChar.get_width()
        timeDelayMet = time.time()
        timeDelayBullet = time.time()
        
        threadlist = []
        lineAmmount = 8
        incrementLine = 360/lineAmmount
        
        rulesUsed = {}
        
        startTime = time.time()
        
        run = True
        while run:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            #key events
            #This contains all keyboard events
            #Note this for some reason upon closing the program creates a pygame error.
            #There is seemingly no reason for this as the error is becasue pygame isn't initialised. However quite clearly in line 754 it is.
            keys = pygame.key.get_pressed()
            
            #Up arrow
            if keys[pygame.K_UP]:
                velx = velx + velXcalc(rot,velx,0.3)
                vely = vely + velYcalc(rot,vely,0.3)
            
            #Down arrow        
            if keys[pygame.K_DOWN]:
                velx = velx - velx/10
                vely = vely - vely/10
            
            #left arrow
            if keys[pygame.K_LEFT]:
                rot = rot + 5
            
            #Right arrow
            if keys[pygame.K_RIGHT]:
                rot = rot - 5
            
            #Space bar
            if keys[pygame.K_SPACE]:
                if time.time() - timeDelayBullet > 0.5:
                    bullets.append(bullet(x,y,rot,win))
                    timeDelayBullet = time.time()
            
            #F key to summon a drone. Warning every summoning of a drone results in worsening performance.
            if keys[pygame.K_f] and "drone1" not in locals():
                drone1 = drone(x,y,velx,vely,rot)
            
            #For some reason this does not like using if drone1. Therefore i had to check the local variables instead.
            #Found the solution on how to do this here...
            #https://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists
            if "drone1" in locals():
                pygame.time.delay(5)
            else:
                pygame.time.delay(40)
            
            #For every meteor, move it and check for any collision with the player
            for mete in mets:
                mete.move(win)
                #If collided end the game loop
                if mete.collision(x-playerSize/2,y-playerSize/2,playerSize):
                    run = False
            
            if debug:
                pygame.draw.ellipse(win, (255,0,0),(x-playerSize/2,y-playerSize/2, playerSize,playerSize))
            
            #Added one due to it causing an error.
            dangerLevel.input['Meteors'] = len(mets)+1
            
            #If drone exists
            if "drone1" in locals():
                droneActivity = threading.Thread(target=droneManagement, args=(drone1, mets, bullets, ruleslist, dangerLevel))
                droneActivity.start()
            
                if drone1.dead:
                    del(drone1)
                
            #Bullet threads start (Performance fixer)
            for bull in bullets:
                bullthread = threading.Thread(target=shootBullet, args=(bull,))
                bullthread.start()
            
            if time.time() - timeDelayMet > 1 and len(mets) < 50:
                timeDelayMet = time.time()
                try:
                    mets.append(meteor(win, asteroidColor))
                except:
                    print("There was a error")
                    pass
            
            
            #Update the board ect and move the player again. However at the end wait for the drone threads to finish.
            #The drone threads were moved here due to how long it actually takes for them to complete their tasks. 
            #Giving them some extra time saves miliseconds on performance, which is useful when things get hectic in the late stages ofthe game.
            scoreBoard(win, score)
            cent = playerSize/2
            x, y = movePlayer(x,y,velx,vely)
            rotatePlayer(x,y,rot, playerChar, win, cent)
            pygame.display.update()
            win.fill((0,0,0))
            if "drone1" in locals():
                droneActivity.join()
        
        if "drone1" in locals():
            del(drone1)
        endTime = time.time()
        GameOver(win, score)
        score = 0