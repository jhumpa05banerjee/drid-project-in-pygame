import pygame
import time
import random

pygame.init()
width,height=1000,700
screen=pygame.display.set_mode((width,height))

pygame.display.set_caption("Whack-a-Mole")
clock = pygame.time.Clock()

mole=pygame.transform.scale(pygame.image.load("images/mole.jpg"),(100,150))

running=True
while running==True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            pygame.quit()
