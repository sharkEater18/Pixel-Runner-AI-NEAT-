# Author: sharkEater_76
# Date: 2021-07-21 20:23:43

import sys

orig_stdin = sys.stdin
orig_stdout = sys.stdout
f_i = open("input.txt", "r")
f_o = open("output.txt", "w")
sys.stdin = f_i
# sys.stdout = f_o

#################################################################################################
"""YOUR CODE GOES HERE, CREATE AN INPUT FILE"""

"""""" """""" """""
LIBRARIES
""" """""" """""" ""
####################################################################################
import pygame
import sys
import os
import random
import math
import neat

####################################################################################


####################################################################################
pygame.init()
clock = pygame.time.Clock()
####################################################################################


"""""" """""" """""
CONSTANT VARIABLES
""" """""" """""" ""
####################################################################################
HEIGHT = 400
WIDTH = 800
FONT = pygame.font.Font("freesansbold.ttf", 20)
Y_POS = 300  # Position where the player stands, sky-ground intersection point
####################################################################################


"""""" """""" """""
BACKGROUND
""" """""" """""" ""
####################################################################################
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PIXEL RUNNER AI")
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
####################################################################################


"""""" """""" """""
AUDIO SECTION
""" """""" """""" ""
####################################################################################
# Game Over Sound
over_sound = pygame.mixer.Sound("audio/exp.wav")
over_sound.set_volume(0.37)

# Bg sound
bg_sound = pygame.mixer.Sound("audio/bg.mp3")
bg_sound.set_volume(0.2)
bg_sound.play(loops=-1)
####################################################################################

"""""" """""" """""
PLAYER SECTION
""" """""" """""" ""
####################################################################################
# Player Class
class Player(pygame.sprite.Sprite):
    X_POS = 80
    Y_POS = 300
    # Constructor
    def __init__(self):
        # Inherit from the Sprite Class
        super().__init__()

        self.jumping = False
        self.running = True
        self.player_gravity = 0
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.33)

        # Import Images for the player
        player_walk1 = pygame.image.load(
            "graphics/player/player_walk_1.png"
        ).convert_alpha()

        player_walk2 = pygame.image.load(
            "graphics/player/player_walk_2.png"
        ).convert_alpha()

        # Jumping Frame
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.player_walk_list = [player_walk1, player_walk2]
        self.player_walk_id = 0

        self.image = self.player_walk_list[self.player_walk_id]
        self.rect = self.image.get_rect(midbottom=(self.X_POS, self.Y_POS))

    # Draw Method
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(
            screen,
            self.color,
            (self.rect.x, self.rect.y, self.rect.width, self.rect.height),
            2,
        )
        # screen.blit(self.image, self.rect)

    # Jump method
    def jump(self):
        # Initially gravity in "downwards" +(ve)
        self.player_gravity += 1
        self.rect.y += self.player_gravity
        if self.rect.bottom > self.Y_POS:
            self.rect.bottom = self.Y_POS

        # On Jump a strong gravity acts "upwards" -(ve)
        # Jump Implementation wrt to the AI
        if self.jumping and self.rect.bottom == self.Y_POS:
            # print("JUMP")
            self.player_gravity = -20
            self.jumping = False
            self.jump_sound.play()

        # For Jump Test Only
        # key = pygame.key.get_pressed()
        # if key[pygame.K_SPACE] and self.rect.bottom == self.Y_POS:
        #     self.player_gravity = -20
        #     print("JUMP")
        #     self.jump_sound.play()

    # Animate diff frames
    def animate(self):
        # Jump
        if self.rect.bottom < self.Y_POS:
            self.image = self.player_jump

        # Walk
        else:
            self.player_walk_id += 0.1
            if self.player_walk_id >= 2:
                self.player_walk_id = 0
            self.image = self.player_walk_list[int(self.player_walk_id)]

    # Visualization (Drawing rectangles and Lines to the enemies)
    def visualize(self, screen):
        for enemy in enemies:
            pygame.draw.line(
                screen,
                self.color,
                (self.rect.x + 54, self.rect.y + 12),
                enemy.rect.center,
                2,
            )

    # Update the methods
    def update(self):
        self.draw(screen)
        self.jump()
        self.animate()
        self.visualize(screen)


####################################################################################

"""""" """""" """""
ENEMY(s) SECTION
""" """""" """""" ""
####################################################################################
class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        # Snail
        snail_y_pos = Y_POS
        snail_speed = 10

        # Fly
        fly_y_pos = Y_POS - 50
        fly_speed = 5

        # Inherit the Sprite Class
        super().__init__()

        # Snail
        if type == "snail":
            snail1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()

            self.enemy_frame_list = [snail1, snail2]
            self.enemy_y_pos = snail_y_pos
            self.enemy_speed = snail_speed

        # Fly
        elif type == "fly":
            fly1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()

            self.enemy_frame_list = [fly1, fly2]
            self.enemy_y_pos = fly_y_pos
            self.enemy_speed = fly_speed

        # Randomly Place the enemy
        self.enemy_x_pos = random.randint(900, 1100)
        self.enemy_frame_id = 0
        self.image = self.enemy_frame_list[self.enemy_frame_id]
        self.rect = self.image.get_rect(midbottom=(self.enemy_x_pos, self.enemy_y_pos))

    # Movement method
    def moevment(self):
        # Move enemy to the left
        self.enemy_speed = game_speed - self.enemy_speed
        self.rect.x -= self.enemy_speed

        # Destroy the enemies leaving the arena
        if self.rect.right <= -100:
            enemies.pop()
            self.kill()

    # Animate the frames
    def animate(self):
        self.enemy_frame_id += 0.1
        if self.enemy_frame_id >= 2:
            self.enemy_frame_id = 0
        self.image = self.enemy_frame_list[int(self.enemy_frame_id)]

    # Draw method
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.moevment()
        self.animate()
        self.draw(screen)


