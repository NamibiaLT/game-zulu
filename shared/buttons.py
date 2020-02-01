from shared.display import DISPLAY_WIDTH, DISPLAY_HEIGHT
from ngini import arduino

# Button position, configuration, and action
BUTTON_WIDTH = DISPLAY_WIDTH * 0.25   # Number is a scaling factor. On 1920 screen this is a 300mm button
BUTTON_HEIGHT = DISPLAY_HEIGHT * 0.17    # Number is a scaling factor. On 1080 screen this is a 150mm button
BUTTON_CENTER_ONE_THIRD = (DISPLAY_WIDTH*0.33)-(BUTTON_WIDTH/2)
BUTTON_CENTER_TWO_THIRD = (DISPLAY_WIDTH*0.66)-(BUTTON_WIDTH/2)
BUTTON_CENTER_VERTICAL = (DISPLAY_HEIGHT*0.5)-(BUTTON_HEIGHT/2)

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