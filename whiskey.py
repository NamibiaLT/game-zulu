# Possible number of trys. Decrease this nuymber to increase difficulty.
MAX_TRYS = 3

# Number of steps in the sequence that the player must follow. Add numbers to increase difficulty.
correctSteps = [1,1,2]

# Initialize the guess list
guesses = [0,0,0]

# Lights to illuminate players progress
lights = [False, False, False]

# What step of the sequence is the player currently on? Initialize with 0 for first number in list.
currentStep = 0

# Players attempts. Initialize as 1st attempt.
attempts = 1

# Leave game loop when players beat the game or maximum # of trys are reached.
while currentStep < len(correctSteps) and attempts <= MAX_TRYS:
    
    # User enters their guess and it stores in the list as a number 
    guesses[currentStep] = int(input('Enter Number Guess (1-3): ' ))     

    # If the number equals the correct step, then add a light
    if(correctSteps[currentStep] == guesses[currentStep]):
        lights[currentStep] = True         
        currentStep += 1
    
    # If the number does not equal correct step, then turn off all lights
    else:
        currentStep = 0
        attempts += 1
        lights = [False, False, False]
        print('Incorrect input. Back to the beginning!')         
    
    print('Lights:', lights)
    print('')


# Check whether the puzzle has been solved
if guesses == correctSteps:
    print('YOU WIN.')
else:
    print('YOU LOSE.')




