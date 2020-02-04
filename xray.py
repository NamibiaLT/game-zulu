#Game Details:
# lights1,2,3,4,5 will sequence when won
# Must push button1,2,3 in the correct sequence
# lights1,2,3,4,5 will come on consequitively when correct sequence is pushed.


# Possible number of inputs. Player cannot try anymore than this.
numInputs = 3

# pins the buttons are connected too
inputPins(numInputs]) = (4,3,2)


# number of steps in the sequence that the player must follow
numSteps = 5

# Correct sequence of inputs required to solve the pizzle
steps[numSteps] = (0, 2, 1, 1, 0) # press button #2 once, then button #3 twice then button #0 then button #1

# pins are used to light up LEDs to show the player's progress, so one output pin per step in the puzzle'
ledPins[numSteps] = {12, 11, 10, 9, 8}

# This pin will be driven LOW to release a lock when puzzle is solved
lockPin = A0 
    success()

# Assume the defailt state of each switch is HIGH
lastInputState[] = {HIGH, HIGH, HIGH, HIGH}

# What step of the sequence is the player currently on?
currentSteps = 0

#Put this in game loop

##loop through all the inputs
for i in buttons():
    if(button[i] == LOW and lastInputState[i] == HIGH):
        if(steps[currentSteps] == i):
            currentStep += 1
        else:
            currentStep = 0
            print('Incorrect input! Back to the beginning!')
    
    # Update the stored value for this input
    lastInputState[i] = currentInputState

    # Check whether the puzzle has been solved
    if(currentStep == numSteps)
        success()

    # Turn on the number of LEDs corresponding to the current step
    for i in numSteps:
        lights(write[i]), (i < currentStep ? HIGH : LOW)    