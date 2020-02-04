import pygame
import random
import os
import logging
import time
from pyfirmata import Arduino, util

pygame.init()
 
##### BUTTON BOX CONFIGURATION ######
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
    print("No arduino board is detected\n")

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


ON = 1
OFF = 0
def light(light, state):
    light.write(state)

###### DISPLAY #####
display_width = 800
display_height = 600
white = (255,255,255)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Button Box Test')
clock = pygame.time.Clock() 

##### LIGHT ASSIGNMENTS #####
lights = {
  'button1': arduino.get_pin('d:11:p'),
  'button2': arduino.get_pin('d:10:p'),
  'led1': arduino.get_pin('d:3:p'),
  'led2': arduino.get_pin('d:2:p'),
  'led3': arduino.get_pin('d:5:p'),
  'led4': arduino.get_pin('d:4:p'),
  'led5': arduino.get_pin('d:13:p'), }

def quitgame():
    pygame.quit()
    quit()

    
def testLoop():
 
    gameExit = False
 
    while not gameExit:
        
        gameDisplay.fill(white)        
        largeText = pygame.font.SysFont("comicsansms",250)            
          
        # Keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    TextSurf, TextRect = text_objects("Keyboard Button b", largeText)
                    TextRect.center = ((display_width/2),(display_height/2))
                    gameDisplay.blit(TextSurf, TextRect)



        # Button Box
        if buttonsPressed(['back']):
                pygame.quit()
                quit()

        if buttonsPressed(['button1']):
            TextSurf, TextRect = text_objects("Button 1", largeText)
            TextRect.center = ((display_width/2),(display_height/2))
            gameDisplay.blit(TextSurf, TextRect)


        if buttonsPressed(['button2']):
            TextSurf, TextRect = text_objects("Button 2", largeText)
            TextRect.center = ((display_width/2),(display_height/2))
            gameDisplay.blit(TextSurf, TextRect)


        pygame.display.update()
        clock.tick(60)

testLoop()
pygame.quit()
quit()

