import pygame
from settings import *
from player import Character
from projectiles import bullet_group, grendade_group, explosion_group

pygame.init()
pygame.display.set_caption("Shooter Game")

player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

def BG():
    screen.fill(BLUE)
    pygame.draw.line(screen, RED, (0,300), (SCREEN_WIDTH,300))
    
def main():
    game_over = False
    enemy1 = Character('enemy',200, 265,C_SIZE, C_SPEED)
    enemy2 = Character('enemy',400, 265,C_SIZE, C_SPEED)
    
    player = Character('player',600, 200,C_SIZE, P_SPEED)
    
    player_group.add(player)
    enemy_group.add(enemy1, enemy2)
    moving_right = False
    moving_left = False
    shoot_b = False
    throw_g = False
    grendade_thrown = False
    
    while not game_over:
        clock.tick(60)
        
        BG()  
        player.draw()
        player.update()
        for enemy in enemy_group:
            enemy.draw()
            enemy.update()

        player.movement(moving_left, moving_right)
        
        # update and draw groups
        bullet_group.update(player_group,enemy_group)
        bullet_group.draw(screen)
        grendade_group.update(player_group,enemy_group)
        grendade_group.draw(screen)
        explosion_group.update()
        explosion_group.draw(screen)
        # event window
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
                if event.key == pygame.K_q:
                    shoot_b = True
                if event.key == pygame.K_f:
                    throw_g = True
                if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and player.alive:
                    player.jump = True
                if event.key == pygame.K_ESCAPE:
                    game_over = True
            
            # button releases
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_q:
                    shoot_b = False
                if event.key == pygame.K_f:
                    throw_g = False
                    grendade_thrown = False
                     
        # only change action if player is alive
        if player.alive:               
            # changing action when running or idle or jumping
            if shoot_b:
                player.shoot_b()
            elif throw_g and not grendade_thrown:
                player.throw_g()
                grendade_thrown = True
                
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1) # 1 = run
            else:
                player.update_action(0) # 0 = idle
        
        #player.movement(moving_left, moving_right)
        pygame.display.update()
    pygame.quit()
            
if __name__ == "__main__": 
    main()