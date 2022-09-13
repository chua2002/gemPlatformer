import pygame
from time import sleep
import levelHolder
pygame.init()


window_x = 600
window_y = 600

display = pygame.display.set_mode((window_y,window_x))
clock = pygame.time.Clock()
pygame.display.set_caption("Gem")


lvl_0 = levelHolder.opening     #calling levels from levelHolder program
lvl_1 = levelHolder.downUp
lvl_2 = levelHolder.dirtShow
lvl_3 = levelHolder.dirtOverSpire
lvl_4 = levelHolder.dirtChasm
lvl_5 = levelHolder.lvl_dirtElevator
lvl_6 = levelHolder.upLedge
lvl_7 = levelHolder.lava1
lvl_8 = levelHolder.lava2
lvl_9 = levelHolder.lava3
lvl_10 = levelHolder.slimeIntro
lvl_11 = levelHolder.slime1
lvl_12 = levelHolder.slime2

lavaSpeedList = [ 0, 0, 0, 0, 0, 0, 0, 1.35, .95, 1, 0, 0, 0]   #values of lava speed for every level

class LevelBuilder:
    def __init__(self):
        self.lvlList = [lvl_0,lvl_1,lvl_2,lvl_3,lvl_4,lvl_5,lvl_6,
                        lvl_7,lvl_8,lvl_9,lvl_10,lvl_11,lvl_12]
        self.currentLvl = []    #contains every object in the current level
        self.respawnCoor = [0,0]    #where the player returns when they die/start new level
        self.done = False
        self.life = False
        self.lvlNum = 0
    def setLvl(self,p):
        self.lvlNum = p
        lvl = self.lvlList[p]
        self.currentLvl.clear()
        self.done = False
        y = 0
        for i in lvl:   #puts every object into a list
            x = 0
            for j in i:
                if j == 1: self.currentLvl.append(Block(x * 30, y * 30, 30, 30))
                elif j == 2: self.respawnCoor = [x * 30 ,y * 30]
                elif j == 3: self.currentLvl.append(Block(x * 30, y * 30, 30, 30,"finish",(194, 193, 180)))
                elif j == 4: self.currentLvl.append(Dirt(x * 30, y * 30, 30, 30))
                elif j == 5: self.currentLvl.append(Lava(x*30,y*30+1))
                elif j == 6: self.currentLvl.append(Slime(x*30,y*30))
                x += 1
            y += 1
        self.currentLvl.sort(key=sortByY)
        self.lavaSpeed(lavaSpeedList[self.lvlNum])  #checks for what the lava list should be, then assigns it to every block
    def setDone(self): self.done = True
    def checkDone(self): return self.done
    def drawLvl(self):  #draws every object in the level
        for i in self.currentLvl:
            i.draw()
    def getlvl(self): return self.currentLvl    #returns every object in the level as a list
    def getRespawn(self): return self.respawnCoor
    def setLive(self,p): self.live = p
    def getLive(self): return self.live
    def lavaSpeed(self,p):  #goes through all lava objects
        for i in self.getlvl():
            if i.getType() == "lava":
                i.setRiseSpeed(p)


