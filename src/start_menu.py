import pygame
from settings import *
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('editor'))) 
from editor.button import Button
pygame.init()

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game - Menu")
FONT = pygame.font.SysFont('Futura', 40)

# Helper function to display text
def display_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    screen.blit(img, (x, y))

# start, restart and exit buttons
start_button_img = pygame.image.load('assets/images/buttons/start_btn.png').convert_alpha()
exit_button_img = pygame.image.load('assets/images/buttons/exit_btn.png').convert_alpha()
restart_button_img = pygame.image.load('assets/images/buttons/restart_btn.png').convert_alpha()

# create buttons
start_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_button_img, 1)
exit_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_button_img, 1)
restart_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 - 50, restart_button_img, 2)
def start_screen():
    running = True
    while running:
        screen.fill(BLUE)
        # Draw buttons
        if start_button.draw(screen):
            return True
        if exit_button.draw(screen):
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False

        pygame.display.update()
    pygame.quit()

def end_screen():
    running = True
    while running:
        screen.fill(BLACK)
        # Draw buttons
        if restart_button.draw(screen):
            return True
        if exit_button.draw(screen):
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False

        pygame.display.update()
    pygame.quit()
    
if __name__ == "__main__":
    start_screen()