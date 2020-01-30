import serial
import pygame
import time
import logging
from pyfirmata import Arduino, util
pygame.mixer.init()

#GENERAL TODO
#Replace all print() with Logging.info("..."). See: https://realpython.com/python-logging/
#TODO: Figure out why game is slow to respond to button pressed at the beginning.
    #Maybe will try inputFirmata firmware on arduino

#SOUNDS
soundIntroMusic = pygame.mixer.Sound("/home/pi/Puzzilist/Sounds/music_zapsplat_among_the_stars_no_piano.wav")
soundPrecheck = pygame.mixer.Sound("/home/pi/Puzzilist/Sounds/zapsplat_science_fiction_computer_voice_says_pre_checks_completed_30835.wav") 
soundDoorOpen = pygame.mixer.Sound("/home/pi/Puzzilist/Sounds/zapsplat_science_fiction_door_open_hiss_air_release_then_auto_motor_drome_44436.wav")
soundWelcome = pygame.mixer.Sound("/home/pi/Puzzilist/Sounds/zapsplat_science_fiction_computer_voice_says_welcome_30843.wav")
soundGamePlay = pygame.mixer.Sound("/home/pi/Puzzilist/Sounds/zapsplat_science_fiction_drone_large_cavernous_metallic_43232.wav")
soundSuccess = pygame.mixer.Sound("/home/pi/Puzzilist/Sounds/zapsplat_science_fiction_computer_voice_male_says_success_15858.wav")
soundIncomingMissile = pygame.mixer.Sound("/home/pi/Puzzilist/Sounds/zapsplat_science_fiction_computer_voice_male_says_warning_incoming_missle_15860.wav")
soundExplosion = pygame.mixer.Sound("/home/pi/Puzzilist/Sounds/zapsplat_warfare_missile_incoming_whizz_by_then_explosion_001_31162.wav")
soundData = pygame.mixer.Sound("/home/pi/Puzzilist/Sounds/zapsplat_science_fiction_data_stream_computer_41940.wav")
#Add other success sound. Add button sounds.-

#DISPLAY
    #Play a gray, slow-moving symbol for pregame screen
    #Play a green, slow-moving symbol for gameplay screen
    #Play a green, static symbol for success screen
    #play a red, slow-moving symbol for fail screen
#screen = pygame.display.set_mode((200,200))
#pygame.display.update()


def buttonPressed(buttonType): #Do I need this function? Would this be better code?
    print('buttonType', buttonType)
    print('buttonType read', buttonType.read())
    if buttonType.read() == False:
        return buttonType
    return False

##
##### MAIN CODE #####
##
def main(arduino):

    buttonPressed(BUTTON_START)
    while True:      #Main Loop. Keep the game on indefinitely.   
        initPregame()      
        #TODO: Refactor arduino/python code to send character strings rather than integer values        
        print(BUTTON_ALL)  
        if BUTTON_START.read() == False: #Start Game
            exitPregame()
            initGamePlay(arduino)

def initPregame():
    #lightPressed = bytes(arduino.write(10))
    #LIGHT_GREEN.write(1)
    print("Initializing Pregame")
    soundIntroMusic.set_volume(0.5)
    soundIntroMusic.play(-1)
    #TODO: Illuminate blinking greenlight.
    #arduino.writeline("greenlight") blink

def exitPregame():
    print("Exiting Pregame")   
    pygame.mixer.stop()     #Stop all music  

def exitGamePlay():
    print("Exiting GamePlay")
    LIGHT_GREEN.write(0)
    pygame.mixer.stop()     #Stop all music
    while BUTTON_RESTART.read() == True:
        LIGHT_1.write(1)   #Should I make a function for light functionality? How will blinking likes effect the threading of the code?
        LIGHT_2.write(1)
        LIGHT_3.write(1)
        LIGHT_BLUE.write(1)
        LIGHT_YELLOW.write(1)
        time.sleep(0.3)
        LIGHT_1.write(0)
        LIGHT_2.write(0)
        LIGHT_3.write(0)
        LIGHT_BLUE.write(0)
        LIGHT_YELLOW.write(0)
        time.sleep(0.3)
        restartGame = True
    return restartGame

