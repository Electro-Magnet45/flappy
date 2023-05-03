import pygame
import random
import sys

# set up pygame
pygame.init()

# set up the display
screen_width = 288
screen_height = 512
font = pygame.font.Font('04B_19.ttf', 20)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# set up game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# set up game objects
background = pygame.image.load('background.png').convert()
floor = pygame.image.load('base.png').convert()
floor_x = 0

bird = pygame.image.load('bird.png').convert()
bird_rect = bird.get_rect(center=(50, screen_height / 2))


floor_width = floor.get_width()
num_floor_tiles = screen_width // floor_width + 2
floor_surface = pygame.Surface(
    (floor_width * num_floor_tiles, floor.get_height()))
for i in range(num_floor_tiles):
    floor_surface.blit(floor, (i * floor_width, 0))

pipe_surface = pygame.image.load('pipe.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_heights = [200, 250, 300, 350]

# set up game functions


def create_pipe():
    random_pipe_pos = random.choice(pipe_heights)
    bottom_pipe = pipe_surface.get_rect(
        midtop=(screen_width + 100, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(
        screen_width + 100, random_pipe_pos - 150))
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_height - 100:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    global game_active, score, high_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            game_active = False
            if score > high_score:
                high_score = score
            score = 0

    if bird_rect.top <= -50 or bird_rect.bottom >= screen_height - 100:
        game_active = False
        if score > high_score:
            high_score = score
        score = 0


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_width / 2, 50))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        score_surface = font.render(
            f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_width / 2, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = font.render(
            f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(
            center=(screen_width / 2, 425))
        screen.blit(high_score_surface, high_score_rect)


clock = pygame.time.Clock()

# set up bird animation
bird_downflap = pygame.transform.scale2x(pygame.image.load(
    'bird.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(
    'bird.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(
    'bird.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, screen_height / 2))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


def draw_floor():
    global floor_x
    screen.blit(floor_surface, (floor_x, 450))
    screen.blit(floor_surface, (floor_x + floor_surface.get_width(), 450))
    floor_x -= 1
    if floor_x <= -floor_width:
        floor_x = 0


# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, screen_height / 2)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(background, (0, 0))

    if game_active:
        # bird movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += int(bird_movement)
        screen.blit(rotated_bird, bird_rect)

        # pipe movement
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # score
        score += 0.01
        score_display('main_game')
        check_collision(pipe_list)

    else:
        screen.blit(font.render("Press SPACE to start",
                    True, (255, 255, 255)), (65, 250))
        score_display('game_over')

    # floor movement
    floor_x -= 1
    draw_floor()
    if floor_x <= -screen_width:
        floor_x = 0

    pygame.display.update()
    clock.tick(60)
