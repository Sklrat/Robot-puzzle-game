import pygame
import math
from math import cos, sin
from Tiles import Tile, Wall, Door
from Settings import tile_size, screen_width
from Player import Player, Arm
from Items import Block, Button, Key


class Level:
    def __init__(self,level_data,surface):
        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0 #how much map scroll
        
    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.arm = pygame.sprite.GroupSingle()
        self.blocks = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.door = pygame.sprite.GroupSingle()
        self.key = pygame.sprite.GroupSingle()
        
        for row_index,row in enumerate(layout):#looping though each row, enumerate gives us the index(which loop we on) and info
            for col_index,cell in enumerate(row):
                    #getting the cordniates
                x = col_index * tile_size
                y = row_index * tile_size
                    
                if cell == 'X':#placing tiles
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                    
                if cell == 'P':#placing player
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
                    arm_sprite = Arm((x,y))
                    self.arm.add(arm_sprite)
                    
                if cell == 'B':#placing tiles
                    block = Block((x,y))
                    self.blocks.add(block)
                    
                if cell == 'b':
                    button = Button((x,y + 32))
                    self.buttons.add(button)
                    
                if cell == 'W':#placing walls
                    wall = Wall((x,y),tile_size)
                    self.walls.add(wall)
                    
                if cell == 'D':#placing door
                    door = Door((x,y))
                    self.door.add(door)
                    
                if cell == 'K':#placing key
                    key = Key((x,y))
                    self.key.add(key)
                    
#making map scroll when player is about to go off screen                    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
            
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
            
        else:
            self.world_shift = 0
            player.speed = 8
 
