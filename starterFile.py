import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H = 800, 447
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('images','bg.png')).convert()
bgX = 0 #keeps track of x position of the 2 bckgrnd imgs
bgX2 = bg.get_width()

clock = pygame.time.Clock() #change fps as char moves (increase speed)

class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8,16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1,8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    fall = pygame.image.load(os.path.join('images', '0.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.falling = False

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y+30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount//18], (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x+4, self.y, self.width-24, self.height-10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80: #if char is lying down
                self.hitbox = (self.x, self.y+3, self.width-8, self.height-35)
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x+4, self.y, self.width-24, self.height-10) 
            win.blit(self.slide[self.slideCount//10], (self.x,self.y)) 
            self.slideCount += 1
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+4, self.y, self.width-24, self.height-13)

        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

class saw(object):
    img = [pygame.image.load(os.path.join('images', 'SAW0.png')), pygame.image.load(os.path.join('images', 'SAW1.png')), pygame.image.load(os.path.join('images', 'SAW2.png')), pygame.image.load(os.path.join('images', 'SAW3.png'))]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 5, self.width - 10, self.height)
        if self.count >= 8:
            self.count = 0
        win.blit(pygame.transform.scale(self.img[self.count//2], (64, 64)), (self.x, self.y)) #integar divison finds even amount that can go into something. this way, every 2 frames, we're drawing 1 frame of the saw so it doesn't move too fast
        self.count += 1
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def collide(self, rect):
        #rect[0] = player x pos, [1] = player y pos, [2] = width, [3] player feet
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]: #2 corresponds width; this checks if x coordinates are within each other, now we check y:
            if rect[1] + rect[3] > self.hitbox[1]: 
                return True
        return False

class spike(saw): 
    img = pygame.image.load(os.path.join('images', 'spike.png'))
    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        win.blit(self.img, (self.x, self.y))
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def collide(self, rect):
        #rect[0] = player x pos, [1] = player y pos, [2] = width, [3] player feet
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]: 
            if rect[1] < self.hitbox[3]:  
                return True
        return False


def redrawWindow():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    runner.draw(win)
    for objectt in objects:
        objectt.draw(win)
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Score: ' + str(score), 1, (255,255,255))
    win.blit(text, (700, 10))
    pygame.display.update()

def updateFile():
    f = open('scores.txt', 'r') #use f to open and save file, r means reading the file
    file = f.readlines() #content of file
    last = int(file[0]) #last score is only line in the file b/c only using that 1 line, 0 corresponds to the first line because this puts it into a list
    if last < int(score):
        f.close() 
        file = open('scores.txt', 'w') 
        file.write(str(score)) 
        file.close()
        return score
    return last 

def endScreen():
    global pause, objects, speed, score 
    pause = 0
    objects = []
    speed = 30

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False #when click, exit loop and continue onto rest of loop
        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        previousScore = largeFont.render('Previous Score: ' + str(updateFile()), 1, (255,255,255))
        win.blit(previousScore, (W/2 - previousScore.get_width()/2, 200)) #align to middle of screen, 200 is height
        newScore = largeFont.render('Score: ' + str(score), 1, (255,255,255))
        win.blit(newScore, (W/2 - newScore.get_width()/2, 320))
        pygame.display.update()

    score = 0
    runner.falling = False

#create instance of player
runner = player(200, 313, 64, 64)

#event to increment speed
pygame.time.set_timer(USEREVENT+1, 500) #in miliseconds, triggers this USEREVENT+1 to be true every half second

#event to happen b/w 3-5 seconds (random) seconds to create new object based on that
pygame.time.set_timer(USEREVENT+2, random.randrange(3000, 5000))

speed = 30
run = True

pause = 0 #use to increment time
fallSpeed = 0
objects = []

while run:
    score = speed//5 - 6 #everytime increment by 5, score goes up by 1 subtract 6 b/c start speed of 30 so start with score at 0
    if pause > 0:
        pause += 1 #change pause once started falling b/c that's the delay for how long to wait until endscreen
        if pause > fallSpeed * 2: #w/e speed is, multiply by 2 to give equivalent of about 2 seconds. Use fallSpeed so it's equal to what the speed was when w so it changes dynamically based on how fast char moving
            endScreen()

    #once player collides, check if pause is 0; if so, char hasn't already collided with an object (b/c pause is set to 0 at beginning) so once that happens, set fallspeed to current speed to store fps then set pause to 1 to prevent from resetting
    for objectt in objects:
        if objectt.collide(runner.hitbox):
            runner.falling = True

            if pause == 0:
                fallSpeed = speed
                pause = 1
            
        #movement        
        objectt.x -= 1.4
        if objectt.x < -objectt.width * -1: #offscreen
            objects.pop(objects.index(objectt))

    #this moves the bckgrnd
    bgX -= 1.4 #moving bckgrnd back every frame
    bgX2 -= 1.4 #moving 2nd img bckgrnd at same speed
    if bgX < bg.get_width() * -1: #1st img bckgrnd starts at (0,0) and starts moving backwards until eventually it gets to the negative width of bckgrnd
        bgX = bg.get_width() #reset so that it's at postive bckgrnd width offscreen to the right side
    if bgX2 < bg.get_width() * -1: #once the 1st leaves screen, this one enters
        bgX2 = bg.get_width()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        #check if the timer event is happening in order to increment speed:
        if event.type == USEREVENT+1:
            speed += 1

        if event.type == USEREVENT+2:
            r = random.randrange(0,2) #randomly select object to generate
            if r == 0:
                objects.append(saw(810, 310, 64, 64))
            else:
                objects.append(spike(810, 0, 48, 320))

    #introduce movement
    keys = pygame.key.get_pressed() 

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]: 
        if not(runner.jumping): 
            runner.jumping = True 

    if keys[pygame.K_DOWN]:
        if not(runner.sliding):
            runner.sliding = True

    clock.tick(speed) #fps

    redrawWindow()


