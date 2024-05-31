import neat.population
import pygame
import os
import neat
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
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((WIDTH/2, HEIGHT/2))

        self.clock = pygame.time.Clock()

        self.scroll = [0, 0]

        self.movement = [False, False]

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
            'first_player_img': load_image('Characters/Virtual Guy/idle/00.png'),
            'player/idle': Animation(load_images('Characters/Virtual Guy/idle')),
            'player/run': Animation(load_images('Characters/Virtual Guy/run')),
            'player/jump': Animation(load_images('Characters/Virtual Guy/jump')),
            'fruit': load_images('Fruits'),
        }

        #self.player = Player(self, START_POINT, self.scroll)
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
        punti = 0
        while True:
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
            
            if self.traps.check_player_collision(self.player.rect):
                break
            if self.fruits.check_player_collision(self.player.rect):
                punti += 5
            self.checkpoints.check_player_collision(self.player.rect)

            punti += 0.1
            punti += self.player.rect.x * 0.01

            if self.die:
                break

            if self.win:
                punti += 50
                print(str(punti))
                break

            
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
        

            #print(output)
            
            
            self.floors.render(self.display, self.scroll)
            self.platforms.render(self.display, self.scroll)
            self.traps.render(self.display, self.scroll)
            self.checkpoints.render(self.display, self.scroll)
            self.fruits.render(self.display, self.scroll)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

#Game().run()


def eval_genomes(genomes, config):
    ge = []
    nets = []
    players = []
    game = Game()

    for genome_id, genome in genomes:
        players.append(Player(game, START_POINT, game.scroll))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    game.train_ai(ge, nets, players)
    
    

def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(eval_genomes, 500)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)