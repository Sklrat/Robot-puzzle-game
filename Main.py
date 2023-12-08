import pygame
import random
#importing other scripts
from Settings import *
from Tiles import Tile
from Level import Level

FPS = 30

screen = pygame.display.set_mode((screen_width, screen_height))

level = Level(level_map,screen)

#difine colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BG_COLOR = (150,150,150)

# initilize pygame and create window
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Robot puzz")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


#Game loop
running = True
while running:
    #keep loop running at the right speed
    clock.tick(FPS)
    #Process input (events)
    
    #stops program when close window
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
    #Update
    all_sprites.update()
    #Draw / render
    screen.fill(BG_COLOR)
    
    level.run()
    
    
    all_sprites.draw(screen)
    # after drawing everything, flip the display
    pygame.display.flip()
    
pygame.quit()
    
    