#Game Details:
# lights1,2,3,4,5 will sequence when won
# Must push button1,2,3 in the correct sequence
# lights1,2,3,4,5 will come on consequitively when correct sequence is pushed.

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
def buttonsPressed(buttonArray):
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
def light(light, state):
    if (light == 'ALL'):
        for lightName in lights:
            lightName.write(state)
    else:
        light.write(state)
 
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

    #### BUTTON BOX ####
    # HELP: How to make light function so we can do 'light(lights['ALL'], ON)
    light(lights['button1'], ON)
    light(lights['button2'], ON)
    light(lights['led1'], ON)
    light(lights['led2'], ON)
    light(lights['led3'], ON)
    light(lights['led4'], ON)
    light(lights['led5'], ON)
    time.sleep(0.3)
    light(lights['button1'], OFF)
    light(lights['button2'], OFF)
    light(lights['led1'], OFF)
    light(lights['led2'], OFF)
    light(lights['led3'], OFF)
    light(lights['led4'], OFF)
    light(lights['led5'], OFF)
    time.sleep(0.3)
    light(lights['button1'], ON)
    light(lights['button2'], ON)
    light(lights['led1'], ON)
    light(lights['led2'], ON)
    light(lights['led3'], ON)
    light(lights['led4'], ON)
    light(lights['led5'], ON)
    time.sleep(0.3)
    light(lights['button1'], OFF)
    light(lights['button2'], OFF)
    light(lights['led1'], OFF)
    light(lights['led2'], OFF)
    light(lights['led3'], OFF)
    light(lights['led4'], OFF)
    light(lights['led5'], OFF)
    time.sleep(0.3)    
    light(lights['button1'], ON)
    light(lights['button2'], ON)
    light(lights['led1'], ON)
    light(lights['led2'], ON)
    light(lights['led3'], ON)
    light(lights['led4'], ON)
    light(lights['led5'], ON)
    time.sleep(0.3)
    light(lights['button1'], OFF)
    light(lights['button2'], OFF)
    light(lights['led1'], OFF)
    light(lights['led2'], OFF)
    light(lights['led3'], OFF)
    light(lights['led4'], OFF)
    light(lights['led5'], OFF)

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

            #### BUTTON BOX #####
    #### HELP: How to get this for loop working
    # for counter in range(0,10):
    #     light(lights['led5'], ON)
    #     light(lights['led1'], OFF)
    #     time.sleep(1)
    #     light(lights['led1'], OFF)
    #     light(lights['led5'], ON)        
    #     time.sleep(1)
    
    # light(lights['led1'], OFF)
    # light(lights['led5'], ON)  
    # time.sleep(0.3)
    # light(lights['led1'], ON)
    # light(lights['led5'], OFF)        
    # time.sleep(0.3)
    # light(lights['led1'], OFF)
    # light(lights['led5'], ON)  
    # time.sleep(0.3)
    # light(lights['led1'], ON)
    # light(lights['led5'], OFF)        
    # time.sleep(0.3)

    light(lights['button1'], OFF)
    light(lights['button2'], OFF)
    light(lights['led1'], OFF)
    light(lights['led2'], OFF)
    light(lights['led3'], OFF)
    light(lights['led4'], OFF)
    light(lights['led5'], OFF)

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
            # Quit game from window screen
            if event.type == pygame.QUIT:
                quitgame()

            # Quit game from keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quitgame()
        
        # Start intro music
        while not startMusicPlay:
            pygame.mixer.music.load(introMusicSpace)
            pygame.mixer.music.play(-1)  
            startMusicPlay = True

        # Background and title
        gameDisplay.blit(stars, (0,0))
        largeText = pygame.font.SysFont("comicsansms",250)
        TextSurf, TextRect = text_objects("Zulu", largeText)
        TextRect.center = ((DISPLAY_WIDTH * 0.5),(DISPLAY_HEIGHT * 0.3))
        gameDisplay.blit(TextSurf, TextRect)

        button("Enter",BUTTON_CENTER_HORIZONTAL,DISPLAY_HEIGHT * 0.6,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_loop)
        
        pygame.display.update()
        clock.tick(15)
        

   
def gate_1():
    # Possible number of trys. Decrease this nuymber to increase difficulty.
    MAX_TRYS = 3

    # Number of steps in the sequence that the player must follow. Add numbers to increase difficulty.
    correctSteps = [1,1,1]
    for i in range(3):
        correctSteps[i] = random.choice(buttonsPressed(['button1']), buttonsPressed(['button2']), buttonsPressed(['center']))

    # Initialize the guess list
    guesses = [0,0,0]

    # Lights to illuminate players progress
    lights = [light(led1,ON), light(led2,ON), light(led3,ON)]

    # What step of the sequence is the player currently on? Initialize with 0 for first number in list.
    currentStep = 0

    # Players attempts. Initialize as 1st attempt.
    attempts = 1

    # Leave game loop when players beat the game or maximum # of trys are reached.
    while currentStep < len(correctSteps) and attempts <= MAX_TRYS:
        # User enters their guess and it stores in the list as a number 
        if any button pushed:
            guesses[currentStep] = ButtonPressed()     

        # If the number equals the correct step, then add a light
        if(correctSteps[currentStep] == guesses[currentStep]):
            lights[currentStep]         
            currentStep += 1
        
        # If the number does not equal correct step, then turn off all lights
        else:
            currentStep = 0
            attempts += 1
            light(ALL,OFF)
            print('Incorrect input. Back to the beginning!')         
    
        # Check whether the puzzle has been solved
        if guesses == correctSteps:
            success()
        else:
            fail()
        


    pygame.display.update()
    clock.tick(60)

def gate_2():

    pass
    # Do something here.

    pygame.display.update()
    clock.tick(60)

def gate_3():

    pass
    # Do something here.
    
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
