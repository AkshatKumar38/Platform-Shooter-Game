import pygame
from settings import *

hbox_img = pygame.image.load(HEALTH_BOX).convert_alpha()
gbox_img = pygame.image.load(GRENADE_BOX).convert_alpha()
abox_img = pygame.image.load(AMMO_BOX).convert_alpha()

item_boxes = {
    'health'    : hbox_img,
    'grenade'   : gbox_img,
    'ammo'      : abox_img
}

item_group = pygame.sprite.Group()

class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type, x, y ):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self, player_group):
        # check collision with player
        for player in pygame.sprite.spritecollide(self, player_group, False):
            if player.alive:
                if self.item_type == 'health':
                    player.health += 25
                    if player.health > player.max_health:
                        player.health = player.max_health
                if self.item_type == 'grenade':
                    player.g_ammo += 1
                else:
                    player.s_ammo += 5
                self.kill()
                
            