class Block():
    def __init__(self,x,y,w,h,t="normal",c=(107,107,107)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = c
        self.type = t #is used for different checks, such as lava, slime, or dirt

    def setCor(self,pX,pY,):
        self.x = pX
        self.y = pY
    def setSize(self,pW,pH):
        self.w = pW
        self.h = pH
    def setColor(self,c): self.color = c
    def draw(self):
        pygame.draw.rect(display,self.color,(self.x,self.y,self.w,self.h))
    def getCoor(self):  #used for collision checks
        return [self.x,self.y,self.x+self.w,self.y+self.h]
    def getType(self): return self.type
    def setType(self,p):
        self.type = p

class Dirt(Block):
    def __init__(self,x,y,w,h):
        self.fallTimer = 20
        self.setCor(x,y)
        self.Ix = x #initial x value
        self.Iy = y #initial y value
        self.setSize(w,h)
        self.setColor((171, 123, 60))
        self.setType("dirt")
        self.falling = False
        self.checkDepth = 25
        self.y_momentum = 0

    def reset(self):    #returns block to original location
        self.y = self.Iy
        self.x = self.Ix
        self.falling = False
        self.fallTimer = 20
        self.y_momentum = 0


    def fall(self): #if player touches the dirt block, it will wait 20 frames, then begin falling
        if self.fallTimer == 0 and self.falling:
            if self.y_momentum <= 22:
                self.y_momentum+=1
            self.y += self.y_momentum

        elif self.falling:
            self.fallTimer-= 1
            self.falling = True


    def yCollision(self):   #works the same way as player collision but only checks top of blocks
        for i in lvls.getlvl():
            if not i == self and not i.getType() == "lava":
                cords = i.getCoor()     #[left,top,right,bottom]
                if self.x+self.w> cords[0] and self.x < cords[2]:
                    if cords[1]+self.checkDepth > self.y+self.h > cords[1]:
                        self.y = cords[1]-self.h
                        self.y_momentum =0

    def startFall(self):
        self.falling = True

class Lava(Block):
    def __init__(self,x,y):
        self.setType("lava")
        self.setSize(30,29) #slightly shorter than normal blocks so player won't die if on another block
        self.setCor(x,y)
        self.setColor((255, 72, 0))
        self.riseSpeed = 0.0
        self.ogY = y    #original y
        self.ogH = 29 #original x

    def rise(self): #lava rises by the rise speed
        self.y -= self.riseSpeed
        self.h += self.riseSpeed
    def lavaReset(self):    #lava returns to original state
        self.y = self.ogY
        self.h = self.ogH
    def setRiseSpeed(self,p):
        self.riseSpeed = p

class Slime(Block):
    def __init__(self,x,y):
        self.setCor(x,y)
        self.setColor((126, 191, 128))
        self.setType("slime")
        self.setSize(30,30)

class Player(Block):
    def __init__(self):
        self.x_momentum = 0
        self.y_momentum = 0
        self.movingX = "N"
        self.jump_power = 16
        self.groundY = 0
        self.inAir = True
        self.jumping = False    #whether up is being held down
        self.checkDepth = 25
        self.willBounce = False #whether or not player is touching green block
        self.airCounter = 0.0

    def resetMomentum(self):
        self.x_momentum = 0
        self.y_momentum = 0
    def drawP(self):    #draws the player
        pygame.draw.rect(display,self.color,(self.x,self.y,self.w,self.h))
    def setCheckDepth(self,p):self.checkDepth = p
    def setBounce(self,p): self.willBounce = p
    def bounce(self,p):
        if self.willBounce: #if touching a green block
            if p == "x":    #if you touch the side of an object
                if self.x_momentum >4 or self.x_momentum <-4: return -1*round(self.x_momentum/2) #x momentum is halved and reversed
                else: return 0
            else:   #if you touch the top of an object
                if self.y_momentum < -10:
                    return round(self.airCounter*1.5)   #y momentum = the number of frames the player has been in the air *1.5
                else: return 0
        else: return 0

    def addXM(self,p=0):    #adds x-momentum and sets moving to 'L' or 'R'
        if not p == 0:
            if p > 0:
                self.movingX = "R"
                if self.x_momentum < 10: self.x_momentum += p
            elif p < 0:
                self.movingX = "L"
                if -10 < self.x_momentum: self.x_momentum +=p
        else: self.movingX= "N"
    def moveX(self):
        decelr = 3  #how much you decelerate per frame if not holding L or R
        if self.willBounce == True: decelr = 1  #you will 'slide' more if on a green block

        if not self.x_momentum == 0:
            self.x += self.x_momentum
            if self.movingX == "N": #if not holding left or right, acceleration will go torwards 0
                if self.x_momentum > 0:
                    self.x_momentum -= decelr
                    if self.x_momentum<0: self.x_momentum = 0
                elif self.x_momentum < 0:
                    self.x_momentum += decelr
                    if self.x_momentum>0: self.x_momentum = 0
    def moveY(self):
        if self.inAir:  #if in the air, player will be affected by y acceleration
            self.y -= self.y_momentum   #moves the player by its current speed
            if self.jumping == False and self.y_momentum>7: #if jump is released, you will start falling
                self.y_momentum -=3
            elif self.jumping == False and self.y_momentum>0:
                self.y_momentum -=2
            elif self.y_momentum > -22:
                self.y_momentum -= 1
            if self.y_momentum < 0: self.airCounter += 1    #this is stored for the bounce method

    def jump(self):
        if not self.inAir:  #checks if the player is in the air
            self.y_momentum = self.jump_power   #y-acceleration is instaniously set to a pre-determined value
            self.groundY = self.y
            self.inAir = True
            self.jumping = True

    def cutJump(self):  #if False, player will stop moving upward
        self.jumping = False

    def setMoving(self,p):self.movingX = p  #if p = 'N', the player cannot accelerate left or right

    def yCollision(self):
        self.inAir=True
        for i in lvls.getlvl():
            cords = i.getCoor()     #[left,top,right,bottom]
            if i.getType() == "finish": # Checks if player is on top of the level clear block
                if (self.x > cords[0] and self.x < cords[2]) or (self.x+self.w > cords[0] and self.x+self.w < cords[2]):
                    if cords[1]-2 < self.y + self.h < cords[1]+self.checkDepth:
                        lvls.setDone()  #if true, level will end


            elif self.x+self.w> cords[0] and self.x < cords[2]: #checks if player is within the correct x range to interact with the block
                if cords[1] < self.y+self.h < cords[1]+self.checkDepth and self.y_momentum < 0: #checks if player is touching top of the block
                    self.inAir = False
                    self.y = cords[1]-self.h
                    if i.getType() == "dirt":
                        i.startFall()
                    if i.getType() == "slime":
                        self.setBounce(True)    #allows player method 'bounce' to function if touching slime block
                    else: self.setBounce(False)
                    if i.getType() == "lava": lvls.setLive(False)   #kills player if touching lava
                    self.y_momentum = self.bounce("y")
                    self.airCounter = 0
                elif cords[3]-self.checkDepth < self.y < cords[3] and self.y_momentum >0:   #checks if player is touching bottom of the block
                    self.y = cords[3]
                    if i.getType() == "lava": lvls.setLive(False)   #kills player if touching lava
                    if i.getType() == "slime": self.setBounce(True) #allows player method 'bounce' to function if touching slime block
                    else: self.setBounce(False)
                    self.y_momentum = self.bounce("y")


    def xCollosion(self):
        for i in lvls.getlvl(): #goes through every block in the current level
            cords = i.getCoor()     #[left,top,right,bottom]
            if self.y+self.h>cords[1]and self.y<cords[3]:   #checks if player is within the y-range to touch the block
                if cords[0]+self.checkDepth > self.x+self.w > cords[0] and self.x_momentum > 0: #checks if player is touching left side of the block
                    self.x = cords[0]-self.w
                    self.movingX = "N"
                    if i.getType() == "lava": lvls.setLive(False)   #kills player if touching lava
                    if i.getType() == "slime": self.setBounce(True) #allows player method 'bounce' to function if touching slime block
                    else: self.setBounce(False)
                    self.x_momentum = self.bounce("x")
                elif cords[2]-self.checkDepth < self.x < cords[2] and self.x_momentum < 0: #checks if player is touching right side of block
                    self.x = cords[2]   #allows player method 'bounce' to function if touching slime block
                    self.movingX = "N"
                    if i.getType() == "lava": lvls.setLive(False)   #kills player if touching lava
                    if i.getType() == "slime": self.setBounce(True) #allows player method 'bounce' to function if touching slime block
                    else: self.setBounce(False)
                    self.x_momentum = self.bounce("x")

def sortByY(val):       #is used to sort the blocks in current level by their y value so collisions will work correctly
    return val.getCoor()[1]

def gameloop(p):    #p = level number
    lvls.setLvl(p)
    inlvl = True
    pygame.draw.rect(display, (0, 0, 0), (0, 0, window_y, window_x))    #0.5 second black screen btwn lvls
    pygame.display.update()
    sleep(.5)
    while inlvl:
        p1.setCor(lvls.respawnCoor[0],lvls.respawnCoor[1])
        lvls.setLive(True)
        for i in lvls.getlvl():         #checks every block in current lvl
            if i.getType() == "dirt":   #resets falling dirt block
                i.reset()
            elif i.getType() == "lava": #resets rising lava
                i.lavaReset()
        p1.resetMomentum()
        while lvls.getLive():
            p1.setMoving("N")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        p1.cutJump()    #if key is released while accelerating upward from a jump, you will begin falling earlier. tldr:variable jumps
            key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT] and key[pygame.K_LEFT]:p1.setMoving("N") #prevents wierd stuff from happening when L and R are bith held
            elif key[pygame.K_RIGHT]: p1.addXM(1)
            elif key[pygame.K_LEFT]:  p1.addXM(-1)
            if key[pygame.K_UP]: p1.jump()


            pygame.draw.rect(display,(0,0,0),(0,0,window_y,window_x))

            p1.moveY()
            p1.yCollision()
            p1.moveX()
            p1.xCollosion()
            p1.drawP()


            lvls.drawLvl()

            for i in lvls.getlvl():
                if i.getType() == "dirt":
                    i.fall()    #checks if dirt timer should be falling
                    i.yCollision()  #checks if dirt should stop falling
                if not p1.getCoor()[0] == lvls.getRespawn()[0] or not p1.getCoor()[1] == lvls.getRespawn()[1]:
                    if i.getType() == "lava":
                        i.rise()    #lava rises by predetermined amount every frame

            if p1.getCoor()[1]> window_y:   #kills player if they fall below the screen
                lvls.setLive(False)

            if lvls.checkDone():    #if you've touched the level end block, checkdone will return true and the current level will end
                lvls.setLive(False)
                inlvl = False

            pygame.display.update()
            clock.tick(60)
        pygame.draw.rect(display, (0, 0, 0), (0, 0, window_y, window_x))    #0.5 second delay after player death
        pygame.display.update()
        sleep(.5)






#MAIN===================
p1 = Player()
p1.setSize(30,30)
p1.setCor(220,300)
p1.setColor((162, 45, 225)) #purple

lvls = LevelBuilder()

for i in range(len(lvls.lvlList)):
    gameloop(i)
