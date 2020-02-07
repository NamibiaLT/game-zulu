import time
from pyfirmata import Arduino, util

class KeyboardArduino:
    def __init__(self):
        self.pins = {
            'd:11:p': self.light(),
            'd:10:p': self.light(),
            'd:3:p': self.light(),
            'd:2:p': self.light(),
            'd:5:p': self.light(),
            'd:4:p': self.light(),
            'd:13:p': self.light(),
            'd:36:i': self.button(),
            'd:37:i': self.button(),
            'd:35:i': self.button(),
            'd:36:i': self.button(),
            'd:30:i': self.button(),
            'd:32:i': self.button(),
            'd:31:i': self.button(),
            'd:34:i': self.button(),
            'd:33:i': self.button(),
        }
    def get_pin(self, pin):
        return self.pins[pin]
        
    class light:
        def __init__(self):
            self.value = False
        def read(self):
            return self.value
        def write(self, val):
            self.value = val
    class button:
        def __init__(self):
            self.value = False
        def read(self):
            return self.value

def getArduino():
  ##### BUTTON BOX CONFIGURATION ##########################################################
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
      arduino = KeyboardArduino()

  iterator = util.Iterator(arduino)
  iterator.start()
  time.sleep(0.5)   # Give time for arduino to initialize
  return arduino