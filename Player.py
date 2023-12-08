import pygame
from os import path
import os
import math

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"Sprites")

def image_loader(image):
    sprite = pygame.image.load(os.path.join(img_folder,image)).convert()
    return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):      
        super().__init__()
        #importing sprites
        self.idleL = [image_loader("player_idle0000.png"),image_loader("player_idle0001.png"),image_loader("player_idle0002.png"),image_loader("player_idle0003.png")]
        self.idleR = [image_loader("player_idle_r0000.png"),image_loader("player_idle_r0001.png"),image_loader("player_idle_r0002.png"),image_loader("player_idle_r0003.png")]
        self.walkL = [image_loader("player_walk_l0000.png"),image_loader("player_walk_l0001.png"),image_loader("player_walk_l0002.png"),image_loader("player_walk_l0003.png"),image_loader("player_walk_l0004.png")]
        self.walkR = [image_loader("player_walk_r0000.png"),image_loader("player_walk_r0001.png"),image_loader("player_walk_r0002.png"),image_loader("player_walk_r0003.png"),image_loader("player_walk_r0004.png")]        
        self.jump_img = [image_loader("player_idle0000.png"),image_loader("player_idle_r0000.png")]
        self.fall_img = [image_loader("player_idle0002.png"),image_loader("player_idle_r0002.png")]
        
        #variables for the animation
        self.walk_count = 0
        self.image = self.idleL
        self.image = (self.idleL[1])
        self.rect = self.image.get_rect(topleft = pos)
        self.direct = "L"
        
        #player movemnt
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.9
        self.jump_speed = -16
        self.jump_count = 1
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if self.walk_count >= 40:
            self.walk_count = 0
        
        #moving side to side
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.direct = "R"
            self.image = (self.walkR[self.walk_count //8])
            self.walk_count += 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.direct = "L"
            self.image = (self.walkL[self.walk_count //8])
            self.walk_count += 1
        #idle animation
        else:
            self.direction.x = 0
            if self.direct == "R":
                self.image = (self.idleR[self.walk_count //10])
            else:
                self.image = (self.idleL[self.walk_count //10])
            self.walk_count += 1
            
        #jump animation
        if keys[pygame.K_SPACE] and self.jump_count >= 1 or keys[pygame.K_w] and self.jump_count >= 1:
            self.jump()
            self.walk_count = 0
            self.jump_count = 0
            
        #makes it be jump image when jumping   
        if self.direction.y < 0 and self.direct == "L":
            self.image = self.jump_img[0]
        if self.direction.y < 0 and self.direct == "R":
            self.image = self.jump_img[1]
        #makes it be fall image when falling    
        if self.direction.y > 0 and self.direct == "L":
            self.image = self.fall_img[0]
        if self.direction.y > 0 and self.direct == "R":
            self.image = self.fall_img[1]
            
        #self.image.set_colorkey((0,0,0))#getting rid of the background
        self.image.set_colorkey((255,255,255))#getting rid of the background
            
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        self.direction.y = self.jump_speed
            
    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.speed
        
        #maaking player cordonates gloabal
        global playerX
        playerX = self.rect.x
        global playerY
        playerY = self.rect.y
        

#arms for the crab
class Arm(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.open = pygame.image.load(os.path.join(img_folder,"claw_open.png")).convert()
        self.closed = pygame.image.load(os.path.join(img_folder,"claw_closed.png")).convert()
                                        
        self.image = self.open
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(bottomright = pos)
        
        self.offset = 25
        self.radius = 32
        self.angle = 0

    def get_input(self): #seeing if player pressed mouse button
        click = pygame.mouse.get_pressed()
        
        if click[0] == 1:
            self.image = self.closed
        else:
            self.image = self.open
            
    def aim(self):
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        
    def update(self):
        self.get_input()
        
        #pointing the arm at the mouse
        mouseX, mouseY = pygame.mouse.get_pos()
        dx, dy = mouseX - self.rect.centerx, mouseY - self.rect.centery
        self.angle = math.degrees(math.atan2(-dy,dx))
        self.aim()
        
        self.image.set_colorkey((0,0,0))
        
        #off setting arm from player
        self.rect.centerx = playerX + 64/2
        self.rect.centery = playerY + 20
    