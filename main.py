import pygame, sys # import pygame and sys

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame

pygame.display.set_caption('UNTITLED PROJECT') # set the window name

WINDOW_SIZE = (600,400) # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

display = pygame.Surface((150, 100))

player_image_r = pygame.image.load('sprites/player.png').convert()
player_image_r.set_colorkey((255, 255, 255))
player_image = player_image_r

player_image_l = pygame.transform.flip(player_image_r, True, False)

grass_image = pygame.image.load('sprites/grass.png')
grass_ind = pygame.image.load('sprites/grass_ind.png').convert()
grass_ind.set_colorkey((255,255,255))
TILE_SIZE = grass_image.get_width()

dirt_image = pygame.image.load('sprites/dirt.png')

background = pygame.image.load('sprites/bg.png')

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')

    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('map')

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def kill(rect):
    rect.x = 50
    rect.y = 70

moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0
true_scroll = [0,0]

player_rect = pygame.Rect(50, 70, player_image_r.get_width(), player_image_r.get_height())

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]


test_rect = pygame.Rect(100,100,100,50)

while True: # game loop
    display.blit(background, (0,0))

    true_scroll[0] += (player_rect.x - true_scroll[0] - 75)/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 50)/20
    scroll = true_scroll.copy()
    scroll[0] = int(true_scroll[0])
    scroll[1] = int(true_scroll[1])

    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(14,222,150),obj_rect)
        else:
            pygame.draw.rect(display,(9,91,85),obj_rect)

    tile_rects = []
    y = 0
    thing = []
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '3':
                display.blit(grass_ind, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '4':
                thing.append(pygame.Rect(x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1], TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(display, (0,0,0), (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1], TILE_SIZE, TILE_SIZE), 1)
            if tile != '0' and tile != '3' and tile != '4':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
                player_image = player_image_r
            if event.key == K_LEFT:
                moving_left = True
                player_image = player_image_l
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    if player_rect.y >= 200:
        kill(player_rect)

    for amount in range(len(thing)):
        if thing[amount].colliderect(player_rect):
            print('woo')

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps
