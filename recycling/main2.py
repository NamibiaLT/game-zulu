import pygame
import time
import random
import os
import logging
from pyfirmata import Arduino, util

pygame.init()
clock = pygame.time.Clock()

##### DISPLAY ##### 
gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_SIZE = gameDisplay.get_size()   #James work PC is 1920 1080
DISPLAY_WIDTH = SCREEN_SIZE[0]
DISPLAY_HEIGHT = SCREEN_SIZE[1]
pygame.display.set_caption('Game Zulu')

###### IMAGES #####
stars = pygame.transform.scale(pygame.image.load('Images/stars.jpg'), SCREEN_SIZE)
spaceShip = pygame.transform.scale(pygame.image.load('Images/inside_space_ship.jpg'), SCREEN_SIZE)
spaceShipFail = pygame.transform.scale(pygame.image.load('Images/inside_space_ship_fail.jpg'), SCREEN_SIZE)
spaceShipSuccess = pygame.transform.scale(pygame.image.load('Images/inside_space_ship_success.jpg'), SCREEN_SIZE)

# TODO: Get game icon. Maybe a small spaceship.
gameIcon = pygame.image.load('racecar2.png')
pygame.display.set_icon(gameIcon)

##### COLORS #####
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200,0,0)
GREEN = (0,200,0)
BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)

###### SOUNDS #####
soundMissile = pygame.mixer.Sound("Sounds/missile.wav")
soundSuccess = pygame.mixer.Sound("Sounds/success.wav")
# TODO: Add precheck complete sound
# TODO: Add welcome sound
introMusic = "Sounds/intro_music.wav"
gamePlayMusic = 'Sounds/spooky_gameplay.wav'
pause = False

##### BUTTON BOX CONFIGURATION ##########################################################
mega = {
    'digital' : tuple(x for x in range(54)),
    'analog' : tuple(x for x in range(16)),
    'pwm' : tuple(x for x in range(2,14)),
    'use_ports' : True,
    'disabled' : (0, 1, 14, 15) # Rx, Tx, Crystal
}

try:    
    arduino = Arduino('/dev/ttyACM0', mega, 57600)
except NameError:
    arduino = Arduino('/dev/ttyACM1', mega, 57600)
except AttributeError:
    arduino = Arduino('COM7', mega, 57600)   
except:
    print("No Arduino board is detected\n")

iterator = util.Iterator(arduino)   # Game is really slow. Would adding this iterator in another loop be better?
iterator.start()
time.sleep(0.5)   # Needed for arduino to initialize


##### LIGHT CONSTANTS #####
LIGHT_GREEN = arduino.get_pin('d:3:o')
# TODO: Add white light
# TODO: Replace yellow light with red light
LIGHT_BLUE = arduino.get_pin('d:24:o')
LIGHT_YELLOW = arduino.get_pin('d:11:o')
LIGHT_1 = arduino.get_pin('d:23:o')
LIGHT_2 = arduino.get_pin('d:22:o')
LIGHT_3 = arduino.get_pin('d:2:o')
#lightArray = [green, LIGHT_BLUE_PIN, LIGHT_YELLOW_PIN, LIGHT_1_PIN, LIGHT_2_PIN, LIGHT_3_PIN]

# TODO: Make this into a function
# BUTTON_BLUE = arduino.get_pin('d:4:i')
# BUTTON_YELLOW = arduino.get_pin('d:12:i')
# BUTTON_BLACK = arduino.get_pin('d:6:i')
# BUTTON_GREEN = arduino.get_pin('d:5:i')
# BUTTON_LEFT = arduino.get_pin('d:10:i')
# BUTTON_RIGHT = arduino.get_pin('d:9:i')
# BUTTON_UP = arduino.get_pin('d:8:i')
# BUTTON_DOWN = arduino.get_pin('d:7:i')

# Use button name to get button pin
buttonConverter = {
    'blue': arduino.get_pin('d:4:i'),
    'yellow': arduino.get_pin('d:12:i'),
    'start': arduino.get_pin('d:6:i'),
    'restart': arduino.get_pin('d:5:i'),
    'left': arduino.get_pin('d:10:i'),
    'right': arduino.get_pin('d:9:i'),
    'up': arduino.get_pin('d:8:i'),
    'down': arduino.get_pin('d:7:i')
    }

#########################################################################################

# TODO: Make this function better with an array
on = 1
off = 0
def light(light, state):
    light.write(state)

def buttonPressed(button, state):
    pass

BUTTON_PRESSED = False
def buttonsPressed(buttonArray):
    if (buttonArray[0] == 'start'):
        btn = buttonConverter['start']
        print('start button is ', btn.read())
    for buttonName in buttonArray:
        try:
            button = buttonConverter[buttonName]
        except:
            return False
        if (button.read() != BUTTON_PRESSED):
            return False
    return True

def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()
 
