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

# TODO: Add white light
# TODO: Replace yellow light with red light
##### LIGHTS #####
lights = {
  'blue': arduino.get_pin('d:24:o'),
  'yellow': arduino.get_pin('d:11:o'),
  'green': arduino.get_pin('d:3:o'),
  'one': arduino.get_pin('d:23:o'),
  'two': arduino.get_pin('d:22:o'),
  'three': arduino.get_pin('d:2:o'),
}

##### BUTTONS #####
from shared.buttons import button, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_CENTER_ONE_THIRD, BUTTON_CENTER_TWO_THIRD, BUTTON_CENTER_VERTICAL
buttons = {
  'blue': arduino.get_pin('d:4:i'),
  'yellow': arduino.get_pin('d:12:i'),
  'start': arduino.get_pin('d:6:i'),
  'restart': arduino.get_pin('d:5:i'),
  'left': arduino.get_pin('d:10:i'),
  'right': arduino.get_pin('d:9:i'),
  'up': arduino.get_pin('d:8:i'),
  'down': arduino.get_pin('d:7:i')
}

BUTTON_PRESSED = False
def buttonsPressed(buttonArray):
    if (buttonArray[0] == 'start'):
        btn = buttons['start']
        print('start button is ', btn.read())
    for buttonName in buttonArray:
        try:
            button = buttons[buttonName]
        except:
            return False
        if (button.read() != BUTTON_PRESSED):
            return False
    return True

###### SOUNDS #####
from shared.sounds import soundMissile, soundSuccess, lava, gamePlayMusic

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

        button("Play Again",BUTTON_CENTER_ONE_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_loop)
        button("Quit",BUTTON_CENTER_TWO_THIRD,BUTTON_CENTER_VERTICAL,BUTTON_WIDTH,BUTTON_HEIGHT,RED,BRIGHT_RED,quitgame)

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
        TextSurf, TextRect = text_objects("Ngini", largeText)
        TextRect.center = ((DISPLAY_WIDTH * 0.5),(DISPLAY_HEIGHT * 0.3))
        gameDisplay.blit(TextSurf, TextRect)

        button("Play",BUTTON_CENTER_ONE_THIRD,DISPLAY_HEIGHT * 0.6,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,game_loop)
        button("Quit",BUTTON_CENTER_TWO_THIRD,DISPLAY_HEIGHT * 0.6,BUTTON_WIDTH,BUTTON_HEIGHT,RED,BRIGHT_RED,quitgame)

        light(lights['one'], ON)
        light(lights['two'], ON)
        light(lights['three'], ON)
        
        pygame.display.update()
        clock.tick(15)

def game_loop():
    global pause
    # Start the game play music
    #green.write(1)
    light(lights['green'], ON)
    light(lights['two'], OFF)
    light(lights['three'], OFF)
    light(lights['blue'], ON)

    gameDisplay.blit(lavaBackground, (0,0))
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
                if event.key == pygame.K_g:
                    quitgame()

        # Button box logic
        if buttonsPressed(['blue']):
            fail()

        if buttonsPressed(['yellow']):
            fail()
            
        if (buttonsPressed(['right'])):
            light(lights['blue'], OFF)
            light(lights['yellow'], ON)


        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()