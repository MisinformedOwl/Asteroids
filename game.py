import pygame
import random
import math
import time

#Made screenSize global as it is passed around alot. Less...
#Management over varaibles
global screenSize
screenSize = int(input("Screen size (In pixels): "))

#initialise game and fonts
pygame.init()
pygame.font.init()

Fon = pygame.font.Font("fonts/Crashnumberinggothic-MAjp.ttf", 50)

#Set screen size and screen name.
win = pygame.display.set_mode((screenSize, screenSize))
pygame.display.set_caption("Meteors")

##############################################################################

#Create game over screen and present to user
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
    
    time.sleep(4)
    
    
##############################################################################

#Class for bullets the ship shoots
class bullet():
    x = 0
    y = 0
    size = 10
    vel = 15
    direction = 0
    colour = (255,255,255)
    
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
        self.x = self.x - velXcalc(self.direction,self.x,self.vel)
        self.y = self.y - velYcalc(self.direction,self.y,self.vel)
        self.draw(win)
        if self.gone():
            return True
        else:
            return False
        
#Check if bullet has gone off the screen.
    def gone(self):
        if self.x > screenSize or self.x < 0:
            return True
        elif self.y > screenSize or self.y < 0:
            return True
        else:
            return False
    
#Thsi function returns if a bullet has entered a meterors range.
    def shot(self, mets):
        for met in mets:
            x = met.x+met.size/2
            y = met.y+met.size/2
            distance = math.sqrt(math.pow(x-self.x,2) + math.pow(y-self.y,2))
            if distance < met.size/2:
                mets.append(meteor(win, met, met.direction-30, 1))
                mets.append(meteor(win, met, met.direction+30, 1))
                mets.remove(met)
                return mets, True
        return mets, False

##############################################################################

#Class for meteors.
class meteor():
    x = 0
    y = 0
    size = 0
    vel = 0
    direction = 0
    colour = (139,69,19)
    
#Since python doesn't have a way of creating multipel construction
#methods i had to add a few extra parameters which automatically return None.
    def __init__(self, win, parent=None, rot=None, split=None):
        if split == None:
            side = random.randint(1,4)
            self.direction = random.randint(0,360)
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
        elif split != None:
            if parent.size/2 < 18:
                return
            self.size = parent.size/2
            self.size = parent.size
            self.x = parent.x
            self.y = parent.y
            self.size = parent.size/2
            self.vel = parent.vel/1.5
            self.direction = rot
        self.draw(win)
        
#Draws the meteor
    def draw(self, win):
        pygame.draw.ellipse(win, self.colour, 
                            (self.x,self.y,self.size,self.size))
        
#Moves the meteor and check if the meteor has gone off the screen.
    def move(self, win):
        self.x = self.x + self.vel*math.sin(self.direction/57.2)
        self.y = self.y + self.vel*math.cos(self.direction/57.2)
        self.x, self.y = fixPos(self.x, self.y)
        self.draw(win)

#Check if the meteor has collided with the player
    def collision(self,x,y, size):
        
        distance = math.sqrt(math.pow(x-self.x,2) + math.pow(y-self.y,2))
        
        # text = Fon.render(f"{round(distance,2)}", True, (255,255,255))
        # textRect = text.get_rect()
        # textRect.center = (self.x-20, self.y-20)
        # win.blit(text,textRect)
        
        if distance < size + self.size/2:
            return True
        
        return False

##############################################################################

#Rotate the player
def rotatePlayer(x,y,rot, playerChar, win, center):
    x = x - playerChar.get_width() / 2
    y = y - playerChar.get_height() / 2
    playerChar = pygame.transform.rotate(playerChar, rot)
    
    move = center - playerChar.get_width()/2
    
    win.blit(playerChar, (x+move,y+move))

##############################################################################

#Moves the player and check if they have gone off the screen.
def movePlayer(x,y,velx,vely):
    x = x - velx
    y = y - vely
    x,y = fixPos(x,y)
    return x,y
    

##############################################################################

#Check if object is out screen area and then send it to the other side.
def fixPos(x,y):
    if x > screenSize:
        x = 0
    elif x < 0:
        x = screenSize
    if y > screenSize:
        y = 0
    elif y < 0:
        y = screenSize
    
    return x, y

##############################################################################

#Calculate the X cordinate after rotation and velocity is applied
def velXcalc(rot, velx, boost):
    rot = rot % 360
    x = math.sin(rot/57.2)*boost
    return x

##############################################################################

#Calculate the Y cordinate after rotation and velocity is applied
def velYcalc(rot, vely, boost):
    rot = rot % 360
    y = math.cos(rot/57.2)*boost
    return y

##############################################################################

#Displays the score for the user in the top left.
def scoreBoard(win, score):
    text = Fon.render(f"{score}", True, (255,255,255))
    textRect = text.get_rect()
    win.blit(text, textRect)
    

##############################################################################

#Contains the game loop aswell as player variables
def play():
    
    x = screenSize/2
    y = screenSize/2
    velx,vely = 0,0
    rot = 0
    score = 0
    mets = []
    bullets = []
    playerChar = pygame.image.load("sprites/player.png")
    playerSize = playerChar.get_width()/2
    timeDelayMet = time.time()
    timeDelayBullet = time.time()
    
    run = True
    while run:
        pygame.time.delay(33)
        
        #This contains all keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            velx = velx + velXcalc(rot,velx,0.3)
            vely = vely + velYcalc(rot,vely,0.3)
            
        if keys[pygame.K_DOWN]:
            velx = velx - velx/10
            vely = vely - vely/10
            
        if keys[pygame.K_LEFT]:
            rot = rot + 5
        
        if keys[pygame.K_RIGHT]:
            rot = rot - 5
            
        if keys[pygame.K_SPACE]:
            if time.time() - timeDelayBullet > 0.5:
                bullets.append(bullet(x-playerSize/2,y-playerSize/2,rot,win))
                timeDelayBullet = time.time()
        
        #For every bullet, check if it is out of bounds and if it has hit 
        #anything
        for bull in bullets:
            oob = bull.move(win)
            mets, hit = bull.shot(mets)
            if hit:
                score += 1
                bullets.remove(bull)
            elif oob:
                bullets.remove(bull)
        
        #For every meteor, move it and check for any collision with the player
        for mete in mets:
            mete.move(win)
            #If collided end the game loop
            if mete.collision(x-playerSize/2,y-playerSize/2,playerSize):
                run = False
        
        #if the time hits the 3 second mark spawn meteors equal to the equation
        if time.time() - timeDelayMet > 2:
            timeDelayMet = time.time()
            mets.append(meteor(win))
        
        scoreBoard(win, score)
        cent = playerSize/2
        rotatePlayer(x,y,rot, playerChar, win, cent)
        x, y = movePlayer(x,y,velx,vely)
        pygame.display.update()
        win.fill((0,0,0))
    
    GameOver(win, score)

##############################################################################

play()

pygame.quit()