def success():
    # Start the success sounds
    soundSuccess.play()
    pygame.mixer.music.stop()
    logging.info("Game Success")
   
    # Display a GREEN spaceship
    gameDisplay.blit(spaceShipSuccess, (0,0))  
    pygame.display.update()     
   
    largeText = pygame.font.SysFont("comicsansms",250)
    TextSurf, TextRect = text_objects("", largeText)
    TextRect.center = ((DISPLAY_WIDTH * 0.5),(DISPLAY_HEIGHT * 0.33))
    gameDisplay.blit(TextSurf, TextRect)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        # Button position, configuration, and action
        BUTTON_WIDTH = DISPLAY_WIDTH * 0.25   # Number is a scaling factor. On 1920 screen this is a 300mm button
        BUTTON_HEIGHT = DISPLAY_HEIGHT * 0.17    # Number is a scaling factor. On 1080 screen this is a 150mm button
        BUTTON_CENTER_ONE_THIRD = (DISPLAY_WIDTH*0.33)-(BUTTON_WIDTH/2)
        BUTTON_CENTER_TWO_THIRD = (DISPLAY_WIDTH*0.66)-(BUTTON_WIDTH/2)
        BUTTON_CENTER_VERTICAL = (DISPLAY_HEIGHT*0.5)-(BUTTON_HEIGHT/2)
        button("Play Again",BUTTON_CENTER_ONE_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_loop)
        button("Quit",BUTTON_CENTER_TWO_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,RED,BRIGHT_RED,quitgame)
 
        pygame.display.update()
        clock.tick(15) 

def fail():
    # Start the fail sounds
    pygame.mixer.music.stop()
    soundMissile.play()
    logging.info("Game Failure")
    
    # Display a RED spaceship
    gameDisplay.blit(spaceShipFail, (0,0))  
    pygame.display.update()  

    largeText = pygame.font.SysFont("comicsansms",250)
    TextSurf, TextRect = text_objects("", largeText)
    TextRect.center = ((DISPLAY_WIDTH * 0.5),(DISPLAY_HEIGHT * 0.33))
    gameDisplay.blit(TextSurf, TextRect)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Button position, configuration, and action
        BUTTON_WIDTH = DISPLAY_WIDTH * 0.25   # Number is a scaling factor. On 1920 screen this is a 300mm button
        BUTTON_HEIGHT = DISPLAY_HEIGHT * 0.17    # Number is a scaling factor. On 1080 screen this is a 150mm button
        BUTTON_CENTER_ONE_THIRD = (DISPLAY_WIDTH*0.33)-(BUTTON_WIDTH/2)
        BUTTON_CENTER_TWO_THIRD = (DISPLAY_WIDTH*0.66)-(BUTTON_WIDTH/2)
        BUTTON_CENTER_VERTICAL = (DISPLAY_HEIGHT*0.5)-(BUTTON_HEIGHT/2)
        button("Play Again",BUTTON_CENTER_ONE_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_loop)
        button("Quit",BUTTON_CENTER_TWO_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,RED,BRIGHT_RED,quitgame)

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
    TextRect.center = ((DISPLAY_WIDTH * 0.5),(DISPLAY_HEIGHT * 0.33))
    gameDisplay.blit(TextSurf, TextRect)
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Button position, configuration, and action
        BUTTON_WIDTH = DISPLAY_WIDTH * 0.25   # Number is a scaling factor. On 1920 screen this is a 300mm button
        BUTTON_HEIGHT = DISPLAY_HEIGHT * 0.17    # Number is a scaling factor. On 1080 screen this is a 150mm button
        BUTTON_CENTER_ONE_THIRD = (DISPLAY_WIDTH*0.33)-(BUTTON_WIDTH/2)
        BUTTON_CENTER_TWO_THIRD = (DISPLAY_WIDTH*0.66)-(BUTTON_WIDTH/2)
        button("Play Again",BUTTON_CENTER_ONE_THIRD,DISPLAY_HEIGHT * 0.6,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_loop)
        button("Quit",BUTTON_CENTER_TWO_THIRD,DISPLAY_HEIGHT * 0.6,BUTTON_WIDTH,BUTTON_HEIGHT,RED,BRIGHT_RED,quitgame)

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
        TextRect.center = ((DISPLAY_WIDTH * 0.5),(DISPLAY_HEIGHT * 0.3))
        gameDisplay.blit(TextSurf, TextRect)

        # Button position, configuration, and action
        BUTTON_WIDTH = DISPLAY_WIDTH * 0.25   # Number is a scaling factor. On 1920 screen this is a 300mm button
        BUTTON_HEIGHT = DISPLAY_HEIGHT * 0.17    # Number is a scaling factor. On 1080 screen this is a 150mm button
        BUTTON_CENTER_ONE_THIRD = (DISPLAY_WIDTH*0.33)-(BUTTON_WIDTH/2)
        BUTTON_CENTER_TWO_THIRD = (DISPLAY_WIDTH*0.66)-(BUTTON_WIDTH/2)
        button("Play",BUTTON_CENTER_ONE_THIRD,DISPLAY_HEIGHT * 0.6,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_loop)
        button("Quit",BUTTON_CENTER_TWO_THIRD,DISPLAY_HEIGHT * 0.6,BUTTON_WIDTH,BUTTON_HEIGHT,RED,BRIGHT_RED,quitgame)
        
        pygame.display.update()
        clock.tick(15)

def game_loop():
    global pause
    # Start the game play music
    #green.write(1)
    light(LIGHT_GREEN, on)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(gamePlayMusic)
    pygame.mixer.music.play(-1)
   
    # Background
    gameDisplay.blit(spaceShip, (0,0))    
    pygame.display.update()

    dodged = clock.tick() 
    # TODO: Play clock at dodged = 0...
    # TODO: Add time limit to game.
    gameExit = False
 
    while not gameExit:
        
        # Keyboard logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_h:
                    fail()    
                if event.key == pygame.K_g:
                    success()                                  

        # Button box logic
        if buttonsPressed(['blue']):
            success()

        if buttonsPressed(['yellow']):
            fail()

        if buttonsPressed(['restart']):
            pause = True
            paused()  

        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()