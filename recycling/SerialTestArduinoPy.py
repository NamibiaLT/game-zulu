try:
    from pyfirmata import Arduino, util
except:
    import pip
    pip.main(['install','pyfirmata'])
    from pyfirmata import Arduino, util
    
import time
    
try:    
    board = Arduino('/dev/ttyACM0')
except:
    board = Arduino('/dev/ttyACM1')

iterator = util.Iterator(board)
iterator.start()

#BUTTON_BLUE = board.digital[4]

BUTTON_BLUE = board.get_pin('d:4:i')
LIGHT_GREEN = board.get_pin('d:3:p')

time.sleep(1)


        
def buttonPressed():
    if (BUTTON_BLUE.read() == False):
        return "BUTTON BLUE"

while True:
    
    time.sleep(1)

#    BUTTON_BLUE.read()
#    print(BUTTON_BLUE.read())
#    time.sleep(3)
    BUTTON_YELLOW = True

    if(BUTTON_BLUE.read() == False):
        LIGHT_GREEN.write(1)
#        print(BUTTON_BLUE.read())
    else:
        LIGHT_GREEN.write(0)
        
    BUTTON_ALL = [BUTTON_BLUE.read(), BUTTON_YELLOW]
    print(BUTTON_ALL)
    
    if False in BUTTON_ALL:
        print("BLUE BUTTON PRESSED")
    
    #buttonPressed()
    #print(buttonPressed())



    
#    
#    LIGHT_GREEN.write(0)
#    board.pass_time(1)
#    LIGHT_GREEN.write(1)
#    board.pass_time(1)
    
    
    

#print(buttonPressed.read())

#for i in range(100):
#    lightPressed.write(i/100)
#    time.sleep(0.1)
#time.sleep(5)
#
#lightPressed.write(0)
#
#
#board.exit()
