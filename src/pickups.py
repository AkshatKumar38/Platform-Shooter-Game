import pygame
from settings import *
# Pickups
HEALTH_BOX  = 'assets/images/icons/health_box.png'
GRENADE_BOX  = 'assets/images/icons/grenade_box.png'
AMMO_BOX  = 'assets/images/icons/ammo_box.png'

hbox_img = pygame.image.load(HEALTH_BOX).convert_alpha()
gbox_img = pygame.image.load(GRENADE_BOX).convert_alpha()
abox_img = pygame.image.load(AMMO_BOX).convert_alpha()

item_boxes = {
    'health'    : hbox_img,
    'grenade'   : gbox_img,
    'ammo'      : abox_img
}

class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type, x, y ):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        # check collision with player
        for player in pygame.sprite.spritecollide(self, player_group, False):
            if player.alive:
                if self.item_type == 'health':
                    player.health += 25
                    if player.health > player.max_health:
                        player.health = player.max_health
                    print("health collected")
                if self.item_type == 'grenade':
                    player.g_ammo += 1
                    print("grenade collected")
                if self.item_type == 'ammo':
                    player.s_ammo += 5
                    print("ammo collected")
                self.kill()
                
            