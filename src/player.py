import pygame, os
from settings import *
from bullet import Bullet, bullet_group



class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.health = C_HEALTH
        self.max_health = self.health
        self.speed = speed
        self.jump = False
        self.in_air = True
        self.vel_y = 0
        self.direction = 1
        self.flip =False
        self.shoot_cooldown = 0
        self.ammo = AMMO
        self.start_ammo = AMMO
        
        self.frame_index = 0
        self.action = 0
        self.animation_list = []
        self.char_type = char_type
        self.update_time = pygame.time.get_ticks()
        
        animation_types = ['Idle','Run','Jump','Death'] # load all animation types
        for animation in animation_types:
            temp_list =[] # list to store images
            num_of_frames = len(os.listdir(f'assets/images/{self.char_type}/{animation}')) # count number of images in folder
            for i in range(num_of_frames):
                img = pygame.image.load(f'assets/images/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        
    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
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
        if self.jump and not self.in_air: 
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
    
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = SHOOT_COOLDOWN    
            bullet = Bullet(self.rect.centerx + (self.rect.size[0] * 0.6 * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1 # reduce ammo
            
    def update_animation(self):
		#update animation
        ANIMATION_COOLDOWN = 100
		#update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #check if new action is different from the previous action
        # print(new_action)
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0 # reset animation
            self.check_time = pygame.time.get_ticks()
    
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
        
    def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)