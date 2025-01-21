#***********  GAME SETTINGS **********
import pygame
import pickle
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
FPS = 60

# Game variables
GRAVITY = 0.75
ANIMATION_COOLDOWN = 100
clock = pygame.time.Clock()
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 0

# Character settings
C_SIZE = 1.65
C_SPEED = 5
P_SPEED = 10
C_HEALTH = 100

# Projectiles
B_PATH = 'assets/images/icons/bullet.png'
bullet_image = pygame.image.load(B_PATH).convert_alpha()
B_SPEED = 15
S_AMMO = 20
SHOOT_COOLDOWN = 20
G_PATH = 'assets/images/icons/grenade.png'
grenade_image = pygame.image.load(G_PATH).convert_alpha()
grenade_image = pygame.transform.scale(grenade_image, (int(grenade_image.get_width()), int(grenade_image.get_height())))
G_SPEED = 7
G_AMMO = 20
G_TIMER = 100
E_SPEED = 4

# Basic Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)

# load level file
world_data = []
pickle_in = open(f'level{level}_data', 'rb')
world_data = pickle.load(pickle_in)

# create sprite groups
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grendade_group = pygame.sprite.Group()
explosion_group= pygame.sprite.Group()
item_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