#--------------------------------------collissions---------------------------------------
#hmc stands for horizontal movment collission and vmc stands for vertical movment collision
#player collision for tiles 
    def hmc_tile_player(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    
    def vmc_tile_player(self):
        player = self.player.sprite
        player.apply_gravity()
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0 #this line resets the gravity
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.jump_count = 1
                    
#player collision with the wall
    def hmc_wall_player(self):
        player = self.player.sprite
        
        for sprite in self.walls.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    
    def vmc_wall_player(self):
        player = self.player.sprite
        
        for sprite in self.walls.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0 #this line resets the gravity
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.jump_count = 1
                    
#player collision for blocks 
    def hmc_block_player(self):
        player = self.player.sprite
        block = self.blocks.sprites()
        
        for block in self.blocks.sprites():
            for sprite in self.blocks.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        block.rect.right = player.rect.left
                        block.direction.x = player.direction.x
                    elif player.direction.x > 0:
                        block.rect.left = player.rect.right
                        block.direction.x = player.direction.x
                    
    def vmc_block_player(self):
        player = self.player.sprite
        block = self.blocks.sprites()
        
        for block in self.blocks.sprites():
            for sprite in self.blocks.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.y < 0:
                        block.rect.bottom = player.rect.top
                    if player.direction.y > 0:
                        player.rect.bottom = block.rect.top
                        player.jump_count = 1
 
 #block and tile collision
    def hmc_tile_block(self):
        block = self.blocks.sprites()
        
        for block in self.blocks.sprites():
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(block.rect):
                    if block.direction.x < 0:
                        block.rect.left = sprite.rect.right
                        block.direction.x = 0
                    elif block.direction.x > 0:
                        block.rect.right = sprite.rect.left
                        block.direction.x = 0
                    
    def vmc_tile_block(self):
        block = self.blocks.sprites()
        
        for block in self.blocks.sprites():
            block.apply_gravity()
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(block.rect):
                    if block.direction.y < 0:
                        block.rect.top = sprite.rect.bottom
                        block.direction.y = 0 #this line resets the gravity
                    elif block.direction.y > 0:
                        block.rect.bottom = sprite.rect.top
                        block.direction.y = 0
                    
 #block and wall collision
    def hmc_wall_block(self):
        block = self.blocks.sprites()
        
        for block in self.blocks.sprites(): 
            for sprite in self.walls.sprites():
                if sprite.rect.colliderect(block.rect):
                    if block.direction.x < 0:
                        block.rect.left = sprite.rect.right
                        block.direction.x = 0
                    elif block.direction.x > 0:
                        block.rect.right = sprite.rect.left
                        block.direction.x = 0
                    
    def vmc_wall_block(self):
        block = self.blocks.sprites()
        
        for block in self.blocks.sprites():
            for sprite in self.walls.sprites():
                if sprite.rect.colliderect(block.rect):
                    if block.direction.y < 0:
                        block.rect.top = sprite.rect.bottom
                        block.direction.y = 0 
                    elif block.direction.y > 0:
                        block.rect.bottom = sprite.rect.top
                        block.direction.y = 0
                    

                    
 #key and tile collision                    
    def vmc_tile_key(self):
        key = self.key.sprite
        key.apply_gravity()
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(key.rect):
                if key.direction.y < 0:
                    key.rect.top = sprite.rect.bottom
                    key.direction.y = 0 
                elif key.direction.y > 0:
                    key.rect.bottom = sprite.rect.top
                    key.direction.y = 0
                    
 #key and block collision                    
    def vmc_block_key(self):
        key = self.key.sprite
        block = self.blocks.sprites()
        
        for block in self.blocks.sprites():
            if block.rect.colliderect(key.rect):
                if key.direction.y < 0:
                    key.rect.top = block.rect.bottom
                    key.direction.y = 0 
                elif key.direction.y > 0:
                    key.rect.bottom = block.rect.top
                    key.direction.y = 0
 
 #block and wall collision
    def hmc_block_key(self):
        key = self.key.sprite
        block = self.blocks.sprites()
        
        for block in self.blocks.sprites():        
            if block.rect.colliderect(key.rect):
                if key.direction.x < 0:
                    key.rect.right = block.rect.left
                    key.direction.x = 0 
                elif key.direction.x > 0:
                    key.rect.left = block.rect.right
                    key.direction.x = 0          
                    
    #button and player collisiosn
    def vmc_button_player(self):
        player = self.player.sprite
        
        for sprite in self.buttons.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    sprite.pressed = True
                    self.buttons.update(0)
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.jump_count = 1
            else:
                sprite.pressed = False
                self.buttons.update(0)
                
    def hmc_button_player(self):
        player = self.player.sprite
        
        for sprite in self.buttons.sprites():
            if sprite.rect.colliderect(player.rect):
                    sprite.pressed = True
                    self.buttons.update(0)
                    player.rect.bottom = sprite.rect.top
                    player.jump_count = 1

#button and block collision
    def vmc_button_block(self):
        block = self.blocks.sprites()
        
        for block in self.blocks.sprites():
            for sprite in self.buttons.sprites():
                if sprite.rect.colliderect(block.rect):
                    if block.direction.y > 0:
                        sprite.pressed = True
                        self.buttons.update(0)
                        block.rect.bottom = sprite.rect.top
                        block.direction.y = 0
                    
    def hmc_button_player(self):
        block = self.blocks.sprites()
        
        for block in self.blocks.sprites():
            for sprite in self.buttons.sprites():
                if sprite.rect.colliderect(block.rect):
                        sprite.pressed = True
                        self.buttons.update(0)
                        block.rect.bottom = sprite.rect.top
                    
    #arm and block colission
    def block_pick_up(self):
        click = pygame.mouse.get_pressed()
        arm = self.arm.sprite
        block = self.blocks.sprites()
        
        for block in self.blocks.sprites():
            if arm.rect.colliderect(block.rect):
                if click[0] == 1:
                    block.grab = True
                    self.radAngle = math.pi * arm.angle / 180.

                    armLen = arm.image.get_width()/2
                    #putting block where arm is
                    block.rect.center = \
                        ( arm.rect.center[0] + armLen*cos(self.radAngle),
                          arm.rect.center[1] - armLen*sin(self.radAngle) )

                    self.dest = (block.rect.centerx + 1000*cos(self.radAngle), 
                                 block.rect.centery - 1000*sin(self.radAngle) )
                else:
                    block.grab = False
      
      #unlocking the door
    def door_unlock(self):
        keys = pygame.key.get_pressed()
        door = self.door.sprite
        key = self.key.sprite
        
        if key.rect.colliderect(door.rect) and key.grab and keys[pygame.K_s]:
            door.locked = False
            
                
    #arm and key colission
    def key_pick_up(self):
        key = self.key.sprite
        click = pygame.mouse.get_pressed()
        arm = self.arm.sprite
        
        if arm.rect.colliderect(key.rect):
            if click[0] == 1:
                key.grab = True
                self.radAngle = math.pi * arm.angle / 180.

                armLen = arm.image.get_width()/2
                #putting block where arm is
                key.rect.center = \
                    ( arm.rect.center[0] + armLen*cos(self.radAngle),
                      arm.rect.center[1] - armLen*sin(self.radAngle) )

                self.dest = (key.rect.centerx + 1000*cos(self.radAngle), 
                             key.rect.centery - 1000*sin(self.radAngle) )
            else:
                key.grab = False
                
        
        #win condition and saying you win
    def win(self):
        door = self.door.sprite
        player = self.player.sprite
        win = False
        
    #creating text
        font_name = pygame.font.match_font('arial')
        def draw_text(text, size, x,y):
            font = pygame.font.Font(font_name, size)
            text_surface = font.render(text, True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x, y)
        
        if player.rect.colliderect(door.rect) and door.locked == False:
            win = True
            
        if win:
            draw_text('You win', 100, 100, 100)
            print('You win')
            
                
    def run(self):
        #level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        
        #door
        self.door.update(self.world_shift)
        self.door.draw(self.display_surface)
        self.door_unlock()
        
        #walls
        self.walls.update(self.world_shift)
        if self.buttons.sprites()[0].pressed == False:#will make the wall dissaper if button is pressed
            self.walls.draw(self.display_surface)
        self.scroll_x()
        
        #player
        self.player.update()
        self.hmc_tile_player()
        self.vmc_tile_player()
        
        if self.buttons.sprites()[0].pressed == False:#making the wall collidable when button is not pressed
            self.hmc_wall_player()
            self.vmc_wall_player()
            
        if self.blocks.sprites()[0].grab == False:#turning block player collision off when player grabbing block
            self.vmc_block_player()
            self.hmc_block_player()
            
        self.vmc_button_player()
        self.hmc_button_player()
        self.player.draw(self.display_surface)
        #arm
        self.arm.update()
        self.block_pick_up()
        self.key_pick_up()
        self.arm.draw(self.display_surface)
        self.player.draw(self.display_surface)
        
        #blocks
        self.blocks.update(self.world_shift)
        self.hmc_tile_block()
        self.vmc_tile_block()
        self.hmc_wall_block()
        self.vmc_wall_block()
        self.vmc_button_block()
        self.blocks.draw(self.display_surface)
        self.scroll_x()
        
        
        #buttons
        self.buttons.update(self.world_shift)
        self.buttons.draw(self.display_surface)
        
        #key
        self.key.update(self.world_shift)
        self.vmc_tile_key()
        self.hmc_block_key()
        self.vmc_block_key()
        self.key.draw(self.display_surface)
        
        self.win()
        
