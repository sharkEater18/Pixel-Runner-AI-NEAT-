import pygame
import sys
from random import randint

pygame.init()
clock = pygame.time.Clock()


HEIGHT = 400
WIDTH = 800
FONT = pygame.font.Font("font/Pixeltype.ttf", 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("RUN FOR YOUR LIFE")

sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()


"""
Create Player
"""
player_surface1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_surface2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()

player_rect = player_surface1.get_rect(midbottom=(80, 300))

# Gravity
player_gravity_x, player_gravity_y = 0, 0

"""
Enemies
"""
enemy_rect_list = []

# Snail
snail_surface1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_surface2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_x_pos, snail_y_pos = 600, 255
snail_speed = 6.5

# Fly
fly_surface1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_surface2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_x_pos, fly_y_pos = 1000, 400
fly_speed = 6.5

# Timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

# Movement & Collision Function
def enemy_movement(enemies):
    if not enemies:
        return []

    # Move the all enemies to the left
    for enemy_rect in enemies:
        # Snail
        if enemy_rect.bottom == 300:
            enemy_rect.x -= snail_speed
            screen.blit(snail_surface1, enemy_rect)

        # Fly
        else:
            enemy_rect.x -= fly_speed
            screen.blit(fly_surface1, enemy_rect)

    # Boundary Collision
    enemies = [enemy for enemy in enemies if enemy.left >= -100]

    return enemies


"""
Enemy-Player Collision
"""

# Return true and game over
def is_collision(player, enemy_rect_list):
    for enemy_rect in enemy_rect_list:
        if player.colliderect(enemy_rect):
            # Reset all the enemies
            enemy_rect_list.clear()

            print("GAME OVER")
            return True
    return False


"""
Score Section
"""
# Score is based on time
start_time = pygame.time.get_ticks()


def update_score():
    score = (pygame.time.get_ticks() - start_time) // 500
    score_surface = FONT.render("Score: " + str(score), False, "black")
    score_rect = score_surface.get_rect(midtop=(400, 20))
    # Update the score
    screen.blit(score_surface, score_rect)
    return score


"""
Intro-Outro Screen
"""
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name_surface = FONT.render("Pixel Runner", False, "#38f2e9")
game_name_rect = game_name_surface.get_rect(midtop=(400, 40))

game_message_surface = FONT.render("Press SPACE to Run", False, "#38f2e9")
game_message_rect = game_message_surface.get_rect(midtop=(400, 320))


"""
Main Game Loop
"""
scr = -1
game_over = True
while True:
    for event in pygame.event.get():
        # Game Quit event
        if event.type == pygame.QUIT:
            game_over = True
            pygame.quit()
            score = 0
            print("GAME CLOSED")
            sys.exit()

        # Player jumps on pressing 'space' or starts the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Start the game
                if game_over:
                    start_time = pygame.time.get_ticks()
                    game_over = False
                    print("GAME START")

                # Jump
                if player_rect.bottom >= 300:
                    player_gravity_y = -20
                    print("JUMP")

        # Append enemy to the list
        if event.type == enemy_timer and not game_over:
            range_x = randint(900, 1100)
            choice_enemy = randint(0, 1)
            if choice_enemy:
                enemy_rect_list.append(
                    snail_surface1.get_rect(bottomright=(range_x, 300))
                )
            else:
                enemy_rect_list.append(
                    fly_surface1.get_rect(bottomright=(range_x, 190))
                )

    if not game_over:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        scr = update_score()

        """
        For Player
        """
        # Implement gravity
        player_gravity_y += 1
        player_rect.y += player_gravity_y
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface1, player_rect)

        """
        For Enemy(s)
        """
        enemy_rect_list = enemy_movement(enemy_rect_list)

        """
        Player-Enemy Collision
        """
        game_over = is_collision(player_rect, enemy_rect_list)

    """
    GAME OVER
    """
    if game_over:
        # Clear the enemy list
        enemy_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity_y = 0

        score = 0
        screen.fill("#15768a")  # Teal color
        # Game over screen
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name_surface, game_name_rect)

        if scr != -1:
            score_surface = FONT.render("Your Score: " + str(scr), False, "#38f2e9")
            score_rect = game_name_surface.get_rect(midtop=(400, 300))
            screen.blit(score_surface, score_rect)

        else:
            screen.blit(game_message_surface, game_message_rect)

    pygame.display.update()
    clock.tick(60)

assert False
