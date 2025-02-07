import pygame
import pickle  # Import for loading level data
from settings import *
from game_world import World
from start_menu import start_screen, end_screen, start_fade
from sound import *

pygame.init()
pygame.display.set_caption("Shooter Game")
FONT = pygame.font.SysFont('Futura', 30)
font = FONT

world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)

def reset():
    # Empty groups
    player_group.empty()
    enemy_group.empty()
    bullet_group.empty()
    grendade_group.empty()
    explosion_group.empty()
    item_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    
    world_list = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_list.append(r)
    return world_list


def main():
    # Run the start menu
    if not start_screen():
        return  # Exit the game if the player quits from the menu
    # Initialize variables
    start_intro = True
    game_over = False
    screen_scroll = 0
    bg_scroll = 0
    moving_right, moving_left, shoot_b, throw_g, grendade_thrown = False, False, False, False, False
    world = World()
    level = 1
    # Load level data
    try:
        with open(f'level{level}_data', 'rb') as pickle_in:
            world_data = pickle.load(pickle_in)
    except FileNotFoundError:
        print(f"Error: Level data file 'level{level}_data' not found!")
        return

    player, healthbar, level_length = world.process_data(world_data)

    while not game_over:
        clock.tick(FPS)

        world.bg(bg_scroll)
        world.draw_world(screen_scroll)

        healthbar.draw(player.health)
        World.display_text('AMMO: ', font, WHITE, 10, 35)  # show ammo
        for x in range(player.s_ammo):
            screen.blit(bullet_image, (85 + (x * 10), 40))
        World.display_text('GRENADE: ', font, WHITE, 10, 65)  # show grenades
        for x in range(player.g_ammo):
            screen.blit(grenade_image, (120 + (x * 15), 68))

        # Update and draw groups
        bullet_group.update(world, screen_scroll)
        bullet_group.draw(screen)
        grendade_group.update(world, screen_scroll)
        grendade_group.draw(screen)
        explosion_group.update(screen_scroll)
        explosion_group.draw(screen)
        item_group.update(screen_scroll)
        item_group.draw(screen)
        decoration_group.draw(screen)
        decoration_group.update(screen_scroll)
        water_group.draw(screen)
        water_group.update(screen_scroll)
        exit_group.draw(screen)
        exit_group.update(screen_scroll)
        
        player.draw()
        player.update()

        for enemy in enemy_group:
            enemy.draw()
            enemy.update()
            enemy.ai(world, screen_scroll, bg_scroll, level_length)

        if start_intro:
            if start_fade.fade():
                start_intro = False
                start_fade.fade_counter = 0
        if player.alive:
            if shoot_b:
                player.shoot_b()
            elif throw_g and not grendade_thrown:
                player.throw_g()
                grendade_thrown = True
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)
            screen_scroll, level_complete = player.movement(moving_left, moving_right, world, screen_scroll, bg_scroll, level_length)
            bg_scroll -= screen_scroll
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset()
                world_data = []
                if level <= MAX_LEVELS:
                    pickle_in = open(f'level{level}_data', 'rb')
                    world_data = pickle.load(pickle_in)
                    world = World()
                    player, healthbar, level_length = world.process_data(world_data)
        else:
            # When player dies, reset the world and reload the level
            screen_scroll = 0

            restart = end_screen()
            if restart:
                start_intro = True
                bg_scroll = 0
                world_data = reset()
                world_data = []
                pickle_in = open(f'level{level}_data', 'rb')
                world_data = pickle.load(pickle_in)
                world = World()
                player, healthbar, level_length = world.process_data(world_data)
            else:
                game_over = True
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_q:
                    shoot_b = True
                if event.key == pygame.K_f:
                    throw_g = True
                if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and player.alive:
                    player.jump = True
                    jump_fx.play()
                if event.key == pygame.K_ESCAPE:
                    game_over = True
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

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
