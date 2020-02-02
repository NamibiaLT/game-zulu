import pygame
import random
import os
import logging

pygame.init()
clock = pygame.time.Clock()

##### DISPLAY ##### 
from shared.display import gameDisplay, DISPLAY_WIDTH, DISPLAY_HEIGHT, fullScreenImage
pygame.display.set_caption('Game Zulu')

# TODO: Get game icon. Maybe a small spaceship.
###### IMAGES #####
lavaBackground = fullScreenImage('images/lava.jpg')
spaceShip = fullScreenImage('images/inside_space_ship.jpg')
spaceShipFail = fullScreenImage('images/inside_space_ship_fail.jpg')
spaceShipSuccess = fullScreenImage('images/inside_space_ship_success.jpg')
gameIcon = pygame.image.load('images/racecar2.png')
pygame.display.set_icon(gameIcon)

##### COLORS #####
from shared.color import BLACK, WHITE, RED, GREEN, BRIGHT_RED, BRIGHT_GREEN

##### TEXT #####
from shared.text import text_objects

##### ARDUINO #####
from shared.arduino_setup import getArduino
arduino = getArduino()

##### LIGHTS #####
lights = {
  'blue': arduino.get_pin('d:10:p'),
  'green': arduino.get_pin('d:13:p'),
  'red': arduino.get_pin('d:13:p'), 
  'red': arduino.get_pin('d:3:p'),
  'one': arduino.get_pin('d:2:p'),
  'two': arduino.get_pin('d:5:p'),
  'three': arduino.get_pin('d:4:p'),
}

def lightsOn(lightArray):
    for lightName in lightArray:
        try:
            light = lights[lightName]
        except:
            return False
        if (light.read() != ON):
            return False
    return True

##### BUTTONS #####
from shared.buttons import button, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_CENTER_ONE_THIRD, BUTTON_CENTER_TWO_THIRD, BUTTON_CENTER_VERTICAL
buttons = {
  'blue': arduino.get_pin('d:5:i'),
  'green': arduino.get_pin('d:37:i'),
  'red': arduino.get_pin('d:35:i'),  
  'abort': arduino.get_pin('d:30:i'),   #Back of game. Should be abort button to exit/quit program/game
  'left': arduino.get_pin('d:32:i'),
  'right': arduino.get_pin('d:31:i'),
  'up': arduino.get_pin('d:34:i'),
  'down': arduino.get_pin('d:33:i'),
}
        # 'handle': arduino.get_pin('d:XXXXXX:i') ADD TO button array
##### SENSORS #####
motionSense = ardiuno.get_pin('d:8:i')    # Detects motion as HIGH then waits 3 seconds of no motion to go low. Can adjust time manually. https://www.makerguides.com/hc-sr501-arduino-tutorial/


BUTTON_PRESSED = False
def buttonsPressed(buttonArray):
    for buttonName in buttonArray:
        try:
            button = buttons[buttonName]
        except:
            return False
        if (button.read() != BUTTON_PRESSED):
            return False
    return True

###### SOUNDS #####
from shared.sounds import soundMissile, soundSuccess, lava, gamePlayMusic, soundTrumpet

pause = False

# TODO: Make this function better with an array
ON = 1
OFF = 0
def light(light, state):
    light.write(state)
 
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