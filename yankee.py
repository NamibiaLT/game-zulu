import pygame
import random
import os
import logging
import time

# Game Zulu
# This game is the first game of the series.  
# Game Play: A button will light up. The player must hit a coorosponding button. Other buttons will trigger a fail condition. 

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

##### DISPLAY ##### 
from shared.display import gameDisplay, DISPLAY_WIDTH, DISPLAY_HEIGHT, fullScreenImage
pygame.display.set_caption('Game Zulu')

###### IMAGES #####
stars = fullScreenImage('images/stars.jpg')
spaceShip = fullScreenImage('images/inside_space_ship.jpg')
spaceShipFail = fullScreenImage('images/inside_space_ship_fail.jpg')
spaceShipSuccess = fullScreenImage('images/inside_space_ship_success.jpg')
gameIcon = pygame.image.load('images/space_ship_2.png')
pygame.display.set_icon(gameIcon)

##### ARDUINO #####
from shared.arduino_setup import getArduino
arduino = getArduino()

from shared.color import BLACK, WHITE, RED, GREEN, BRIGHT_RED, BRIGHT_GREEN
from shared.text import text_objects
from shared.sounds import soundMissile, soundButtonDead, soundGateSuccess, soundSuccess, gamePlayMusic, soundTrumpet, introMusicSpace, soundButtonPushDead, soundButtonPush1, soundbuttonPush2

##### LIGHT ASSIGNMENTS #####
lights = {
  'button1': arduino.get_pin('d:11:p'),
  'button2': arduino.get_pin('d:10:p'),
  'led1': arduino.get_pin('d:3:p'),
  'led2': arduino.get_pin('d:2:p'),
  'led3': arduino.get_pin('d:5:p'),
  'led4': arduino.get_pin('d:4:p'),
  'led5': arduino.get_pin('d:13:p'), }

# takes in array, returns true if all lights are on
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
from shared.buttons import button, BUTTON_WIDTH, BUTTON_HEIGHT,BUTTON_CENTER_HORIZONTAL, BUTTON_CENTER_ONE_THIRD, BUTTON_CENTER_TWO_THIRD, BUTTON_CENTER_VERTICAL
buttons = {
  'button2': arduino.get_pin('d:36:i'),
  'button1': arduino.get_pin('d:37:i'),
  'center': arduino.get_pin('d:35:i'),  
  'back': arduino.get_pin('d:30:i'),
  'left': arduino.get_pin('d:32:i'),
  'right': arduino.get_pin('d:31:i'),
  'up': arduino.get_pin('d:34:i'),
  'down': arduino.get_pin('d:33:i'),
}

BUTTON_PRESSED = False
def buttonsPressed(buttonArray, buttonType):
    if (buttonType == 'any'):
        for buttonName in buttonArray:
            try:
                button = buttons[buttonName]
            except:
                print('exception')
            if (button.read() != BUTTON_PRESSED):
                return True
        return False
    if (buttonType == 'all'):
        for buttonName in buttonArray:
            try:
                button = buttons[buttonName]
            except:
                return False
            if (button.read() != BUTTON_PRESSED):
                return False
        return True

pause = False
ON = 1
OFF = 0
### HELP: How to write if "ALL, ON" then all lights come on. Help with this function. "ALL does not work."
def light(lightArray, state):
    if (state == 'blink'):
        i = 0
        while i < 3:
            for lightName in lightArray:
                lights[lightName].write(ON)
            time.sleep(1000)
            for lightName in lightArray:
                lights[lightName].write(OFF)
    else:
        for lightName in lightArray:
            lights[lightName].write(state)
 
def success():
    #### SOUNDS ####
    pygame.mixer.music.stop()    
    soundTrumpet.play()
    pygame.mixer.music.stop()
    logging.info("Game Success")
   
    #### DISPLAY ####
    gameDisplay.blit(spaceShipSuccess, (0,0))  
    pygame.display.update()     
   
    largeText = pygame.font.SysFont("comicsansms",250)
    TextSurf, TextRect = text_objects("", largeText)
    TextRect.center = ((DISPLAY_WIDTH * 0.5),(DISPLAY_HEIGHT * 0.33))
    gameDisplay.blit(TextSurf, TextRect)
    
    pygame.display.update()
    clock.tick(15)

    #### START SEQUENCE ####
    light(lights.keys(), 'blink')

    while True:
        for event in pygame.event.get():
            # Quit game from window screen            
            if event.type == pygame.QUIT:
                quitgame()
            # Quit game from keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quitgame()
        # TODO: Make Proceed only available if game was successful.
        button("Proceed",BUTTON_CENTER_ONE_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_intro)
        # TODO: Make Leave go back to main screen with list of games
        button("Leave",BUTTON_CENTER_TWO_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,RED,BRIGHT_RED,game_intro)
 
        pygame.display.update()
        clock.tick(15) 


