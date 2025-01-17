#***********  GAME SETTINGS **********
import pygame


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#Player settings
P_SIZE = 2
P_SPEED = 10

# Game variables
GRAVITY = 0.75
ANIMATION_COOLDOWN = 100
clock = pygame.time.Clock()

# Basic Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)