def initGamePlay(arduino):
    #TODO: Illuminate greenlight.
    #arduino.writeline("greenlight")
    LIGHT_GREEN.write(1)
    print("Initializing Game Play")    
    restartGame = False
    while restartGame == False:
        #int(arduino.write(11))
        soundGamePlay.set_volume(1)
        soundDoorOpen.play()
        time.sleep(3)
        soundPrecheck.play()     # TODO: Find better way to play sounds consecutively. For loop?
        time.sleep(2)
        soundWelcome.play()
        time.sleep(2)               
        soundGamePlay.play(-1)        
        
        print("Game Play Loop")

        while restartGame == False:     #Put this loop here because the initGamePlay sounds kept cycling            
#            #Sequence 3 LEDS from Right to LEFT...Need help with for loop.
#            LIGHTS_ON[] =[LIGHT_1.write(1),LIGHT_2.write(1),LIGHT_3.write(1)]
#            LIGHTS_OFF[] = [LIGHT_1.write(0),LIGHT_2.write(0),LIGHT_3.write(0)]            
#            for i in range(4):                   
#                LIGHT_ON[i]
#                pass_time(0.5)
#                LIGHT_OFF[i]    
        
            if BUTTON_BLUE.read() == False:
                pygame.mixer.stop()
                soundSuccess.play()
                time.sleep(2)
                print("Game Success")
                restartGame = exitGamePlay()

            if BUTTON_YELLOW.read() == False:
                pygame.mixer.stop()
                pygame.mixer.Channel(0).play(soundIncomingMissile)
                pygame.mixer.Channel(0).queue(soundExplosion)
                time.sleep(5)
                print("Game Failure")
                restartGame = exitGamePlay()

            if BUTTON_RESTART.read() == False:
                print("Restart Button Pressed")
                LIGHT_GREEN.write(0)
                pygame.mixer.stop()                
                restartGame = True

if __name__== "__main__":

    mega = {
        'digital' : tuple(x for x in range(54)),
        'analog' : tuple(x for x in range(16)),
        'pwm' : tuple(x for x in range(2,14)),
        'use_ports' : True,
        'disabled' : (0, 1, 14, 15) # Rx, Tx, Crystal
    }

    try:    
        arduino = Arduino('/dev/ttyACM0', mega, 57600)
    except:
        arduino = Arduino('/dev/ttyACM1', mega, 57600)

    iterator = util.Iterator(arduino)   # Game is really slow. Would adding this iterator in another loop be better?
    iterator.start()

    #BUTTON_CONSTANTS     ....Should this be here or up top. When up top the code did not run.
    BUTTON_BLUE = arduino.get_pin('d:4:i')
    BUTTON_YELLOW = arduino.get_pin('d:12:i')
    BUTTON_START = arduino.get_pin('d:6:i')
    BUTTON_RESTART = arduino.get_pin('d:5:i')
    BUTTON_LEFT = arduino.get_pin('d:10:i')
    BUTTON_RIGHT = arduino.get_pin('d:9:i')
    BUTTON_UP = arduino.get_pin('d:8:i')     # Temp red button until up down gets fixed
    BUTTON_DOWN = arduino.get_pin('d:7:i')#Temp Out of Service
    #TODO: Must add back in "BUTTON_RIGHT.read(), BUTTON_UP.read(),BUTTON_DOWN.read()"
    BUTTON_ALL = [BUTTON_BLUE.read(), BUTTON_YELLOW.read(), BUTTON_START.read(), BUTTON_RESTART.read()]

    ##### LIGHT CONSTANTS #####
    LIGHT_GREEN = arduino.get_pin('d:3:o')     # If pin "Invalid pin definition" it could be due to standard Firmata not recognizing ArduinoMEGA pins.
    LIGHT_BLUE = arduino.get_pin('d:24:o')
    LIGHT_YELLOW= arduino.get_pin('d:11:o')
    LIGHT_1 = arduino.get_pin('d:23:o')
    LIGHT_2 = arduino.get_pin('d:22:o')
    LIGHT_3 = arduino.get_pin('d:2:o')

    main(arduino)    
