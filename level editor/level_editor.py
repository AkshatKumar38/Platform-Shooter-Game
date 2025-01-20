import pygame
import button
import pickle

pygame.init()
FPS = 60
clock = pygame.time.Clock()

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300  

# colours
WHITE = (255, 255, 255)
GREEN = (144, 201, 120)
RED = (200, 25, 25)

# game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21


font = pygame.font.SysFont('Futura', 30)
# create world 
world_list = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_list.append(r)

# create ground
for tile in range(0, MAX_COLS):
    world_list[ROWS - 1][tile] = 0

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

# background images
pine1_img = pygame.image.load('assets/images/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('assets/images/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('assets/images/background/mountain.png').convert_alpha()
sky_cloud_img = pygame.image.load('assets/images/background/sky_cloud.png').convert_alpha()

# tile images
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'assets/images/tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE,TILE_SIZE))
    img_list.append(img)
# tile button
button_list = []
button_row = 0
button_col = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

save_level_img = pygame.image.load('assets/images/buttons/save_btn.png').convert_alpha()
load_level_img = pygame.image.load('assets/images/buttons/load_btn.png').convert_alpha()
# fn to set bg
def bg(scroll):
    screen.fill(GREEN)
    width  = sky_cloud_img.get_width()
    for x in range(4):
        screen.blit(sky_cloud_img, ((x * width) - scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - scroll *0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height() ))

def draw_grid(scroll):
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT )) # vertical lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE ))

def draw_world():
    for y, row in enumerate(world_list):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE, y * TILE_SIZE))

def draw_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    screen.blit(img, (x, y))

def main():
    run = True
    
    # game variables
    scroll_left = False
    scroll_right = False
    scroll = 0
    scroll_speed = 1
    current_tile = 0
    level = 0
    global world_list
    
    # save and load buttons
    save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50,save_level_img, 1)
    load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50,load_level_img, 1)
    while run:
        clock.tick(FPS)
        bg(scroll)
        draw_grid(scroll)
        draw_world()
        
        # draw buttons
        if save_button.draw(screen):
            # save level date in csv
            pickle_out = open(f'level{level}_data', 'wb')
            pickle.dump(world_list, pickle_out)
            pickle_out.close()
                
        if load_button.draw(screen):
            scroll = 0
            world_list = []
            pickle_in = open(f'level{level}_data', 'rb')
            world_list = pickle.load(pickle_in)
                    
        
        draw_text(f'Level: {level}',font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
        draw_text('Press UP or DOWN to change the level',font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
        button_count = 0
        for button_count,i in enumerate(button_list):
            if i.draw(screen):
                current_tile = button_count
        # hishlight current button selected
        pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)
        
        # scroll control
        if scroll_left and scroll > 0:
            scroll -= 5 * scroll_speed
            if scroll < 0:
                scroll = 0
        if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
            scroll += 5 * scroll_speed
            if scroll > (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
                scroll = (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH
        
        # get mouse pos
        pos = pygame.mouse.get_pos()
        x = (pos[0] + scroll) // TILE_SIZE
        y = pos[1] // TILE_SIZE
        
        # check ony if mouse in tile area
        if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:
                if world_list[y][x] != current_tile:
                    world_list[y][x] = current_tile
            if pygame.mouse.get_pressed()[2] == 1:
                world_list[y][x] = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit game
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    level += 1
                if event.key == pygame.K_DOWN and level > 0:
                    level -= 1
                if event.key == pygame.K_LEFT:
                    scroll_left = True
                if event.key == pygame.K_RIGHT:
                    scroll_right = True
                if event.key == pygame.K_RSHIFT:
                    scroll_speed = 5
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    scroll_left = False
                if event.key == pygame.K_RIGHT:
                    scroll_right = False
                if event.key == pygame.K_RSHIFT:
                    scroll_speed = 1
                
        
        pygame.display.update()
    pygame.quit()
    
    
if __name__ == '__main__':
    main()
