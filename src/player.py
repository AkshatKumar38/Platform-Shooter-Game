import pygame, os
from settings import *

class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.jump = False
        self.in_air = True
        self.vel_y = 0
        self.direction = 1
        self.flip =False
        self.char_type = char_type
        self.frame_index = 0
        self.animation_list = []
        self.action = 0
        animation_types = ['Idle','Run','Jump'] # load all animation types
        for animation in animation_types:
            temp_list =[] # list to store images
            #count number of images in folder
            num_of_frames = len(os.listdir(f'assets/images/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'assets/images/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.check_time = pygame.time.get_ticks()
        
    
    
    def movement(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0
        
        # assign movement variables if left or right
        if moving_left:
            dx = -self.speed
            self.direction = -1
            self.flip = True
        if moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = False
        if self.jump == True and self.in_air == False: 
            self.vel_y = -10
            self.jump = False
            self.in_air = True
        
        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        
        
        #check for collision with line
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
        # actually moves the player 
        self.rect.x += dx
        self.rect.y += dy
    
    def update_animation(self):
        #update image depending on timepassed
        self.image = self.animation_list[self.action][self.frame_index]
        #check if cooldown finishes move to next img
        if pygame.time.get_ticks() - self.check_time > ANIMATION_COOLDOWN:
            self.check_time = pygame.time.get_ticks()
            self.frame_index += 1
        # loop for img
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
    def update_action(self, new_action):
        #check if new action is different from the previous action
        if new_action != self.action:
            self.action = new_action
            #reset animation
            self.frame_index = 0
            self.check_time = pygame.time.get_ticks()
        
    def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)