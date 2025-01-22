import pygame
from settings import *
from player import Character, HealthBar
from pickups import ItemBox

# background images
pine1_img = pygame.image.load('assets/images/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('assets/images/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('assets/images/background/mountain.png').convert_alpha()
sky_cloud_img = pygame.image.load('assets/images/background/sky_cloud.png').convert_alpha()

class World():
    def __init__(self):
        self.obstacle_list = []
    
    def process_data(self, data):
        level_length = len(data[0])
        # Load tile images
        img_list = []
        player = None  # Initialize the player variable
        for x in range(TILE_TYPES):
            img = pygame.image.load(f'assets/images/tile/{x}.png').convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            img_list.append(img)

        # Process the world data
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)

                    if 0 <= tile <= 8:  # Dirt blocks
                        self.obstacle_list.append(tile_data)
                    elif 9 <= tile <= 10:  # Water
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif 11 <= tile <= 14:  # Decorations
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  # Player
                        player = Character('player', x * TILE_SIZE, y * TILE_SIZE, C_SIZE, P_SPEED)
                        player_group.add(player)
                        health_bar = HealthBar(10,10, player.health, player.max_health)
                        health_bar.draw(player.health) # show health bar
                    elif tile == 16:  # Enemy
                        enemy = Character('enemy', x * TILE_SIZE, y * TILE_SIZE, C_SIZE, C_SPEED)
                        enemy_group.add(enemy)
                    elif tile == 17:  # Ammo box
                        ammo = ItemBox('ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_group.add(ammo)
                    elif tile == 18:  # Grenade box
                        grenade = ItemBox('grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_group.add(grenade)
                    elif tile == 19:  # Health box
                        health = ItemBox('health', x * TILE_SIZE, y * TILE_SIZE)
                        item_group.add(health)
                    elif tile == 20:  # Exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                        
        # Check if player was created
        if player is None:
            raise ValueError("Player could not be initialized. Ensure the world data contains a player tile (15).")

        return player, health_bar, level_length
        
    def display_text(text, font, colour, x, y):
        img = font.render(text, True, colour)
        screen.blit(img, (x, y))
    
    def bg(self, bg_scroll):
        screen.fill(GREEN)
        width  = sky_cloud_img.get_width()
        for x in range(4):
            screen.blit(sky_cloud_img, ((x * width) - bg_scroll * 0.5, 0))
            screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
            screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
            screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height() ))
            
    def draw_world(self, screen_scroll):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y ):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self, screen_scroll):
        self.rect.x += screen_scroll
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y ):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self, screen_scroll):
        self.rect.x += screen_scroll
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y ):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self, screen_scroll):
        self.rect.x += screen_scroll