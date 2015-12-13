import pygame, pytext
import time, sys, subprocess
import random

white = (255,255,255)
black = (0, 0, 0)
pytext.FONT_NAME_TEMPLATE = "assets/fonts/%s.ttf"

clock = pygame.time.Clock()

screenSize = (496, 496)
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Title TBD")
screen.fill(white)

image_library = {}
def get_image(path):
        global image_library
        image = image_library.get(path)
        if image == None:
                actual_path = "assets/" + path + ".png"
                image = pygame.image.load(actual_path)
                image_library[path] = image
        return image

titlescreen = True

global yoffset
yoffset = 0

global forkrow
forkrow = 0

global frame
frame = 0

titleobj = [pygame.Rect(150, 200, 200, 100), pygame.Rect(150, 300, 200, 100), pygame.Rect(150, 400, 200, 100)]

def drawfork():
    for x in range(31):
        screen.blit(get_image("floorblock"),(x * 16, forkrow * 16 + yoffset))


def drawwalls():
    i = 0
    for y in range(32):
        for x in range(31):
            if yoffset == 16:
                screen.blit(get_image("block"),(x * 16, (y - 1) * 16 + yoffset + 1))
                i += 1
            else:
                screen.blit(get_image("block"),(x * 16, (y - 1) * 16 + yoffset))
                i += 1

def drawfloor():
    for y in range(32 + forkrow):
        if yoffset == 16:
            screen.blit(get_image("floorblock"),(240, (abs(y) - 1) * 16 + yoffset + 1))
        else:
            screen.blit(get_image("floorblock"),(240, (abs(y) - 1) * 16 + yoffset))

def drawplayer():
    global frame
    screen.blit(get_image("player" + str(frame)),(240, 240))
    frame = frame + 1
    if frame == 3:
        frame = 0

def game():
    playing = True
    fork = False
    global forkrow
    forkrow = 0
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
            if fork:
                forkrow = forkrow + 1

        drawwalls()
        drawfloor()

        randfork = random.randint(1, 150)
        if randfork == 150 and not fork:
            print "fork"
            fork = True

        if fork:
            drawfork()

        if forkrow == 33:
            fork = False
            forkrow = 0

        drawplayer()

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
#                    titlescreen = False
                    game()
                if whatwasclicked == titleobj[1]:
#                    titlescreen = False
                    options()
                if whatwasclicked == titleobj[2]:
                    titlescreen = False
              
    screen.blit(get_image("Title"), (0, 0))
    screen.blit(get_image("play"), (150, 200))
    screen.blit(get_image("options"), (150, 300))
    screen.blit(get_image("quit"), (150, 400))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
