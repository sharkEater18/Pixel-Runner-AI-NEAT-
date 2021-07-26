import pygame
import sys
from random import choice, randint


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


class Player(pygame.sprite.Sprite):
    # Constructor
    def __init__(self):
        # Inherit from the Sprite Class
        super().__init__()

        # Import Images for the player
        player_walk1 = pygame.image.load(
            "graphics/player/player_walk_1.png"
        ).convert_alpha()
        player_walk2 = pygame.image.load(
            "graphics/player/player_walk_2.png"
        ).convert_alpha()
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.player_walk_list = [player_walk1, player_walk2]
        self.player_walk_id = 0
        self.player_surface = self.player_walk_list[self.player_walk_id]

        self.image = self.player_walk_list[self.player_walk_id]
        self.rect = self.image.get_rect(midbottom=(100, 300))

        self.player_gravity = 0
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.33)

    # Jump method
    def jump(self):
        # Initially gravity in "downwards" +(ve)
        self.player_gravity += 1
        self.rect.y += self.player_gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300

        # On Jump a strong gravity acts "upwards" -(ve)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.rect.bottom == 300:
            print("JUMP")
            self.jump_sound.play()
            self.player_gravity = -20

    # Animate diff frames
    def animate(self):
        # Jump
        if self.rect.bottom < 300:
            self.image = self.player_jump

        # Walk
        else:
            self.player_walk_id += 0.1
            if self.player_walk_id >= 2:
                self.player_walk_id = 0
            self.image = self.player_walk_list[int(self.player_walk_id)]

    # Update the methods
    def update(self):
        self.jump()
        self.animate()


# Instantiate the player class
player = pygame.sprite.GroupSingle()
player.add(Player())


a = player.sprite.rect.left
print(a)

"""
Enemies
"""


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        # Snail Parameters
        snail_x_pos, snail_y_pos = 600, 300
        snail_speed = 6.5

        # Fly Parameters
        fly_x_pos, fly_y_pos = 1000, 190
        fly_speed = 6.5

        # Inherit the Sprite Class
        super().__init__()

        # Snail
        if type == "snail":
            snail_walk1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_walk2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()

            self.enemy_frame_list = [snail_walk1, snail_walk2]
            self.enemy_y_pos = snail_y_pos
            self.enemy_speed = snail_speed

        # Fly
        elif type == "fly":
            fly_walk1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_walk2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()

            self.enemy_frame_list = [fly_walk1, fly_walk2]
            self.enemy_y_pos = fly_y_pos
            self.enemy_speed = fly_speed

        # Randomly Place the enemy
        self.enemy_x_pos = randint(900, 1100)
        self.enemy_frame_id = 0
        self.image = self.enemy_frame_list[self.enemy_frame_id]
        self.rect = self.image.get_rect(midbottom=(self.enemy_x_pos, self.enemy_y_pos))

    def moevment(self):
        # Move enemy to the left
        self.rect.x -= self.enemy_speed

        # Destroy the enemies leaning the arena
        if self.rect.right <= -100:
            self.kill()

    def animate(self):
        self.enemy_frame_id += 0.1
        if self.enemy_frame_id >= 2:
            self.enemy_frame_id = 0
        self.image = self.enemy_frame_list[int(self.enemy_frame_id)]

    def update(self):
        self.moevment()
        self.animate()


# Instantiate the enemy class
enemy = pygame.sprite.Group()

# Timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)


"""
Enemy-Player Collision
"""

# Return true and game over
def is_collision():
    if pygame.sprite.spritecollide(player.sprite, enemy, True, collided=None):
        enemy.empty()
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
Audio
"""

over_sound = pygame.mixer.Sound("audio/exp.wav")
over_sound.set_volume(0.37)


bg_sound = pygame.mixer.Sound("audio/music.wav")
bg_sound.set_volume(0.2)
bg_sound.play(loops = -1)


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

        # Append enemy to the class
        if event.type == enemy_timer and not game_over:
            choice_enemy = choice(["snail", "fly"])
            print("-----------------" + choice_enemy.upper())
            enemy.add(Enemy(choice_enemy))

        # Space starts the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Start the game
                if game_over:
                    start_time = pygame.time.get_ticks()
                    game_over = False
                    print("GAME START")

    if not game_over:
        # Draw the Background(s)
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # Update the score
        scr = update_score()

        """
        For Player
        """

        player.draw(screen)
        player.update()

        """
        For Enemy(s)
        """

        enemy.draw(screen)
        enemy.update()

        """
        Player-Enemy Collision
        """
        game_over = is_collision()

        if game_over:
            print("GAME OVER")
            over_sound.play()


    """
    GAME OVER
    """
    if game_over:

        # Game over screen
        screen.fill("#15768a")  # Teal color
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name_surface, game_name_rect)

        if scr != -1:
            score_surface = FONT.render("Your Score: " + str(scr), False, "#38f2e9")
            score_rect = game_name_surface.get_rect(midtop=(400, 300))
            screen.blit(score_surface, score_rect)

        else:
            screen.blit(game_message_surface, game_message_rect)

    pygame.display.update()

    # Refresh hertz
    clock.tick(60)


assert False
