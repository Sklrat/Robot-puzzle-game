import pygame
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"Sprites")

GREY = (50,50,50)
BLUE = (0,255,255)

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill(GREY)
        self.rect = self.image.get_rect(topleft = pos)

    def update(self,x_shift):#level scrolling
        self.rect.x += x_shift
        
        
class Wall(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft = pos)

    def update(self,x_shift):#level scrolling
        self.rect.x += x_shift
        
        
class Door(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.open = pygame.image.load(os.path.join(img_folder,"door_open.png")).convert()
        self.closed = pygame.image.load(os.path.join(img_folder,"door_closed.png")).convert()
        self.image = self.closed
        self.rect = self.image.get_rect(topleft = pos)
        self.locked = True

    def update(self,x_shift):#level scrolling
        self.rect.x += x_shift
        
        if self.locked == False:
            self.image = self.open
            
            