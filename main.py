import pygame, pytext
import time, sys, subprocess
import random

white = (255,255,255)
black = (0, 0, 0)
pytext.FONT_NAME_TEMPLATE = "assets/fonts/%s.ttf"

clock = pygame.time.Clock()

screenSize = (496, 496)
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Dying Light")
screen.fill(white)

pygame.mixer.init()
pygame.mixer.music.load("assets/bgmusic.mp3")
pygame.mixer.music.play(-1)

image_library = {}
def get_image(path):
        global image_library
        image = image_library.get(path)
        if image == None:
                actual_path = "assets/" + path + ".png"
                image = pygame.image.load(actual_path)
                image_library[path] = image
        return image

def scaleimage(image, percent):
    newx = image.get_width() * (percent / 100 + 1)
    newy = image.get_height() * (percent / 100 + 1)
    return pygame.transform.scale(image, (newx, newy))

titlescreen = True
pygame.display.set_icon(get_image("icon"))

global yoffset
yoffset = 0

global enemyrow
forkrow = 0
global battlenumber
battlenumber = 0

global frame
frame = 0
global framepart
framepart = 0

titleobj = [pygame.Rect(150, 200, 200, 100), pygame.Rect(150, 300, 200, 100), pygame.Rect(150, 400, 200, 100)]

def drawenemy():
    screen.blit(get_image("enemy"),(240, enemyrow * 16 + yoffset))

def drawwalls():
    i = 0
    for y in range(32):
        for x in range(31):
            if yoffset == 16:
                screen.blit(get_image("waterblock"),(x * 16, (y - 1) * 16 + yoffset + 1))
                i += 1
            else:
                screen.blit(get_image("waterblock"),(x * 16, (y - 1) * 16 + yoffset))
                i += 1

listofpos = [32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18,
             17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

def drawfloor():
    for y in listofpos:
        if yoffset == 16:
            screen.blit(get_image("floorblock"), (240, (abs(y)) * 16 + yoffset + 1))
        else:
            screen.blit(get_image("floorblock"), (240, (abs(y)) * 16 + yoffset))

def drawplayer():
    global frame
    global framepart
    screen.blit(get_image("player" + str(frame)), (240, 240))
    framepart = framepart + 1
    if framepart == 10:
        framepart = 0
        frame = frame + 1
    if frame == 7:
        frame = 0

global level
level = 0

def drawlayer():
    screen.blit(get_image("light" + str(level)), (0, 0))

def battle():
    battling = True
    badtext = False
    etext = False
    greattext = False
    goodtext = False
    OKtext = False
    NSGtext = False
    readytimer = 0
    ready = False
    hit = False
    enemyhealth = battlenumber * 30 + 10
    turns = battlenumber * 3 + 2
    while battling:
        screen.fill(white)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                titlescreen = False
                playing = False
                battling = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and ready:
                    if readytimer <= 12:
                        ready = False
                        hit = True
                        etext = True
                        texttimer = 0
                    elif readytimer <= 14 and readytimer > 12:
                        ready = False
                        hit = True
                        greattext = True
                        texttimer = 0
                    elif readytimer <= 17 and readytimer > 14:
                        ready = False
                        hit = True
                        goodtext = True
                        texttimer = 0
                    elif readytimer <= 20 and readytimer > 17:
                        ready = False
                        hit = True
                        OKtext = True
                        texttimer = 0
                    elif readytimer <= 30 and readytimer > 20:
                        ready = False
                        hit = True
                        NSGtext = True
                        texttimer = 0
                    enemyhealth = enemyhealth - abs(readytimer - 30)
                    turns = turns - 1
        
        pygame.key.set_repeat(0, 1000 / 30)
        
        screen.blit(get_image("battleground"), (0, 0))
        screen.blit(scaleimage(get_image("player0"), 300), (400, 160))
        screen.blit(scaleimage(get_image("enemy"), 500), (25, 160))

        if random.randint(1, 75) == 50:
            ready = True

        if ready and readytimer < 30:
            screen.blit(get_image("space"), (100, 50))
            readytimer = readytimer + 1

        if readytimer == 30:
            ready = False
            readytimer = 0
            if not hit:
                badtext = True
                texttimer = 0
                turns = turns - 1

        if badtext and texttimer <= 30:
            pytext.draw("Bad", (235, 350), color="black", fontsize=48)
            texttimer = texttimer + 1
        if etext and texttimer <= 30:
            pytext.draw("Excellent!", (225, 350), color="black", fontsize=48)
            texttimer = texttimer + 1
        if greattext and texttimer <= 30:
            pytext.draw("Great!", (230, 350), color="black", fontsize=48)
            texttimer = texttimer + 1
        if goodtext and texttimer <= 30:
            pytext.draw("Good!", (235, 350), color="black", fontsize=48)
            texttimer = texttimer + 1
        if OKtext and texttimer <= 30:
            pytext.draw("OK", (240, 350), color="black", fontsize=48)
            texttimer = texttimer + 1
        if NSGtext and texttimer <= 30:
            pytext.draw("Not So Good", (224, 350), color="black", fontsize=48)
            texttimer = texttimer + 1

        if hit and not ready:
            hit = False

        if enemyhealth <= 0:
            battling = False

        print turns

        if turns == 0:
            battling = False
            pygame.quit()
        
        pygame.display.flip()
        clock.tick(30)

def game():
    playing = True
    battlingsoon = False
    global enemyrow
    enemyrow = 0
    global battlenumber
    battlenumber = 0
    while playing:
        screen.fill(white)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                titlescreen = False
                playing = False
        
        global yoffset
        yoffset = yoffset + 1
        if yoffset == 16:
            yoffset = 0
            if battlingsoon:
                enemyrow = enemyrow + 1

        drawwalls()
        drawfloor()

        randencounter = random.randint(1, 150)
        if randencounter == 150 and not battlingsoon:
            drawenemy()
            battlingsoon = True

        if battlingsoon:
            drawenemy()

        if enemyrow == 15:
            battle()
            battlenumber = battlenumber + 1
            enemyrow = 0

        drawplayer()
        drawlayer()

        pygame.display.flip()
        clock.tick(30)


def options():
    inoptions = True
    while inoptions:
        screen.fill(white)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                titlescreen = False
                inoptions = False

        screen.blit(get_image("optionsmenu"), (0, 0))

        pygame.display.flip()
        clock.tick(30)

while titlescreen:
    screen.fill(white)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                titlescreen = False
            
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()
                
                whatwasclickedlist = [obj for obj in titleobj if obj.collidepoint(mousepos)]
                whatwasclicked = whatwasclickedlist[0]
                
                if whatwasclicked == titleobj[0]:
                    game()
                if whatwasclicked == titleobj[1]:
                    options()
                if whatwasclicked == titleobj[2]:
                    titlescreen = False
              
    screen.blit(get_image("screenshot"), (0, 0))
    screen.blit(get_image("Title"), (0, 0))
    screen.blit(get_image("play"), (150, 200))
    screen.blit(get_image("options"), (150, 300))
    screen.blit(get_image("quit"), (150, 400))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
