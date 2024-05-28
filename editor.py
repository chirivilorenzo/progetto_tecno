import pygame
import random
from sys import exit
from settings import *
from scripts.utils import load_image, load_images, Animation
from scripts.player import Player  
from scripts.map import Map

class Editor:
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
            'trap': load_images('Traps'),
            'box': load_images('Boxes'),
            'checkpoint': load_images('Checkpoints'),
            'first_player_img': load_image('Characters/Virtual Guy/idle/00.png'),
            'fruit': load_images('Fruits')
        }

        self.type = 0
        self.variant = 0
        self.asset_keys = list(self.assets.keys())
        self.shift_hold = False

        self.map = Map(self, 'map.json')
        self.item_list = self.map.load()

        self.createFloor(2, 15, (0,0))
            

    def createFloor(self, f_type, num, render_scroll):
        x = -10
        y = 400
        self.type = 1
        self.variant = f_type
        for i in range(num):
            self.add_item((x, y), render_scroll)
            x += 94

    def add_item(self, pos, render_scroll):
        pos_x = pos[0] / 2 + render_scroll[0]
        pos_y = pos[1] / 2 + render_scroll[1]
        item = {
            'type': self.asset_keys[self.type],
            'variant': self.variant,
            'position': (pos_x, pos_y)
        }
        self.item_list.append(item)

    def place_items(self, render_scroll):
        for item in self.item_list:
            surf_item = self.assets[item['type']][item['variant']]        
            self.display.blit(surf_item, (item['position'][0] - render_scroll[0], item['position'][1] - render_scroll[1]))

    def remove_item(self, mpos, render_scroll):
        pos_x = mpos[0] / 2 + render_scroll[0]
        pos_y = mpos[1] / 2 + render_scroll[1]

        for item in self.item_list:
            surf_item = self.assets[item['type']][item['variant']]        
            rect = surf_item.get_rect(topleft = (item['position'][0], item['position'][1]))
            if rect.collidepoint((pos_x, pos_y)):
                self.item_list.remove(item)

    def run(self):
        while True:

            self.display.fill((0,0,0))
            self.display.blit(self.assets['first_player_img'], (START_POINT))

            #serve per muovere la telecamera con wasd
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            

            #visualizza l'elemento in alto a sinistra
            self.current_item = self.assets[self.asset_keys[self.type]][self.variant].copy()
            self.current_item.set_alpha(100)
            self.display.blit(self.current_item, (5,5))

            #visualizzare l'elemento selezionato sotto il cursore del mouse
            self.display.blit(self.current_item, (pygame.mouse.get_pos()[0] / 2, pygame.mouse.get_pos()[1] / 2))

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
                    if event.key == pygame.K_o:
                        self.map.save(self.item_list)

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
                    if self.shift_hold:
                        if event.button == 4:
                            self.variant = (self.variant + 1) % len(self.assets[self.asset_keys[self.type]])
                        if event.button == 5:
                            self.variant = (self.variant - 1) % len(self.assets[self.asset_keys[self.type]])
                    else:
                        if event.button == 4:
                            self.type = (self.type + 1) % len(self.asset_keys)
                            self.variant = 0
                        if event.button == 5:
                            self.type = (self.type - 1) % len(self.asset_keys)
                            self.variant = 0
                    if event.button == 1:
                        self.add_item(pygame.mouse.get_pos(), render_scroll)
                    if event.button == 3:
                        self.remove_item(pygame.mouse.get_pos(), render_scroll)


            self.place_items(render_scroll)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
Editor().run()