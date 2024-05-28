import pygame
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

        self.player = Player(self, START_POINT, self.scroll)
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

            if self.die:
                break

            if self.win:
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
Game().run()