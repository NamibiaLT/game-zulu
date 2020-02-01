import pygame

# constants
gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_SIZE = gameDisplay.get_size()   #James work PC is 1920 1080
DISPLAY_WIDTH = SCREEN_SIZE[0]
DISPLAY_HEIGHT = SCREEN_SIZE[1]

def imageLoader(path):
  return pygame.transform.scale(pygame.image.load(path), SCREEN_SIZE)