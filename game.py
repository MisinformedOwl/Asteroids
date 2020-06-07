import pygame
import random
import math
from PIL import Image
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
        
    def draw(self, win):
        xend = self.x - velXcalc(self.direction,self.x,self.vel)
        yend = self.y - velYcalc(self.direction,self.y,self.vel)
        pygame.draw.line(win, self.colour, (self.x, self.y), (xend,yend), 2)
    
    def move(self, win):
        self.x = self.x - velXcalc(self.direction,self.x,self.vel)
        self.y = self.y - velYcalc(self.direction,self.y,self.vel)
        self.draw(win)
        if self.gone():
            return True
        else:
            return False
        
    def gone(self):
        if self.x > screenSize or self.x < 0:
            return True
        elif self.y > screenSize or self.y < 0:
            return True
        else:
            return False
    
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

class meteor():
    x = 0
    y = 0
    size = 0
    vel = 0
    direction = 0
    colour = (139,69,19)
    
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
        else:
            self.size = parent.size
            if self.size/2 < 15:
                return
            self.x = parent.x
            self.y = parent.y
            self.size = self.size/2
            self.vel = parent.vel/1.5
            self.direction = rot
        self.draw(win)
        
    def draw(self, win):
        pygame.draw.ellipse(win, self.colour, 
                            (self.x,self.y,self.size,self.size))
        
    def move(self, win):
        self.x = self.x + self.vel*math.sin(self.direction/57.2)
        self.y = self.y + self.vel*math.cos(self.direction/57.2)
        self.x, self.y = fixPos(self.x, self.y)
        self.draw(win)

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

def rotatePlayer(x,y,rot, playerChar, win, center):
    x = x - playerChar.get_width() / 2
    y = y - playerChar.get_height() / 2
    playerChar = pygame.transform.rotate(playerChar, rot)
    
    move = center - playerChar.get_width()/2
    
    win.blit(playerChar, (x+move,y+move))

##############################################################################

def movePlayer(x,y,velx,vely):
    x = x - velx
    y = y - vely
    x,y = fixPos(x,y)
    return x,y
    

##############################################################################

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

def velXcalc(rot, velx, boost):
    rot = rot % 360
    x = math.sin(rot/57.2)*boost
    return x

##############################################################################

def velYcalc(rot, vely, boost):
    rot = rot % 360
    y = math.cos(rot/57.2)*boost
    return y

##############################################################################

def scoreBoard(win, score):
    text = Fon.render(f"{score}", True, (255,255,255))
    textRect = text.get_rect()
    win.blit(text, textRect)
    

##############################################################################

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
    timeDelayBullet = 0
    timeDelayBullet = time.time()
    
    metSpawn = True
    
    run = True
    while run:
        pygame.time.delay(33)
        
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
        
        for bull in bullets:
            oob = bull.move(win)
            mets, hit = bull.shot(mets)
            if hit:
                score += 1
                bullets.remove(bull)
            elif oob:
                bullets.remove(bull)
        
        for mete in mets:
            mete.move(win)
            if mete.collision(x-playerSize/2,y-playerSize/2,playerSize):
                run = False
        
        if round(time.time(), 0) % 3 == 0 and len(mets) < screenSize/90:
            metSpawn = False
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