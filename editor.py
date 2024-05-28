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

        self.movement = [False, False, False, False]

        self.assets = {
            'base': load_images('Terrain/base'),
            'floor': load_images('Terrain/floors'),
        }

        self.type = 0
        self.variant = 0
        self.asset_keys = list(self.assets.keys())
        self.shift_hold = False

        self.item_list = []   

        #mettere tutti gli ostacoli così
        platform1 = Platform(self, 'base', 0, (200, 150))
        platform2 = Platform(self, 'base', 1, (150, 150))
        self.platforms = Platforms()
        self.platforms.add_platform(platform1, platform2)

    def createFloor(self, f_type, num, render_scroll):
        x = -5
        y = 200
        for i in range(num):
            self.display.blit(self.assets['floor'][f_type], (x - render_scroll[0], y - render_scroll[1]))
            x += 47

    def add_item(self, pos):
        element = {
            'type': self.asset_keys[self.type],
            'variant': self.variant,
            'position': list(pos)
        }
        self.item_list.append(element)

    def place_items(self):
        for item in self.item_list:
            surf_item = self.assets[item['type']][item['variant']]            
            self.display.blit(surf_item, item['position'])

    def run(self):
        while True:

            self.display.fill((0,0,0))

            #serve per muovere la telecamera con wasd
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.createFloor(1, 5, render_scroll)

            self.current_item = self.assets[self.asset_keys[self.type]][self.variant]
            self.display.blit(self.current_item, (5,5))

            self.platforms.render(self.display, render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift_hold = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift_hold = False                        
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.add_item(pygame.mouse.get_pos())
                    if event.button == 4:
                        if self.shift_hold:
                            self.variant = (self.variant + 1) % len(self.assets[self.asset_keys[self.type]])
                        else:
                            self.type = (self.type + 1) % len(self.asset_keys)
                            self.variant = 0

                    if event.button == 5:
                        if self.shift_hold:
                            self.variant = (self.variant - 1) % len(self.assets[self.asset_keys[self.type]])
                        else:
                            self.type = (self.type - 1) % len(self.asset_keys)
                            self.variant = 0

            self.place_items()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
Game().run()