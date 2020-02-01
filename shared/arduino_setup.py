from pyfirmata import Arduino, util

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
      print("No Arduino board is detected\n")

  iterator = util.Iterator(arduino)   # Game is really slow. Would adding this iterator in another loop be better?
  iterator.start()
  time.sleep(0.5)   # Needed for arduino to initialize
  return arduino