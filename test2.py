gettingArdunioStuff2 = 2
gettingArdunioStuff1 = 1


buttons = {
  'button2': gettingArdunioStuff2,
  'button1': gettingArdunioStuff1
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

buttonsPressed(buttons['button2'])

print(buttonsPressed(buttons['button2']))