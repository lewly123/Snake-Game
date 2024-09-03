import pygame
import random
import sys
import os

# Change working directory to the assets directory
os.chdir("C:/Users/Darren Lew/Desktop/Workshop/assets")

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

# Font
font = pygame.font.SysFont(None, 55)
score_font = pygame.font.SysFont("consolas", 20)

# Game Variables
snake_color = green
snake_head_img = pygame.image.load("spaceship.png")  # Placeholder path
snake_head_img = pygame.transform.scale(snake_head_img, (40, 40))
map_choice = 1  # Default map
score = 0
BLOCK_SIZE = 20
snake_pos = [[width // 2, height // 2]]
snake_speed = [0, BLOCK_SIZE]
food_pos = [0, 0]
teleport_walls = True  # Set this to True to enable wall teleporting
clock = pygame.time.Clock()

def display_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, [x, y])

def generate_food():
    while True:
        x = random.randint(0, (width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food_pos = [x, y]
        if food_pos not in snake_pos:
            return food_pos

def draw_objects():
    window.fill(black)
    for pos in snake_pos:
        pygame.draw.rect(window, snake_color, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(window, red, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
    # Render the score
    score_text = score_font.render(f"Score: {score}", True, white)
    window.blit(score_text, (10, 10))

def update_snake():
    global food_pos, score
    new_head = [snake_pos[0][0] + snake_speed[0], snake_pos[0][1] + snake_speed[1]]
    
    if teleport_walls:
        # if the new head position is outside of the screen, wrap it to the other side
        if new_head[0] >= width:
            new_head[0] = 0
        elif new_head[0] < 0:
            new_head[0] = width - BLOCK_SIZE
        if new_head[1] >= height:
            new_head[1] = 0
        elif new_head[1] < 0:
            new_head[1] = height - BLOCK_SIZE
    if new_head == food_pos:
        food_pos = generate_food()  # generate new food
        score += 1  # increment score when food is eaten
    else:
        snake_pos.pop()  # remove the last element from the snake
    
    snake_pos.insert(0, new_head)  # add the new head to the snake

def game_over():
    # game over when snake hits the boundaries or runs into itself
    if teleport_walls:
        return snake_pos[0] in snake_pos[1:]
    else:
        return snake_pos[0] in snake_pos[1:] or \
            snake_pos[0][0] > width - BLOCK_SIZE or \
            snake_pos[0][0] < 0 or \
            snake_pos[0][1] > height - BLOCK_SIZE or \
            snake_pos[0][1] < 0

def game_over_screen():
    global score
    window.fill(black)
    game_over_font = pygame.font.SysFont("consolas", 50)
    game_over_text = game_over_font.render(f"Game Over! Score: {score}", True, white)
    window.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run()  # replay the game
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()  # quit the game
                    return

def run():
    global snake_speed, snake_pos, food_pos, score
    snake_pos = [[width // 2, height // 2]]
    snake_speed = [0, BLOCK_SIZE]
    food_pos = generate_food()
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if snake_speed[1] == BLOCK_SIZE:
                    continue
                snake_speed = [0, -BLOCK_SIZE]
            if keys[pygame.K_DOWN]:
                if snake_speed[1] == -BLOCK_SIZE:
                    continue
                snake_speed = [0, BLOCK_SIZE]
            if keys[pygame.K_LEFT]:
                if snake_speed[0] == BLOCK_SIZE:
                    continue
                snake_speed = [-BLOCK_SIZE, 0]
            if keys[pygame.K_RIGHT]:
                if snake_speed[0] == -BLOCK_SIZE:
                    continue
                snake_speed = [BLOCK_SIZE, 0]
        if game_over():
            game_over_screen()
            return
        update_snake()
        draw_objects()
        pygame.display.update()
        clock.tick(15)  # limit the frame rate to 15 FPS

def main_menu():
    while True:
        window.fill(black)
        display_text("Snake Game", white, 300, 100)
        display_text("Play", white, 350, 200)
        display_text("Quit", white, 350, 300)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 350 <= event.pos[0] <= 450:
                    if 200 <= event.pos[1] <= 250:
                        run()
                    if 300 <= event.pos[1] <= 350:
                        pygame.quit()
                        sys.exit()

# Run the game
main_menu()
