import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the player
PLAYER_SIZE = 50
player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
player_y = SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2
player_speed = 5

# Define the enemy
ENEMY_SIZE = 50
enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
enemy_speed_x = random.randint(-5, 5)
enemy_speed_y = random.randint(-5, 5)

# Define the game state
GAME_STATE_TITLE = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2
current_game_state = GAME_STATE_TITLE

# Define the font
font = pygame.font.Font(None, 36)

def handle_events():
    """
    Handles user input events.
    """
    global current_game_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_game_state == GAME_STATE_TITLE:
                handle_title_screen_click(event.pos, enemy_speed_x, enemy_speed_y)
            elif current_game_state == GAME_STATE_GAME_OVER:
                handle_game_over_screen_click(event.pos)

def handle_title_screen_click(position, enemy_speed_x, enemy_speed_y):
    """
    Handles mouse clicks on the title screen.
    """
    global current_game_state, player_x, player_y, enemy_x, enemy_y

    new_game_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50, 150, 50)
    quit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, 100, 50)

    if new_game_rect.collidepoint(position):
        player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
        player_y = SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        current_game_state = GAME_STATE_PLAYING
    elif quit_rect.collidepoint(position):
        pygame.quit()
        sys.exit()

def handle_game_over_screen_click(position):
    """
    Handles mouse clicks on the game over screen.
    """
    global current_game_state

    restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)

    if restart_rect.collidepoint(position):
        current_game_state = GAME_STATE_TITLE

def update_game_state():
    """
    Updates the game state.
    """
    global current_game_state, player_x, player_y, enemy_x, enemy_y, enemy_speed_x, enemy_speed_y

    if current_game_state == GAME_STATE_PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_SIZE:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - PLAYER_SIZE:
            player_y += player_speed

        enemy_x += enemy_speed_x
        enemy_y += enemy_speed_y

        if (
            player_x + PLAYER_SIZE > enemy_x
            and player_x < enemy_x + ENEMY_SIZE
            and player_y + PLAYER_SIZE > enemy_y
            and player_y < enemy_y + ENEMY_SIZE
        ):
            current_game_state = GAME_STATE_GAME_OVER

        if enemy_x <= 0 or enemy_x >= SCREEN_WIDTH - ENEMY_SIZE:
            enemy_speed_x *= -1
        if enemy_y <= 0 or enemy_y >= SCREEN_HEIGHT - ENEMY_SIZE:
            enemy_speed_y *= -1

def draw_game_objects():
    """
    Draws the game objects on the screen.
    """
    global current_game_state

    screen.fill(BLACK)

    if current_game_state == GAME_STATE_TITLE:
        title_text = font.render("Simple Game", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)

        new_game_text = font.render("New Game", True, WHITE)
        new_game_rect = new_game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.draw.rect(screen, BLACK, new_game_rect)

        screen.blit(new_game_text, new_game_rect)

        quit_text = font.render("Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        pygame.draw.rect(screen, BLACK, quit_rect)
        screen.blit(quit_text, quit_rect)

    elif current_game_state == GAME_STATE_PLAYING:
        pygame.draw.rect(screen, WHITE, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
        pygame.draw.rect(screen, RED, (enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE))

    elif current_game_state == GAME_STATE_GAME_OVER:
        game_over_text = font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        restart_text = font.render("Click to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.draw.rect(screen, BLACK, restart_rect)
        screen.blit(restart_text, restart_rect)

running = True
clock = pygame.time.Clock()

while running:
    handle_events()
    update_game_state()
    draw_game_objects()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()