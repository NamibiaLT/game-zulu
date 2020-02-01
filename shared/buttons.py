def buttons(arduino):
    return {
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