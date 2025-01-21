import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
FPS = 60

# Initialize window in windowed mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fullscreen Toggle Example")

# Colors
BLACK = (0, 0, 0)
BLUE = (50, 153, 213)
# Clock
clock = pygame.time.Clock()

# Main game loop
fullscreen = False

def toggle_fullscreen():
    global screen, fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    fullscreen = not fullscreen

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_F11:  # Press F11 to toggle fullscreen
                toggle_fullscreen()

    # Update and draw
    screen.fill(BLUE)

    # Refresh display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
