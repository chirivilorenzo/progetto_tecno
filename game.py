import pygame
import random
from sys import exit
from settings import *
from scripts.utils import load_image, load_images, Animation
from scripts.player import Player  
from scripts.platforms import Platform, Platforms

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((WIDTH/2, HEIGHT/2))

        self.clock = pygame.time.Clock()

        self.scroll = [0, 0]

        self.movement = [False, False]

        self.assets = {
            'background': load_image('Background/Blue.png'),
            'base': load_images('Terrain/base'),
            'floor': load_images('Terrain/floors'),
            'first_player_img': load_image('Characters/Virtual Guy/idle/00.png'),
            'player/idle': Animation(load_images('Characters/Virtual Guy/idle')),
            'player/run': Animation(load_images('Characters/Virtual Guy/run')),
            'player/jump': Animation(load_images('Characters/Virtual Guy/jump')),
        }

        self.player = Player(self, START_POINT, self.scroll)

        #mettere tutti gli ostacoli così
        platform1 = Platform(self, 'base', 0, (200, 150))
        platform2 = Platform(self, 'base', 1, (150, 150))
        self.platforms = Platforms()
        self.platforms.add_platform(platform1, platform2)
    
    def createFloor(self, f_type, num):
        x = -5
        for i in range(num):
            self.display.blit(self.assets['floor'][f_type], (x - self.scroll[0], 200))
            x += 47

    def run(self):
        while True:
            self.scroll[0] += 0.3
            self.display.blit(self.assets['background'], (0,0))

            self.createFloor(1, 5)

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

            
            self.player.update((self.movement[1] - self.movement[0], 0))
            self.platforms.render(self.display, self.scroll)
            self.player.render(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
Game().run()