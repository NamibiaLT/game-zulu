
#fd

from moviepy.editor import VideoFileClip
import pygame

pygame.display.set_caption('My video!')

clip = VideoFileClip(r'C:\Users\bellj23\Documents\code\game-zulu\Video\Stars-Space-Effect-Background-HD-1.mp4') # "r" denote raw string
clip.preview()
pygame.quit()