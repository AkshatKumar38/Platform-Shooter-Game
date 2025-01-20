import pygame
from settings import *

# create sprite groups
bullet_group = pygame.sprite.Group()
grendade_group = pygame.sprite.Group()
explosion_group= pygame.sprite.Group()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        bullet_image = pygame.image.load(B_PATH).convert_alpha()
        bullet_image = pygame.transform.scale(bullet_image, (int(bullet_image.get_width()), int(bullet_image.get_height())))
        self.image = bullet_image
        self.speed = B_SPEED
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self, player_group, enemy_group):
        self.rect.x += (self.direction * self.speed)
        
        # check if bullet gone offscreen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # check collison with player and enemy
        for player in pygame.sprite.spritecollide(self, player_group, False):
            if player.alive:
                player.health -= 25
                self.kill()
    
        for enemy in pygame.sprite.spritecollide(self, enemy_group, False):
            if enemy.alive:
                enemy.health -= 25
                self.kill()                
    
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        grenade_image = pygame.image.load(G_PATH).convert_alpha()
        grenade_image = pygame.transform.scale(grenade_image, (int(grenade_image.get_width()), int(grenade_image.get_height())))
        self.image = grenade_image
        self.vel_x = G_SPEED
        self.vel_y = -10
        self.timer = G_TIMER
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self, player_group, enemy_group):
        self.vel_y += GRAVITY
        dx = self.direction * self.vel_x
        dy = self.vel_y
        
        #check for collision with line
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.vel_x = 0
        
        self.rect.x += dx
        self.rect.y += dy
        
        # check if bullet gone offscreen
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
        
        # countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y)
            explosion_group.add(explosion)
        
            # check collison with enemy
            for player in player_group:
                if player.alive and abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2:
                    player.health -= 50
                    self.kill()
        
            for enemy in enemy_group:
                if enemy.alive and abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2:
                    enemy.health -= 50
                    self.kill()  
        
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        scale = 1.4
        self.image_list = [] # list to store images
        for i in range(1, 6):
            img = pygame.image.load(f'assets/images/explosion/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.image_list.append(img)
        self.frame_index = 0
        self.image = self.image_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= E_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.image_list):
                self.kill()
            else:
                self.image = self.image_list[self.frame_index]