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

# TODO: Get game icon. Maybe a small spaceship.
###### IMAGES #####
stars = fullScreenImage('images/stars.jpg')
spaceShip = fullScreenImage('images/inside_space_ship.jpg')
spaceShipFail = fullScreenImage('images/inside_space_ship_fail.jpg')
spaceShipSuccess = fullScreenImage('images/inside_space_ship_success.jpg')
gameIcon = pygame.image.load('images/racecar2.png')
pygame.display.set_icon(gameIcon)

from shared.color import BLACK, WHITE, RED, GREEN, BRIGHT_RED, BRIGHT_GREEN
from shared.text import text_objects
from shared.sounds import soundMissile, soundSuccess, gamePlayMusic, soundTrumpet, introMusicSpace, soundButtonPushDead, soundButtonPush1, soundbuttonPush2, soundGateSuccess

##### ARDUINO #####
from shared.arduino_setup import getArduino
arduino = getArduino()

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
#motionSense = ardiuno.get_pin('d:8:i')    # Detects motion as HIGH then waits 3 seconds of no motion to go low. Can adjust time manually. https://www.makerguides.com/hc-sr501-arduino-tutorial/


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


pause = False

# TODO: Make this function better with an array
ON = 1
OFF = 0
def light(light, state):
    light.write(state)
 
def success():
    # Start the success sounds
    pygame.mixer.music.stop()    
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
        pygame.quit()
        quit()

    #HELP: How to I make this if statement change gate0Success and gate1Success states and not require to put gate_2() funtion?
    if buttonsPressed(['button1']):      
        gate0Success = False
        gate1Success = True
        soundGateSuccess.play()
        light(lights['button1'], OFF)       
        gate_2()

    if buttonsPressed(['button2']):
        fail()
    
    # TODO: Change all these to button dead sound
    # HELP: How to make an if statement like if buttonsPressed(['center',up,down....]). So we only need to write one time.
    if buttonsPressed(['center']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()
        
    if buttonsPressed(['up']):
        soundTrumpet.set_volume(0.3)
        soundGateSuccess.play()

    if buttonsPressed(['down']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()

    if buttonsPressed(['left']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()

    if buttonsPressed(['right']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()

    pygame.display.update()
    clock.tick(60)

        
def gate_2():

    light(lights['button2'], ON)
    
    if buttonsPressed(['back']):
        pygame.quit()
        quit()

    #HELP: How to I make this if statement change gate0Success and gate1Success states and not require to put gate_2() funtion?
    if buttonsPressed(['button2']):      
        gate1Success = False
        gate2Success = True
        light(lights['button2'], OFF)       
        gate_3()

    if buttonsPressed(['button1']):
        fail()
    
    # TODO: Change all these to button dead sound
    # HELP: How to make an if statement like if buttonsPressed(['center',up,down....]). So we only need to write one time.
    if buttonsPressed(['center']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()
        
    if buttonsPressed(['up']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()

    if buttonsPressed(['down']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()

    if buttonsPressed(['left']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()

    if buttonsPressed(['right']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()

    pygame.display.update()
    clock.tick(60)

    success()

def gate_3():
    light(lights['led3'], ON)
    
    if buttonsPressed(['back']):
        pygame.quit()
        quit()

    #HELP: How to I make this if statement change gate0Success and gate1Success states and not require to put gate_2() funtion?
    if buttonsPressed(['center']):      
        gate2Success = False
        light(lights['led3'], OFF)       
        success()

    if buttonsPressed(['button1']) or buttonsPressed(['button2']):
        fail()
    
    # TODO: Change all these to button dead sound
    # HELP: How to make an if statement like if buttonsPressed(['center',up,down....]). So we only need to write one time.

    if buttonsPressed(['up']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()

    if buttonsPressed(['down']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()

    if buttonsPressed(['left']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()

    if buttonsPressed(['right']):
        soundTrumpet.set_volume(0.3)
        soundTrumpet.play()

    pygame.display.update()
    clock.tick(60)

    success()    


def game_loop():
    global pause
    global gate0Success
    global gate1Success
    global gate2Success
    # Start the game play music
    pygame.mixer.music.stop()
    pygame.mixer.music.load(gamePlayMusic)
    pygame.mixer.music.play(-1)

    # Background display
    gameDisplay.blit(spaceShip, (0,0))    
    pygame.display.update()

    gameExit = False
 
    gate0Success = True
    gate1Success = False
    gate2Success = False
  
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
        if gate0Success:
            gate_1()

        if gate1Success:
            gate_2()

        if gate2Success:
            gate_3()
        
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()