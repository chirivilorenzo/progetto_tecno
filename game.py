import pygame
import random
from sys import exit
from settings import *
from scripts.utils import load_image, load_images  

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((WIDTH/2, HEIGHT/2))

        self.clock = pygame.time.Clock()

        self.assets = {
            'background': load_image('Background/Blue.png'),
            'base': load_images('Terrain/base'),
            'floor': load_images('Terrain/floors'),
            'player/idle': load_image('Characters/Virtual Guy/idle/0.png'),
        }

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0,0))
            self.display.blit(self.assets['player/idle'], (20, 200))
            self.display.blit(self.assets['base'][0], (200, 200))
            for i in range(10):
                self.display.blit(self.assets['floor'][0], (200,100 * i))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
Game().run()