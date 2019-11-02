import pygame, sys
from pygame.locals import *

"""
gameboardDimension = (1100,750)
scaleDimension will fit image to the size gb[0] * ratio, gb[1]
ratio is set at 750/1100
"""

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1000, 750))
pygame.display.set_caption('Hello Learned One')

img = pygame.image.load('severus.jpeg')
DISPLAYSURF.blit(img, (0,0))
while True: #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()