def fail():
    #### SOUNDS ####
    pygame.mixer.music.stop()
    soundMissile.play()
    logging.info("Game Failure")
    
    #### DISPLAY #####
    gameDisplay.blit(spaceShipFail, (0,0))  
    pygame.display.update()  

    largeText = pygame.font.SysFont("comicsansms",250)
    TextSurf, TextRect = text_objects("", largeText)
    TextRect.center = ((DISPLAY_WIDTH * 0.5),(DISPLAY_HEIGHT * 0.33))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    clock.tick(15)   

    light([lights['led1'], lights['led3']], 'blink')

    light(lights.keys(), OFF)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Quit game from keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quitgame()

        # TODO: Make Enter only available if game was successful. Put LOCK symbol for this fail.
        # TODO: Make dead sound if pushed. Make so nothing happens        
        button("Proceed (LOCKED)",BUTTON_CENTER_ONE_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_intro)
        # TODO: Make Leave go back to main screen with list of games        
        button("Leave",BUTTON_CENTER_TWO_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,RED,BRIGHT_RED,game_intro)

        pygame.display.update()
        clock.tick(15)
  
def quitgame():
    pygame.quit()
    quit()

def game_intro():
    intro = True
    startMusicPlay = False
    while intro:
        # Abilty to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Start intro music
        while not startMusicPlay:
            pygame.mixer.music.load(lava)
            pygame.mixer.music.play(-1)   
            startMusicPlay = True

        # Background and title
        gameDisplay.blit(lavaBackground, (0,0))
        largeText = pygame.font.SysFont("comicsansms",250)
        TextSurf, TextRect = text_objects("Zulu", largeText)
        TextRect.center = ((DISPLAY_WIDTH * 0.5),(DISPLAY_HEIGHT * 0.3))
        gameDisplay.blit(TextSurf, TextRect)

        button("Play",BUTTON_CENTER_ONE_THIRD,DISPLAY_HEIGHT * 0.6,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_loop)
        button("Quit",BUTTON_CENTER_TWO_THIRD,DISPLAY_HEIGHT * 0.6,BUTTON_WIDTH,BUTTON_HEIGHT,RED,BRIGHT_RED,quitgame)

        light(lights.keys(), 'BLINK')
        
        pygame.display.update()
        clock.tick(15)
        
def gate_1():
    if buttonsPressed(['blue'], 'all'):
        if (lightsOn(['blue'])):
            fail()
        else:
            soundTrumpet.play()
            return

    if buttonsPressed(['yellow'], 'all'):
        fail()
        
    if (buttonsPressed(['right'], 'all')):
        light(lights['blue'], OFF)
        light(lights['yellow'], ON)

    if (buttonsPressed(['left'], 'all')):
        light(lights['blue'], ON)
        light(lights['yellow'], OFF)

    if buttonsPressed(['down', 'up', 'left', 'right', 'center'], 'all'):
        soundButtonDead.play()
   
def gate_2():

    light(lights['button2'], ON)
    
    if buttonsPressed(['back'], 'all'):
        pygame.quit()
        quit()

    #HELP: How to I make this if statement change gate0Success and gate1Success states and not require to put gate_2() funtion?
    if buttonsPressed(['button2'], 'all'):
        global gateSuccess
        gateSuccess = [False, False, True]
        soundGateSuccess.play()
        light(lights['button2'], OFF)    
        time.sleep(0.3)     
        gate_3()

    if buttonsPressed(['button1'], 'all'):
        fail()
    
    # TODO: Change all these to button dead sound
    # HELP: How to make an if statement like if buttonsPressed(['center',up,down....]). So we only need to write one time.
    if buttonsPressed(['down', 'up', 'left', 'right', 'center'], 'all'):
        soundButtonDead.play()

    pygame.display.update()
    clock.tick(60)

def gate_3():
    light([lights['led1'], lights['led2']], ON)
    
    if buttonsPressed(['back']):
        pygame.quit()
        quit()

    #HELP: How to I make this if statement change gate0Success and gate1Success states and not require to put gate_2() funtion?
    if buttonsPressed(['up']):      
        global gateSuccess
        gateSuccess = [False, False, False]
        light([lights['led1'], lights['led2']], OFF)
        time.sleep(0.3)       
        success()

    if buttonsPressed(['button1', 'button2', 'down', 'right', 'left', 'center'], 'any'):
        fail()
    
    pygame.display.update()
    clock.tick(60)

def game_loop():

    global pause
    global gateSuccess

    # Start the game play music
    pygame.mixer.music.stop()
    pygame.mixer.music.load(gamePlayMusic)
    pygame.mixer.music.play(-1)

    # Background display
    gameDisplay.blit(spaceShip, (0,0))
    pygame.display.update()

    gameExit = False
 
    gateSuccess = [True, False, False]

    while not gameExit:

        # Ability to quit from screen or keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # Button box logic
        # Make game assign random LED on to determine which one wins the gate.
        if gateSuccess[0]:
            gate_1()

        if gateSuccess[1]:
            gate_2()

        if gateSuccess[2]:
            gate_3()

        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()