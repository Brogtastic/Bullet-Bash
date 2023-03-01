import pygame
import sys
import math
import random

pygame.init()
pygame.font.init()

size = width, height = 800, 600
display = pygame.display.set_mode(size)
pygame.display.set_caption('Bullet Bash Menu')

backgroundColor = (26, 32, 64, 25)

while True:

    display.fill(backgroundColor)
    pygame.display.update()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
