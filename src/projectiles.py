import pygame
from settings import *

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
    
    def update(self, world, screen_scroll):
        self.rect.x += (self.direction * self.speed)
        self.rect.x += screen_scroll
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
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
        self.image = grenade_image
        self.vel_x = G_SPEED
        self.vel_y = -10
        self.timer = G_TIMER
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self, world, screen_scroll):
        self.rect.x += screen_scroll
        self.vel_y += GRAVITY
        dx = self.direction * self.vel_x
        dy = self.vel_y
        
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.vel_x
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.vel_x = 0
                # check collison while thrown
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check collison while falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
                    
        
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

    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        self.counter += 1
        if self.counter >= E_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.image_list):
                self.kill()
            else:
                self.image = self.image_list[self.frame_index]