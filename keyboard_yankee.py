import pygame
import os

# Game Zulu
# This game is the first game of the series.  
# Game Play: A button will light up. The player must hit a coorosponding button. Other buttons will trigger a fail condition. 

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

##### DISPLAY ##### 
# from shared.display import gameDisplay, DISPLAY_WIDTH, DISPLAY_HEIGHT, fullScreenImage
# pygame.display.set_caption('Game Yankee')

###### IMAGES #####

##### ARDUINO #####
from shared.arduino_setup import getArduino
arduino = getArduino()

##### LIGHT ASSIGNMENTS #####
lights = {
  'button1': arduino.get_pin('d:11:p'),
  'button2': arduino.get_pin('d:10:p'),
  'led1': arduino.get_pin('d:3:p'),
  'led2': arduino.get_pin('d:2:p'),
  'led3': arduino.get_pin('d:5:p'),
  'led4': arduino.get_pin('d:4:p'),
  'led5': arduino.get_pin('d:13:p')
}

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
            print(button)
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
            i += 1
    else:
        for lightName in lightArray:
            lights[lightName].write(state)

def quitgame():
    pygame.quit()
    quit()

def game_intro():
    print(buttonsPressed(['button1'], 'any'))

game_intro()
pygame.quit()
quit()