####################################################################################

"""""" """""" """""
Helper Functions
""" """""" """""" ""
####################################################################################
# Remove players
def remove(index):
    players.pop(index)
    ge.pop(index)
    nets.pop(index)


# Euclidian Dist
def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx ** 2 + dy ** 2)


####################################################################################


"""""" """""" """""
MAIN GAME SECTION
""" """""" """""" ""
####################################################################################
max_points = 0


def eval_genomes(genomes, config):
    """
    runs the simulation of the current population of
    players and sets their fitness based on the distance they
    reach in the game.
    """
    global game_speed, players, enemies, ge, nets, points, max_points
    clock = pygame.time.Clock()
    points = 0

    # Player List (Genomes)
    players = []

    # Enemies List
    enemies = []

    # Genome List
    ge = []
    # Neural net asscocaited with the genome
    nets = []

    game_speed = 15

    for genome_id, genome in genomes:
        player = Player()
        players.append(player)

        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def score():
        global points, game_speed, max_points
        points += 1

        # Increment the game speed
        if int(points) % 100 == 0:
            game_speed += 1
            if (game_speed) > 33:
                game_speed = 33  # "33" seem to be the threshold for our player
            game_speed %= 34

        # Max Points
        max_points = max(max_points, points)
        text1 = FONT.render(f"Points:  {str(int(points))}", True, (0, 0, 0))
        text2 = FONT.render(f"Max Points:  {str(int(max_points))}", True, (0, 0, 0))

        # Score
        score_rect = text1.get_rect(midtop=(400, 20))
        max_score_rect = text2.get_rect(midtop=(400, 50))

        screen.blit(text1, score_rect)
        screen.blit(text2, max_score_rect)

    def statistics():
        global players, game_speed, ge
        text_1 = FONT.render(f"Alive:  {str(len(players))}", True, (0, 0, 0))
        text_2 = FONT.render(f"Gen:  {pop.generation+1}", True, (0, 0, 0))
        text_3 = FONT.render(f"Speed:  {str(game_speed)}", True, (0, 0, 0))

        screen.blit(text_1, (50, 350))
        screen.blit(text_2, (600, 20))
        screen.blit(text_3, (600, 50))

    # Main game loop
    print("GAME START")
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            # Game Quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Max Points", max_points)
                print("GAME CLOSED")
                sys.exit()

        # Draw the background
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, Y_POS))

        """""" """""" """""
        For Player
        """ """""" """""" ""
        # Draw all the players
        for player in players:
            player.draw(screen)
            player.update()

        # Game Over Condition (when all genomes perishes)
        if len(players) == 0:
            print("GAME OVER")
            over_sound.play()
            break

        """""" """""" """""
        For Enemies
        """ """""" """""" ""
        # Append enemies
        if len(enemies) == 0:
            choice_enemy = random.choice(
                ["snail", "fly", "fly", "snail", "snail", "snail"]
            )
            print("-----------------" + choice_enemy.upper())
            enemies.append(Enemy(choice_enemy))

        # Update and Collision check with the players
        for enemy in enemies:
            enemy.update()
            for i, player in enumerate(players):
                if player.rect.colliderect(enemy.rect):
                    # Decrease the fitness of the player on collision
                    ge[i].fitness -= 5
                    remove(i)
                else:
                    ge[i].fitness += 1.3

        for i, player in enumerate(players):
            for enemy in enemies:
                # Get the activation function from the nn
                # Two input params are given viz: 
                # 1) Player Vertical Direction, 2) Euclidean distance b/w player and enemy
                output = nets[i].activate(
                    (
                        player.rect.y,
                        distance((player.rect.x, player.rect.y), enemy.rect.midtop),
                    )
                )
                # Jumping condition, activation function = tanh, range = [-1, 1]
                # print(output) # To determine jumping condition 
                if output[0] > 0.0 and player.rect.bottom == player.Y_POS:
                    player.jumping = True
                    player.jump()

        score()
        statistics()
        pygame.display.update()

        # Refresh hertz
        clock.tick(40)


####################################################################################


"""""" """""" """""
NEAT AI IMPLEMENT 
AND CONFIGURE
""" """""" """""" ""
####################################################################################
# Setup the NEAT Neural Network
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    # Set the population according to the config file
    pop = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    # Eval for 50 generations
    best = pop.run(eval_genomes, 50)

    # show final stats
    print("\nBest genome:\n{!s}".format(best))

    # # TODO
    # visualize.draw_net(config_path, ge)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
####################################################################################


####################################################################################
print(max_points)
print("GAME CRASHED")
# assert False
####################################################################################

####################################################################################################
sys.stdin = orig_stdin
sys.stdout = orig_stdout
f_i.close()
f_o.close()
