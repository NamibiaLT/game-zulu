import pygame
import random
import os
import logging
import time

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

##### COLORS #####
from shared.color import BLACK, WHITE, RED, GREEN, BRIGHT_RED, BRIGHT_GREEN

##### TEXT #####
from shared.text import text_objects

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
from shared.sounds import soundMissile, soundSuccess, lava, gamePlayMusic, soundTrumpet, introMusicSpace

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
                quitgame()
            if event.type == pygame.QUIT:
                quitgame()

        button("Enter",BUTTON_CENTER_ONE_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_loop)
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

            # Quit game from keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.q_g:
                    quitgame()

        button("Enter",BUTTON_CENTER_ONE_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_loop)
        button("Exit",BUTTON_CENTER_TWO_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,RED,BRIGHT_RED,quitgame)

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
                if event.key == pygame.q_g:
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
    
    while not gate1Success:
        light(lights['button1'], ON)
        
        if buttonsPressed(['back']):
            pygame.quit()
            quit()

        if buttonsPressed(['button1']):
            gate1Success = True

        if buttonsPressed(['button2']):
            fail()

        
        pygame.display.update()
        clock.tick(60)
        
def gate_2():
    # temporarily success gate....
    light(lights['button1'], ON)
    light(lights['button2'], ON)
    light(lights['led1'], ON)
    light(lights['led2'], ON)
    light(lights['led3'], ON)
    light(lights['led4'], ON)
    light(lights['led5'], ON)
    time.sleep(1)
    light(lights['button1'], OFF)
    light(lights['button2'], OFF)
    light(lights['led1'], OFF)
    light(lights['led2'], OFF)
    light(lights['led3'], OFF)
    light(lights['led4'], OFF)
    light(lights['led5'], OFF)
    time.sleep(1)
    light(lights['button1'], ON)
    light(lights['button2'], ON)
    light(lights['led1'], ON)
    light(lights['led2'], ON)
    light(lights['led3'], ON)
    light(lights['led4'], ON)
    light(lights['led5'], ON)
    time.sleep(1)
    light(lights['button1'], OFF)
    light(lights['button2'], OFF)
    light(lights['led1'], OFF)
    light(lights['led2'], OFF)
    light(lights['led3'], OFF)
    light(lights['led4'], OFF)
    light(lights['led5'], OFF)
    time.sleep(3)
    success()

def game_loop():
    global pause
    # Start the game play music
    pygame.mixer.music.stop()
    pygame.mixer.music.load(gamePlayMusic)
    pygame.mixer.music.play(-1)

    # background display
    gameDisplay.blit(spaceShip, (0,0))    
    pygame.display.update()

    gameExit = False
    gate1Success = False
    gate2Success = False

    while not gameExit:
        
        # Ability to quit from screen or keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.q_g:
                    pygame.quit()
                    quit()

        # Button box logic
        
        gate_1()

        gate_2()
        
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()