import pygame
from settings import *

# create sprite groups
bullet_group = pygame.sprite.Group()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, ):
        pygame.sprite.Sprite.__init__(self)
        bullet_image = pygame.image.load(BULLET_PATH).convert_alpha()
        bullet_image = pygame.transform.scale(bullet_image, (int(bullet_image.get_width()), int(bullet_image.get_height())))
        self.image = bullet_image
        self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self, player_group, enemy_group):
        self.rect.x += (self.direction * self.speed)
        
        # check if bullet gone offscreen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # check collison with enemy
        for player in pygame.sprite.spritecollide(self, player_group, False):
            if player.alive:
                player.health -= 10
                self.kill()
                print(player.health)
    
        for enemy in pygame.sprite.spritecollide(self, enemy_group, False):
            if enemy.alive:
                enemy.health -= 25
                self.kill()
                print(enemy.health)
                
    
