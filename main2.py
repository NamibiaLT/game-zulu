import pygame
import time
import random
import os
#from moviepy.editor import VideoFileClip

pygame.init()
clock = pygame.time.Clock()

##### DISPLAY ##### 
gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screenSize = gameDisplay.get_size()   #James work PC is 1920 1080
display_width = screenSize[0]
display_height = screenSize[1]
pygame.display.set_caption('Game Zulu')

###### SOUNDS #####
# soundMissile = pygame.mixer.Sound("Sounds\missile.wav")
# soundSuccess = pygame.mixer.Sound("Sounds\success.wav")
# introMusic = "Sounds\intro_music.wav"
# gamePlayMusic = 'Sounds\spooky_gameplay.wav'

# TODO: Figure out how to play these on windows OR LINUX regardless of slashes...
soundMissile = pygame.mixer.Sound("Sounds/missile.wav")
soundSuccess = pygame.mixer.Sound("Sounds/success.wav")
introMusic = "Sounds/intro_music.wav"
gamePlayMusic = 'Sounds/spooky_gameplay.wav'

###### IMAGES #####
# stars = pygame.transform.scale(pygame.image.load('Images\stars.jpg'), screenSize)
# spaceShip = pygame.transform.scale(pygame.image.load('Images\inside_space_ship.jpg'), screenSize)
# spaceShipFail = pygame.transform.scale(pygame.image.load('Images\inside_space_ship_fail.jpg'), screenSize)
# spaceShipSuccess = pygame.transform.scale(pygame.image.load('Images\inside_space_ship_success.jpg'), screenSize)

stars = pygame.transform.scale(pygame.image.load('Images/stars.jpg'), screenSize)
spaceShip = pygame.transform.scale(pygame.image.load('Images/inside_space_ship.jpg'), screenSize)
spaceShipFail = pygame.transform.scale(pygame.image.load('Images/inside_space_ship_fail.jpg'), screenSize)
spaceShipSuccess = pygame.transform.scale(pygame.image.load('Images/inside_space_ship_success.jpg'), screenSize)


##### COLOR DEFINITIONS #####
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

# TODO: Get game icon. Maybe a small spaceship.
gameIcon = pygame.image.load('racecar2.png')
pygame.display.set_icon(gameIcon)

pause = False

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()
 
def success():
    # Start the success sounds
    soundSuccess.play()
    pygame.mixer.music.stop()
   
    # Display a green spaceship
    gameDisplay.blit(spaceShipSuccess, (0,0))  
    pygame.display.update()     
   
    largeText = pygame.font.SysFont("comicsansms",250)
    TextSurf, TextRect = text_objects("", largeText)
    TextRect.center = ((display_width * 0.5),(display_height * 0.33))
    gameDisplay.blit(TextSurf, TextRect)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        # Button position, configuration, and action
        buttonWidth = display_width * 0.25   # Number is a scaling factor. On 1920 screen this is a 300mm button
        buttonHeight = display_height * 0.17    # Number is a scaling factor. On 1080 screen this is a 150mm button
        buttonCenterOneThird = (display_width*0.33)-(buttonWidth/2)
        buttonCenterTwoThird = (display_width*0.66)-(buttonWidth/2)
        buttonCenterVertical = (display_height*0.5)-(buttonHeight/2)
        button("Play Again",buttonCenterOneThird,buttonCenterVertical,buttonWidth,buttonHeight,green,bright_green,game_loop)
        button("Quit",buttonCenterTwoThird,buttonCenterVertical,buttonWidth,buttonHeight,red,bright_red,quitgame)
 
        pygame.display.update()
        clock.tick(15) 

def fail():
    # Start the fail sounds
    pygame.mixer.music.stop()
    soundMissile.play()
    
    # Display a red spaceship
    gameDisplay.blit(spaceShipFail, (0,0))  
    pygame.display.update()  

    largeText = pygame.font.SysFont("comicsansms",250)
    TextSurf, TextRect = text_objects("", largeText)
    TextRect.center = ((display_width * 0.5),(display_height * 0.33))
    gameDisplay.blit(TextSurf, TextRect)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Button position, configuration, and action
        buttonWidth = display_width * 0.25   # Number is a scaling factor. On 1920 screen this is a 300mm button
        buttonHeight = display_height * 0.17    # Number is a scaling factor. On 1080 screen this is a 150mm button
        buttonCenterOneThird = (display_width*0.33)-(buttonWidth/2)
        buttonCenterTwoThird = (display_width*0.66)-(buttonWidth/2)
        buttonCenterVertical = (display_height*0.5)-(buttonHeight/2)
        button("Play Again",buttonCenterOneThird,buttonCenterVertical,buttonWidth,buttonHeight,green,bright_green,game_loop)
        button("Quit",buttonCenterTwoThird,buttonCenterVertical,buttonWidth,buttonHeight,red,bright_red,quitgame)

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
    largeText = pygame.font.SysFont("comicsansms",250)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width * 0.5),(display_height * 0.33))
    gameDisplay.blit(TextSurf, TextRect)
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Button position, configuration, and action
        buttonWidth = display_width * 0.25   # Number is a scaling factor. On 1920 screen this is a 300mm button
        buttonHeight = display_height * 0.17    # Number is a scaling factor. On 1080 screen this is a 150mm button
        buttonCenterOneThird = (display_width*0.33)-(buttonWidth/2)
        buttonCenterTwoThird = (display_width*0.66)-(buttonWidth/2)
        button("Play Again",buttonCenterOneThird,display_height * 0.6,buttonWidth,buttonHeight,green,bright_green,game_loop)
        button("Quit",buttonCenterTwoThird,display_height * 0.6,buttonWidth,buttonHeight,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)   


def game_intro():
    intro = True
    startMusicPlay = False
    while intro:
        # Abilty to quite the game
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Start into music
        while not startMusicPlay:
            pygame.mixer.music.load(introMusic)
            pygame.mixer.music.play(-1)   
            startMusicPlay = True

        # Background and title
        gameDisplay.blit(stars, (0,0))
        largeText = pygame.font.SysFont("comicsansms",250)
        TextSurf, TextRect = text_objects("Zulu", largeText)
        TextRect.center = ((display_width * 0.5),(display_height * 0.3))
        gameDisplay.blit(TextSurf, TextRect)

        # Button position, configuration, and action
        buttonWidth = display_width * 0.25   # Number is a scaling factor. On 1920 screen this is a 300mm button
        buttonHeight = display_height * 0.17    # Number is a scaling factor. On 1080 screen this is a 150mm button
        buttonCenterOneThird = (display_width*0.33)-(buttonWidth/2)
        buttonCenterTwoThird = (display_width*0.66)-(buttonWidth/2)
        button("Play",buttonCenterOneThird,display_height * 0.6,buttonWidth,buttonHeight,green,bright_green,game_loop)
        button("Quit",buttonCenterTwoThird,display_height * 0.6,buttonWidth,buttonHeight,red,bright_red,quitgame)
        
        pygame.display.update()
        clock.tick(15)


def game_loop():
    global pause
    # Start the game play music
    pygame.mixer.music.stop()
    pygame.mixer.music.load(gamePlayMusic)
    pygame.mixer.music.play(-1)
   
    # Background
    gameDisplay.blit(spaceShip, (0,0))    
    pygame.display.update()

    dodged = clock.tick() 
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
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()