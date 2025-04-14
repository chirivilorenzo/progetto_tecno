import neat.population
import pygame
import os
import neat
import random
from sys import exit
from settings import *
from scripts.utils import load_image, load_images, Animation
from scripts.player import Player  
from scripts.platforms import Platform, Platforms
from scripts.floors import Floor, Floors
from scripts.traps import Trap, Traps
from scripts.checkpoints import Checkpoint, Checkpoints
from scripts.fruit import Fruit, Fruits
from scripts.map import Map

class Game:
    def __init__(self, character_index=0, camera_movement='indipendently'):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((WIDTH/2, HEIGHT/2))

        self.clock = pygame.time.Clock()

        self.scroll = [0, 0]

        self.movement = [False, False]

        self.camera_movement = camera_movement

        self.platforms = Platforms()
        self.floors = Floors()
        self.traps = Traps()
        self.checkpoints = Checkpoints()
        self.fruits = Fruits()

        self.map = Map(self, 'map.json')
        self.item_list = self.map.load()
          

        self.assets = {
            'background': load_image('Background/Blue.png'),
            'base': load_images('Terrain/base'),
            'floor': load_images('Terrain/floors'),
            'trap': load_images('Traps'),
            'box': load_images('Boxes'),
            'checkpoint': load_images('Checkpoints'),
            'first_player_img0': load_image('Characters/Virtual Guy/idle/00.png'),
            'first_player_img1': load_image('Characters/Pink Man/idle/00.png'),
            'first_player_img2': load_image('Characters/Ninja Frog/idle/00.png'),
            #'first_player_img3': load_image('Characters/Mask Dude/idle/00.png'),
            'player0/idle': Animation(load_images('Characters/Virtual Guy/idle')),
            'player0/run': Animation(load_images('Characters/Virtual Guy/run')),
            'player0/jump': Animation(load_images('Characters/Virtual Guy/jump')),
            'player1/idle': Animation(load_images('Characters/Pink Man/idle')),
            'player1/run': Animation(load_images('Characters/Pink Man/run')),
            'player1/jump': Animation(load_images('Characters/Pink Man/jump')),
            'player2/idle': Animation(load_images('Characters/Ninja Frog/idle')),
            'player2/run': Animation(load_images('Characters/Ninja Frog/run')),
            'player2/jump': Animation(load_images('Characters/Ninja Frog/jump')),
            #'player3/idle': Animation(load_images('Characters/Mask Dude/idle')),
            #'player3/run': Animation(load_images('Characters/Mask Dude/run')),
            #'player3/jump': Animation(load_images('Characters/Mask Dude/jump')),                           
            'fruit': load_images('Fruits'),
        }

        self.player = Player(self, START_POINT, character_index, self.scroll)
        self.die = False
        self.win = False

        for item in self.item_list:
            surf_item = self.assets[item['type']][item['variant']]        
            self.display.blit(surf_item, (item['position'][0], item['position'][1]))

        #inserire all'interno di tutte le liste (floors, platforms, traps), i loro rispettivi oggetti
        for item in self.item_list:
            if item['type'] == 'base':
                self.platforms.add_platform(Platform(self, item['type'], item['variant'], item['position']))
            if item['type'] == 'floor':
                self.floors.add_floor(Floor(self, item['type'], item['variant'], item['position']))
            if item['type'] == 'trap':
                self.traps.add_trap(Trap(self, item['type'], item['variant'], item['position']))
            if item['type'] == 'checkpoint':
                self.checkpoints.add_checkpoint(Checkpoint(self, item['type'], item['variant'], item['position']))
            if item['type'] == 'fruit':
                self.fruits.add_fruit(Fruit(self, item['type'], item['variant'], item['position']))

    def run(self):
        while True:
            if self.camera_movement == 'follow':
                self.scroll[0] += (self.player.rect.centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect.centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            else:
                self.scroll[0] += 0.5

            self.display.blit(self.assets['background'], (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
            
            self.traps.check_player_collision(self.player.rect)
            self.fruits.check_player_collision(self.player.rect)
            self.checkpoints.check_player_collision(self.player.rect)

            if self.die:
                return self.show_game_over_screen()

            if self.win:
                return self.show_game_over_screen()

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.floors.render(self.display, self.scroll)
            self.platforms.render(self.display, self.scroll)
            self.traps.render(self.display, self.scroll)
            self.checkpoints.render(self.display, self.scroll)
            self.fruits.render(self.display, self.scroll)
            self.player.render(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
    
    def train_ai(self, ge, nets, players):
        output_neutro = [0.0, 0.0, 0.0, 0.0]
        while True:
            self.scroll[0] += 0.5
            self.display.blit(self.assets['background'], (0,0))

            if len(players) == 0:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            for i, player in enumerate(players):    
                next_platform = self.platforms.get_next_platform(player.rect)
                next_trap = self.traps.get_next_trap(player.rect, self.scroll)
                next_fruit = self.fruits.get_next_fruit(player.rect)
                next_checkpoint = self.checkpoints.get_next_checkpoint(player.rect)

                next_platform_pos = (next_platform.rect.x, next_platform.rect.y) if next_platform else (0, 0)
                distanceBetweenPlatPlayer_x = next_platform.rect.x - player.rect.x - player.rect.width if next_platform else 0
                distanceBetweenPlatPlayer_y = next_platform.rect.y - player.rect.y - player.rect.height if next_platform else 0

                next_trap_pos = (next_trap.rect.x, next_trap.rect.y) if next_trap else (0, 0)
                distanceBetweenTrapPlayer_x = next_trap.rect.x - player.rect.x - player.rect.width if next_trap else 0
                distanceBetweenTrapPlayer_y = next_trap.rect.y - player.rect.y - player.rect.height if next_trap else 0                

                next_fruit_pos = (next_fruit.rect.x, next_fruit.rect.y) if next_fruit else (0, 0)
                distanceBetweenFruitPlayer_x = next_fruit.rect.x - player.rect.x - player.rect.width if next_fruit else 0
                distanceBetweenFruitPlayer_y = next_fruit.rect.y - player.rect.y - player.rect.height if next_fruit else 0

                next_checkpoint_pos = (next_checkpoint.rect.x, next_checkpoint.rect.y) if next_checkpoint else (0, 0)
                distanceBetweenCheckPlayer_x = next_checkpoint.rect.x - player.rect.x - player.rect.width if next_checkpoint else 0
                distanceBetweenCheckPlayer_y = next_checkpoint.rect.y - player.rect.y - player.rect.height if next_checkpoint else 0

                inputs = (
                    player.rect.x, player.rect.y,
                    next_platform_pos[0], next_platform_pos[1],
                    distanceBetweenPlatPlayer_x, distanceBetweenPlatPlayer_y,
                    next_trap_pos[0], next_trap_pos[1],
                    distanceBetweenTrapPlayer_x, distanceBetweenTrapPlayer_y,
                    next_fruit_pos[0], next_fruit_pos[1],
                    distanceBetweenFruitPlayer_x, distanceBetweenFruitPlayer_y,
                    next_checkpoint_pos[0], next_checkpoint_pos[1],
                    distanceBetweenCheckPlayer_x, distanceBetweenCheckPlayer_y
                )

                output = nets[i].activate(inputs)
                decision = output.index(max(output))

                if output != output_neutro:
                    if decision == 0:
                        player.jump()
                    elif decision == 1:
                        self.movement[0] = True
                    elif decision == 2:
                        self.movement[1] = True
                    else:
                        self.movement[0] = False
                        self.movement[1] = False
                else:
                    self.movement[0] = False
                    self.movement[1] = False                    

                player.update((self.movement[1] - self.movement[0], 0))
                player.render(self.display)

                ge[i].fitness += 0.1
                ge[i].fitness += player.rect.x * 0.01

                if self.fruits.check_player_collision(player.rect):
                    ge[i].fitness += 5
                
                if self.traps.check_player_collision(player.rect):
                    ge[i].fitness -= 10
                    players.pop(i)
                    ge.pop(i)
                    nets.pop(i)
                    continue
                
                if self.checkpoints.check_player_collision(player.rect):
                    ge[i].fitness += 50
                    players.pop(i)
                    ge.pop(i)
                    nets.pop(i)
                    continue
                
        
            self.floors.render(self.display, self.scroll)
            self.platforms.render(self.display, self.scroll)
            self.traps.render(self.display, self.scroll)
            self.checkpoints.render(self.display, self.scroll)
            self.fruits.render(self.display, self.scroll)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

    def show_game_over_screen(self):
        while True:
            self.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 74)
            if self.die == True:
                text = font.render("Game Over", True, (255, 255, 255))
            else:
                text = font.render("You Won", True, (255, 255, 255))
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

            font = pygame.font.Font(None, 50)
            text = font.render("Press R to Retry or M for Main Menu", True, (255, 255, 255))
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return 'retry'
                    if event.key == pygame.K_m:
                        return 'menu'

class NeatAI:
    def __init__(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config.txt")

        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)

        self.run_neat(config)      

    def eval_genomes(self, genomes, config):
        ge = []
        nets = []
        players = []
        game = Game()

        for genome_id, genome in genomes:
            num = random.randint(0, 2)
            players.append(Player(game, START_POINT, num, game.scroll))
            ge.append(genome)
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            genome.fitness = 0

        game.train_ai(ge, nets, players)
            

    def run_neat(self, config):
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        p.run(self.eval_genomes, 500)

def show_start_screen(screen):
    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("2D Game", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

        font = pygame.font.Font(None, 50)
        text = font.render("Press P to Play or A for AI", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return choose_pg(screen)
                if event.key == pygame.K_a:
                    return 'ai'

def choose_pg(screen):
    screen.fill((0, 0, 0))

    clock = pygame.time.Clock()

    fontTitle = pygame.font.Font(None, 74)
    font = pygame.font.Font(None, 30)

    text = fontTitle.render("Scegli il personaggio", True, (255, 255, 255))
    text0 = font.render("Virtual Guy | 0", False, (3, 227, 252))
    text1 = font.render("Pink Man | 1", False, (235, 84, 222))
    text2 = font.render("Ninja Frog | 2", False, (54, 125, 45))

    animations = [
        Animation(load_images('Characters/Virtual Guy/run')),
        Animation(load_images('Characters/Pink Man/run')),
        Animation(load_images('Characters/Ninja Frog/run'))
    ]

    valuePg = '-1'
    while valuePg == '-1':

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    valuePg = '0'
                if event.key == pygame.K_1:
                    valuePg = '1'
                if event.key == pygame.K_2:
                    valuePg = '2'

        for animation in animations:
            animation.update()


        screen.fill((0, 0, 0))
        colonna = WIDTH // 3

        # Fattore di scala (es: 2x)
        scale_factor = 2

        # Ottieni immagine originale
        img0 = animations[0].img()
        img1 = animations[1].img()
        img2 = animations[2].img()

        # Scala l'immagine dei personaggi
        scaled_img0 = pygame.transform.scale(img0, (img0.get_width() * scale_factor, img0.get_height() * scale_factor))
        scaled_img1 = pygame.transform.scale(img1, (img1.get_width() * scale_factor, img1.get_height() * scale_factor))
        scaled_img2 = pygame.transform.scale(img2, (img2.get_width() * scale_factor, img2.get_height() * scale_factor))

        #disegna scritta titolo e nome pg
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 140))
        screen.blit(text0, (colonna // 2 - text0.get_width() // 2, HEIGHT - 95))
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT - 95))
        screen.blit(text2, (WIDTH - colonna // 2 - text2.get_width() // 2, HEIGHT - 95))

        # Disegna le animazioni dei personaggi
        screen.blit(scaled_img0, (colonna // 2 - 32, HEIGHT // 2 - 10))
        screen.blit(scaled_img1, (WIDTH // 2 - 32, HEIGHT // 2 - 10))
        screen.blit(scaled_img2, (WIDTH - colonna // 2 - 32, HEIGHT // 2 - 10))

        pygame.display.flip()
        clock.tick(60)

    return valuePg

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    while True:
        choice = show_start_screen(screen)

        if choice in ['0', '1', '2']:
            result = 'retry'
            while result == 'retry':
                game = Game(character_index=choice, camera_movement='follow')
                result = game.run()
            if result == 'menu':
                continue

        elif choice == 'ai':
            NeatAI()

if __name__ == '__main__':
    main()
