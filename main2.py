import pygame
import time
import random
from moviepy.editor import VideoFileClip
 
pygame.init()

###### SOUNDS #####
soundMissile = pygame.mixer.Sound("/Users/bellj23/Documents/code/game-zulu/Sounds/missile.wav")
soundSuccess = pygame.mixer.Sound("/Users/bellj23/Documents/code/game-zulu/Sounds/success.wav")
introMusic = "/Users/bellj23/Documents/code/game-zulu/Sounds/intro_music.wav"
gamePlayMusic = '/Users/bellj23/Documents/code/game-zulu/Sounds/spooky_gameplay.wav'

###### IMAGES #####
stars = pygame.image.load('/Users/bellj23/Documents/code/game-zulu/Images/Stars.png')
spaceShip = pygame.image.load('/Users/bellj23/Documents/code/game-zulu/Images/inside_space_ship.jpg')




 
##### COLOR DEFINITIONS #####
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

car_width = 73
 
##### SET UP DISPLAY ##### 
# display_width = 800
# display_height = 600
#gameDisplay = pygame.display.set_mode((display_width,display_height))
gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screenSize = gameDisplay.get_size()
display_width = screenSize[0]
display_height = screenSize[1]

pygame.display.set_caption('Game Zulu')
clock = pygame.time.Clock()
 
carImg = pygame.image.load('/Users/bellj23/Documents/code/game-zulu/racecar2.png')
gameIcon = pygame.image.load('/Users/bellj23/Documents/code/game-zulu/racecar2.png')

pygame.display.set_icon(gameIcon)

pause = False
#fail = True

def car(x,y):
    gameDisplay.blit(carImg,(x,y))
 
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()
 
def success():
    # This is run when you win the game
    ####################################
    soundSuccess.play()
    pygame.mixer.music.stop()
    ####################################
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("You Won", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        button("Play Again",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15) 


def fail():
    # This is run when you fail
    soundMissile.play()
    pygame.mixer.music.stop()
    ####################################
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("You Blew Up", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        button("Play Again",display_width*(1/2),display_height/2,100,50,green,bright_green,game_loop)
        button("Quit",display_width*(1/8),display_height/2,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15) 

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    

def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False
    
    
def paused():
    ############
    pygame.mixer.music.pause()
    #############
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",1000,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)   


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        gameDisplay.blit(stars, (display_width * 0.5,display_height * 0.5))
        largeText = pygame.font.SysFont("comicsansms",250)
        TextSurf, TextRect = text_objects("Zulu", largeText)
        TextRect.center = ((display_width * 0.5),(display_height * 0.3))
        gameDisplay.blit(TextSurf, TextRect)

        button("Play Again",display_width * 0.30,display_height * 0.6,300,150,green,bright_green,game_loop)
        button("Quit",display_width * 0.60,display_height * 0.6,300,150,red,bright_red,quitgame)
        
        pygame.display.update()
        clock.tick(15)
    
def game_loop():
    global pause
    ############
    pygame.mixer.music.load(gamePlayMusic)
    pygame.mixer.music.play(-1)
    ############
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    
    # This stops the code until movie is finished. May need to use gif type function.
    # clip = VideoFileClip(r'C:\Users\bellj23\Documents\code\game-zulu\Video\Stars-Space-Effect-Background-HD-1.mp4') # "r" denote raw string
    # clip.preview()
    # pygame.quit()

    x_change = 0 
    dodged = 0 
    # TODO: Play clock at dodged = 0...
    gameExit = False
 
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_h:
                    fail()    
                if event.key == pygame.K_g:
                    success()                                  
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
 
        x += x_change
        gameDisplay.fill(white)
 
        car(x,y)
         
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()