import pygame, os, random
from settings import *
from projectiles import Bullet, Grenade
from sound import shot_fx

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
        self.s_ammo = S_AMMO
        self.start_sammo = S_AMMO
        self.g_ammo = G_AMMO
        self.start_gammo = G_AMMO
        # ai specific methods
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20) # what ai sees
        
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
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        
    def update(self):        
        if not self.alive:
            self.dead_animation(3)  # Play death animation
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            # Regular updates for alive characters
            self.update_animation()
            self.check_alive()
        
    def movement(self, moving_left, moving_right, world, screen_scroll,bg_scroll, level_length):
        screen_scroll = 0    
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
            self.vel_y = 10
        dy += self.vel_y
        
        # check for collision 
        for tile in world.obstacle_list:
            # check collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            # check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check collison while jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check collison while falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        
        # collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True       
        # collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        
        # player falls off the map 
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0
        
        # check so player donot run off the map
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0  
        # actually moves the player 
        self.rect.x += dx
        self.rect.y += dy
        
        # update scroll
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (level_length * TILE_SIZE) - SCREEN_WIDTH)\
                or (self.rect.right < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        
        return screen_scroll, level_complete
    
    def update_animation(self):
        # If the character is alive, update animations based on actions (idle, run, jump)
        
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Reset or loop depending on the action type
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:  # Death animation should not loop
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0  # Loop animations for idle, run, etc.
    
    def dead_animation(self, action):
        self.action = action
        # Always set the current image based on the current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed to update the frame
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            # Update the timing and increment the frame index if possible
            self.update_time = pygame.time.get_ticks()  # Update time here
            if self.frame_index < len(self.animation_list[self.action]) - 1:
                self.frame_index += 1
            else:
                # If on the last frame, keep it there and stop incrementing
                self.frame_index = len(self.animation_list[self.action]) - 1

    def update_action(self, new_action):
        #check if new action is different from the previous action
        # print(new_action)
        if new_action != self.action and self.alive:
            self.action = new_action
            self.frame_index = 0 # reset animation
            self.update_time = pygame.time.get_ticks()
    
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
        
    def shoot_b(self):
        if self.shoot_cooldown == 0 and self.s_ammo > 0:
            self.shoot_cooldown = SHOOT_COOLDOWN    
            bullet = Bullet(self.rect.centerx + (self.rect.size[0] * 0.6 * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.s_ammo -= 1 # reduce ammo
            shot_fx.play()
    def throw_g(self):
        if self.g_ammo > 0:
            grendade = Grenade(self.rect.centerx + (self.rect.size[0] * 0.6 * self.direction), self.rect.top, self.direction)
            grendade_group.add(grendade)   
            self.g_ammo -= 1 # reduce ammo
    
    def ai(self, world, screen_scroll, bg_scroll, level_length):
        for player in player_group:
            if self.alive and player.alive:
                if self.idling == False and random.randint(1, 200) == 69:
                    self.update_action(0)
                    self.idling = True
                    self.idling_counter = 50
                # Detect player in vision
                if self.vision.colliderect(player.rect):
                    # Transition to idle before shooting
                    if not self.idling:
                        self.update_action(0)  # idle frame
                        self.idling = True
                        self.idling_counter = 10  # delay before shooting
                    elif self.idling_counter <= 0:
                        # once the delay is over, start shooting
                        self.shoot_b()
                    else:
                        # Countdown during the idle delay
                        self.idling_counter -= 1
                else:
                    if self.idling == False:
                        if self.direction == 1:
                            ai_move_right = True
                        else:
                            ai_move_right = False
                        ai_move_left = not ai_move_right
                        self.movement(ai_move_left, ai_move_right, world, screen_scroll, bg_scroll, level_length)
                        self.update_action(1) # run
                        self.move_counter += 1 
                        self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                        if abs(self.move_counter) > TILE_SIZE:
                            self.direction *= -1
                            self.move_counter = 0
                    else:
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self. idling = False
        
        self.rect.x += screen_scroll
            
    def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
    
    def draw(self, health):
        self.health = health
        
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y -2 , 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))
        