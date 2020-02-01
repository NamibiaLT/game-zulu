# LIGHT_BLUE_PIN = False
# LIGHT_YELLOW_PIN = False
# LIGHT_1_PIN = False
# LIGHT_2_PIN = False
# LIGHT_3_PIN = False
# lightsArray = [LIGHT_GREEN_PIN, LIGHT_BLUE_PIN, LIGHT_YELLOW_PIN, LIGHT_1_PIN, LIGHT_2_PIN, LIGHT_3_PIN

blue = False
Red = False
lightArray = [blue, Red]
#########################################################################################

# def light(light, state):
#     if(state == 'on'):
#         for light in lightArray:
#             lightArray[light] = True  
#     if(state == 'off'):
#         for light in lightArray:  
#             lightArray[light] = False

on = True
off = False

def light(light, state):

    for light in lightArray:
        lightArray[light] = state  


print(lightArray[blue])
light(blue, on)
print(lightArray[blue])

# blue = True
# red = False
# print(blue)