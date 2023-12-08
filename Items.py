import pygame
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"Sprites")

GREEN = (0,255,0)

class Block(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((64,64))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = 8
        self.gravity = 0.8
        self.direction = pygame.math.Vector2(0,0)
        self.grab = False
        
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self,x_shift):#level scrolling
        self.rect.x += x_shift
       
class Button(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.off = pygame.image.load(os.path.join(img_folder,"button.png")).convert()
        self.on = pygame.image.load(os.path.join(img_folder,"button_pressed.png")).convert()
        self.image = self.off
        self.image.set_colorkey((0,0,0))
        
        self.rect = self.image.get_rect(topleft = pos)
        self.rect_off_Y = self.rect.y
        self.rect_on_Y = self.rect.y + 18
        
        self.pressed = False

    def update(self,x_shift):#level scrolling
        self.rect.x += x_shift
        
        if self.pressed:
            self.image = self.on
            self.rect.y = self.rect_on_Y
        else:
            self.image = self.off
            self.rect.y = self.rect_off_Y
            
        self.image.set_colorkey((0,0,0))
        
class Key(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(img_folder,"key.png")).convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(topleft = pos)
        self.gravity = 0.4
        self.direction = pygame.math.Vector2(0,0)
        self.grab = False
        
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self,x_shift):#level scrolling
        self.rect.x += x_shift