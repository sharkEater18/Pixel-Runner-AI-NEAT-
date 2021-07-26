import pygame
import os
import random
import math
import sys
import neat


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
    def __init__(self, pos=100):
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

        self.image = self.player_walk_list[self.player_walk_id]
        self.rect = self.image.get_rect(midbottom=(pos, 300))

        self.player_gravity = 0
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.33)

        self.jumping = False

        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    # Jump method
    def jump(self):
        # Initially gravity in "downwards" +(ve)
        self.player_gravity += 1
        self.rect.y += self.player_gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300

        # On Jump a strong gravity acts "upwards" -(ve)
        # Jump Implementation wrt to the AI
        if self.jumping and self.rect.bottom >= 300:
            self.jumping = False
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

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(
            screen,
            self.color,
            (self.rect.x, self.rect.y, self.rect.width, self.rect.height),
            2,
        )
        for obstacle in enemy_group:
            pygame.draw.line(
                screen,
                self.color,
                (self.rect.x + 54, self.rect.y + 12),
                obstacle.rect.center,
                2,
            )

    # Update the methods
    def update(self):
        self.jump()
        self.animate()
        self.draw(screen)


# Instantiate the player class
# player = pygame.sprite.GroupSingle()
# player.add(Player())

# genes = 2
# players = []


# def add_players():
#     global players
#     for i in range(genes):
#         player = pygame.sprite.GroupSingle()
#         player.add(Player(100 + i * 100))
#         players.append(player)


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
        self.enemy_x_pos = random.randint(900, 1100)
        self.enemy_frame_id = 0
        self.image = self.enemy_frame_list[self.enemy_frame_id]
        self.rect = self.image.get_rect(midbottom=(self.enemy_x_pos, self.enemy_y_pos))

    def moevment(self):
        # Move enemy to the left
        self.enemy_speed += 0.1
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
enemy_group = pygame.sprite.Group()

# Timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)




"""
Audio
"""

over_sound = pygame.mixer.Sound("audio/exp.wav")
over_sound.set_volume(0.37)


bg_sound = pygame.mixer.Sound("audio/music.wav")
bg_sound.set_volume(0.2)
bg_sound.play(loops=-1)


"""
Main Game Loop
"""


def remove(index):
    players.pop(index)
    ge.pop(index)
    nets.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx ** 2 + dy ** 2)



def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, enemies, players, ge, nets, points
    clock = pygame.time.Clock()
    points = 0

    # obstacles = enemy_group
    # players = players
    
    players = []
    ge = []
    nets = []

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20
    


    # genes = 2
    # players = []
    # def add_players():
    #     global players
    #     for i in range(genes):
    #         player = pygame.sprite.GroupSingle()
    #         player.add(Player(100 + i * 100))
    #         players.append(player)

    
    
    
    
    for genome_id, genome in genomes:
        # player = pygame.sprite.GroupSingle()
        # player.add(Player())
        player = Player()
        players.append(player)
        
        
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def score():
        global points, game_speed
        points += 0.1
        if int(points) % 100 == 0:
            game_speed += 1
        text = FONT.render(f"Points:  {str(int(points))}", True, (0, 0, 0))
        score_rect = text.get_rect(midtop=(400, 20))
        screen.blit(text, score_rect)

    def statistics():
        global players, game_speed, ge
        text_1 = FONT.render(
            f"Alive:  {str(len(players))}", True, (0, 0, 0)
        )
        text_2 = FONT.render(f"Gen:  {pop.generation+1}", True, (0, 0, 0))
        text_3 = FONT.render(f"Speed:  {str(game_speed)}", True, (0, 0, 0))

        screen.blit(text_1, (50, 20))
        screen.blit(text_2, (600, 20))
        screen.blit(text_3, (600, 50))


    """
    Enemy-Player Collision
    """

    # Return true and game over for all the genomes
    def is_collision():
        for i, player in enumerate(players):
            if pygame.sprite.spritecollide(player, enemy_group, False, collided=None):
                # players.remove(player)
                ge[i].fitness -= 1
                remove(i)

        if len(players) == 0:
            enemy_group.empty()
            return True
        return False


    game_over = False
    while True:
        for event in pygame.event.get():
            # Game Quit event
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                print("GAME CLOSED")
                sys.exit()

            # Append enemy to the class
            if event.type == enemy_timer and not game_over:
                choice_enemy = random.choice(["snail", "snail", "fly", "fly", "snail"])
                print("-----------------" + choice_enemy.upper())
                enemy_group.add(Enemy(choice_enemy))

        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))




        """
        Player-Enemy Collision
        """
        game_over = is_collision()
        # is_collision()

        if game_over:
            game_over = True
            print("GAME OVER")
            over_sound.play()
            points = 0
            break

        # """
        # GAME OVER
        # """
        # # Start the game
        # if game_over:
        #     # Resrt the score
        #     points = 0
        #     game_over = False
        #     print("GAME START")
        #     # add_players()




        """
        For Player
        """

        for player in players:
            player.draw(screen)
            player.update()

        """
        For Enemy(s)
        """

        enemy_group.draw(screen)
        enemy_group.update()

        
        # for enemy in enemy_group:
        #     enemy.draw(screen)
        #     enemy.update()
        #     for i, player in enumerate(players):
        #         if player.rect.colliderect(enemy.rect):
        #             ge[i].fitness -= 1
        #             remove(i)

        for i, player in enumerate(players):
            for enemy in enemy_group:
                output = nets[i].activate(
                    (
                        player.rect.y,
                        distance((player.rect.x, player.rect.y), enemy.rect.midtop),
                    )
                )
                player.jumping = True

                if output[0] >= 0.5:
                    player.jumping = True
                    # player.dino_run = False 

        
        score()
        statistics()
        pygame.display.update()

        # Refresh hertz
        clock.tick(60)




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

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)


assert False
