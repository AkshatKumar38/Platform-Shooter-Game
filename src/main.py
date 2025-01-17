import pygame
from settings import *
from player import Character

pygame.init()
pygame.display.set_caption("Shooter Game")

def BG():
    screen.fill(BLUE)
    pygame.draw.line(screen, RED, (0,300), (SCREEN_WIDTH,300))
    
def main():
    game_over = False
    player = Character('player',200, 200,P_SIZE, P_SPEED)
    enemy = Character('enemy',400, 200,P_SIZE, P_SPEED)
    
    moving_right = False
    moving_left = False
    while not game_over:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit game
                game_over = True
                break
            # button presses
            elif event.type == pygame.KEYDOWN: # movement keys
                if event.key == pygame.K_a:
                    moving_left =True
                if event.key == pygame.K_d:
                    moving_right =True
                if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and player.alive:
                    player.jump = True
                if event.key == pygame.K_ESCAPE:
                    game_over = True
            
            # button releases
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                elif event.key == pygame.K_d:
                    moving_right = False
                     
        # only change action if player is alive
        if player.alive:               
            # changing action when running or idle or jumping
            if moving_left or moving_right:
                player.update_action(1) # 1 = run
            elif player.in_air == True:
                player.update_action(2)
            else:
                player.update_action(0) # 0 = idle
                enemy.update_action(0)
            
        BG()  
        player.draw()
        enemy.draw()
        player.update_animation()
        enemy.update_animation()
        player.movement(moving_left, moving_right)
        
        pygame.display.update()
    pygame.quit()
            
if __name__ == "__main__": 
    main()