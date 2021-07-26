import pygame
import sys

pygame.init()

HEIGHT = 400
WIDTH = 800
FONT = pygame.font.Font("font/Pixeltype.ttf", 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("RUN FOR YOUR LIFE")
clock = pygame.time.Clock()

sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

"""
Create the snail (enemy)
"""
snail_surface1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
# snail_surface2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_x_pos, snail_y_pos = 600, 255
snail_speed = 6.5
snail_rect = snail_surface1.get_rect(midbottom=(snail_x_pos, 300))


"""
Fly Enemy
"""
fly_surface1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
# snail_surface2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
fly_x_pos, fly_y_pos = 1000, 400
fly_speed = 6.5
fly_rect = fly_surface1.get_rect(midbottom=(fly_x_pos, 300 - 90))


"""
Create Player
"""
player_surface1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surface1.get_rect(midbottom=(80, 300))

# player_surface2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
# Gravity
player_gravity_x, player_gravity_y = 0, 0


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
Intro Screen
"""
text_surface = FONT.render("Press SPACE To Start", False, "black")
text_rect = text_surface.get_rect(midtop=(400, 20))


"""
Outro Screen
"""
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
# player_stand = pygame.transform.scale(player_stand, (200, 100))
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name_surface = FONT.render("Pixel Runner", False, "#38f2e9")
game_name_rect = game_name_surface.get_rect(midtop=(400, 40))

game_message_surface = FONT.render("Press SPACE to Run", False, "#38f2e9")
game_message_rect = game_message_surface.get_rect(midtop=(400, 320))

scr = -1
game_over = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            pygame.quit()
            score = 0
            print("GAME CLOSED")
            sys.exit()

        # Player jumps on pressing 'space' or starts the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    start_time = pygame.time.get_ticks()
                    game_over = False
                    snail_rect.left = 800
                    fly_rect.left = 1100

                if player_rect.bottom >= 300:
                    player_gravity_y = -20
                    print("JUMP")

    if not game_over:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        scr = update_score()

        """
        For Snail
        """
        snail_rect.x -= snail_speed
        # Collision check with the border
        if snail_rect.right < -100:
            snail_rect.left = 800
        screen.blit(snail_surface1, snail_rect)

        """
        For Fly
        """
        fly_rect.x -= fly_speed
        # Collision check with the border
        if fly_rect.right < -100:
            fly_rect.left = 1000
        screen.blit(fly_surface1, fly_rect)

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
        Player-Enemy Collision
        """
        if player_rect.colliderect(snail_rect) or player_rect.colliderect(fly_rect):
            print("GAME OVER")
            game_over = True

        """
        Mouse/ Cheats
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicks = list(pygame.mouse.get_pressed())
        left_click, mid_click, right_click = (
            mouse_clicks[0],
            mouse_clicks[1],
            mouse_clicks[2],
        )

        if snail_rect.collidepoint(mouse_pos) and left_click:
            snail_rect.left = 800
            print("Hello, from Snail!")

        if player_rect.collidepoint(mouse_pos) and left_click:
            print("Hello, from Player!")

        if fly_rect.collidepoint(mouse_pos) and left_click:
            fly_rect.left = 1000
            print("Hello, from Fly!")

    """
    GAME OVER
    """
    if game_over:
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
