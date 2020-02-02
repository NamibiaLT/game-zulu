import pygame
import random
import os
import logging
import time


# This game is the first game of the series.  
#
# Game Play: A button will light up. The player must hit that button. Other buttons will be dead and indicate so with a sound. 
# 

pygame.init()
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
from shared.sounds import soundMissile, soundSuccess, gamePlayMusic, soundTrumpet, introMusicSpace, soundButtonPushDeadd, soundButtonPush11, soundbuttonPush2, soundGateSuccess

##### LIGHTS #####
lights = {
  'button1': arduino.get_pin('d:11:p'),
  'button2': arduino.get_pin('d:10:p'),
  'led1': arduino.get_pin('d:3:p'),
  'led2': arduino.get_pin('d:2:p'),
  'led3': arduino.get_pin('d:5:p'),
  'led4': arduino.get_pin('d:4:p'),
  'led5': arduino.get_pin('d:13:p'), 
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
        # 'handle': arduino.get_pin('d:XXXXXX:i') ADD TO button array
##### SENSORS #####
#motionSense = ardiuno.get_pin('d:8:i')


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
def light(light, state):
    light.write(state)
 
def success():
    #### SOUNDS ####
    pygame.mixer.music.stop()    
    soundSuccess.play()
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
                if event.key == pygame.q_g:
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
    light(lights['button1'], ON)
    
    if buttonsPressed(['back']):
        quitgame()

    #HELP: How to I make this if statement change gate0Success and gate1Success states and not require to put gate_2() funtion?
    if buttonsPressed(['button1']):      
        global gateSuccess

        gateSuccess = [False,True,False]

        soundButtonPushDead.play()
        light(lights['button1'], OFF)
        time.sleep(0.3)       
        gate_2()

    if buttonsPressed(['button2']):
        fail()
    
    # TODO: Change all these to button dead sound
    # HELP: How to make an if statement like if buttonsPressed(['center',up,down....]). So we only need to write one time.

    if buttonsPressed(['down']) or buttonsPressed(['up']) or buttonsPressed(['left']) or buttonsPressed(['right']) or buttonsPressed(['center']):
        soundButtonPushDead.set_volume(1)
        soundButtonPushDead.play()
        time.sleep(2)

    pygame.display.update()
    clock.tick(60)
   
def gate_2():

    light(lights['button2'], ON)
    
    if buttonsPressed(['back']):
        pygame.quit()
        quit()

    #HELP: How to I make this if statement change gate0Success and gate1Success states and not require to put gate_2() funtion?
    if buttonsPressed(['button2']):      
        global gateSuccess
        gateSuccess = [False, False, True]
        soundTrumpet.play()
        light(lights['button2'], OFF)    
        time.sleep(0.3)     
        gate_3()

    if buttonsPressed(['button1']):
        fail()
    
    # TODO: Change all these to button dead sound
    # HELP: How to make an if statement like if buttonsPressed(['center',up,down....]). So we only need to write one time.
    if buttonsPressed(['down']) or buttonsPressed(['up']) or buttonsPressed(['left']) or buttonsPressed(['right']) or buttonsPressed(['center']):
        soundButtonPushDead.set_volume(1)
        soundButtonPushDead.play()

    pygame.display.update()
    clock.tick(60)

def gate_3():
    light(lights['led3'], ON)
    
    if buttonsPressed(['back']):
        pygame.quit()
        quit()

    #HELP: How to I make this if statement change gate0Success and gate1Success states and not require to put gate_2() funtion?
    if buttonsPressed(['center']):      
        global gateSuccess
        gateSuccess = [False, False, False]
        soundTrumpet.play()
        light(lights['led3'], OFF)  
        time.sleep(0.3)       
        success()

    if buttonsPressed(['button1']) or buttonsPressed(['button2']):
        fail()
    
    # TODO: Change all these to button dead sound
    # HELP: How to make an if statement like if buttonsPressed(['center',up,down....]). So we only need to write one time.

    if buttonsPressed(['down']) or buttonsPressed(['up']) or buttonsPressed(['left']) or buttonsPressed(['right']):
        soundButtonPushDead.set_volume(1)
        soundButtonPushDead.play()

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