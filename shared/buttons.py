import pygame
from shared.display import DISPLAY_WIDTH, DISPLAY_HEIGHT, gameDisplay
from shared.text import text_objects

# Button position, configuration, and action
BUTTON_WIDTH = DISPLAY_WIDTH * 0.25   # Number is a scaling factor. On 1920 screen this is a 300mm button
BUTTON_HEIGHT = DISPLAY_HEIGHT * 0.17    # Number is a scaling factor. On 1080 screen this is a 150mm button
BUTTON_CENTER_ONE_THIRD = (DISPLAY_WIDTH*0.33)-(BUTTON_WIDTH/2)
BUTTON_CENTER_TWO_THIRD = (DISPLAY_WIDTH*0.66)-(BUTTON_WIDTH/2)
BUTTON_CENTER_VERTICAL = (DISPLAY_HEIGHT*0.5)-(BUTTON_HEIGHT/2)

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)