#***********  GAME SETTINGS **********
import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
TILE_SIZE = 75

# Game variables
GRAVITY = 0.75
ANIMATION_COOLDOWN = 100
clock = pygame.time.Clock()

#Character settings
C_SIZE = 2
C_SPEED = 10
P_SPEED = 10
C_HEALTH = 100

#Projectiles
B_PATH = 'assets/images/icons/bullet.png'
B_SPEED = 10
S_AMMO = 20
SHOOT_COOLDOWN = 20
G_PATH = 'assets/images/icons/grenade.png'
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