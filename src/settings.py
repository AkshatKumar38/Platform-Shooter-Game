#***********  GAME SETTINGS **********
import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
TILE_SIZE = 40
FPS = 60

# Game variables
GRAVITY = 0.75
ANIMATION_COOLDOWN = 100
clock = pygame.time.Clock()

# Character settings
C_SIZE = 2
C_SPEED = 5
P_SPEED = 10
C_HEALTH = 100

# Projectiles
B_PATH = 'assets/images/icons/bullet.png'
bullet_image = pygame.image.load(B_PATH).convert_alpha()
B_SPEED = 15
S_AMMO = 5
SHOOT_COOLDOWN = 20
G_PATH = 'assets/images/icons/grenade.png'
grenade_image = pygame.image.load(G_PATH).convert_alpha()
grenade_image = pygame.transform.scale(grenade_image, (int(grenade_image.get_width()), int(grenade_image.get_height())))
G_SPEED = 7
G_AMMO = 2
G_TIMER = 100
E_SPEED = 4

# Pickups
HEALTH_BOX  = 'assets/images/icons/health_box.png'
GRENADE_BOX  = 'assets/images/icons/grenade_box.png'
AMMO_BOX  = 'assets/images/icons/ammo_box.png'

# Basic Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)