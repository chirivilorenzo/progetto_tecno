import pygame
from settings import *

class Player:
    def __init__(self, game, pos, offset=(0,0)):
        self.game = game
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.offset = offset
        self.num_jumps = 1

        self.action = ''
        self.flip = False
        self.set_action('idle')

        self.image = self.game.assets['first_player_img']
        self.rect = self.image.get_rect(topleft = pos)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.last_movement = [0,0]

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets["player/" + self.action].copy()
    
    def update(self, movement=(0,0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        #movimento che fa il player in un frame
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.rect.x += frame_movement[0] * 2
        self.rect.y += frame_movement[1] * 1.7

        #capire quando il player tocca il pavimento che può essere il pavimento ma anche una piattaforma
        #prima cosa vediamo quando tocca il pavimento
        #essendo che tutto dritto, confrontiamo la sua y
        if self.rect.y > FLOOR:
            self.rect.y = FLOOR
            self.collisions['down'] = True
            self.num_jumps = 1
        
        #ora vediamo quando colpisce il bordo sinistro
        if self.rect.x < self.offset[0]:
            self.rect.x = self.offset[0]
        
        #ora capire quando tocca una piattaforma
        for platform in self.game.platforms.platforms:
            if self.rect.colliderect(platform.rect) and self.velocity[1] > 0:
                self.rect.y = platform.rect.top - self.rect.height
                self.collisions['down'] = True
                self.num_jumps = 1

        if movement[0] != 0 and self.collisions['down']:
            self.set_action('run')
        elif movement[0] == 0 and self.collisions['down']:
            self.set_action('idle')

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        
        self.last_movement = movement
        
        self.animation.update()

        self.apply_gravity()

    
    def apply_gravity(self):
        if self.collisions['down'] == False:
            self.velocity[1] += 0.1
        else:
            self.velocity[1] = 0
    
    def jump(self):
            if self.num_jumps > 0:
                self.num_jumps -= 1
                self.set_action('jump')
                self.velocity[1] = -3
                self.collisions['down'] = False
    
    def render(self, surf):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.rect.x - self.offset[0], self.rect.y - self.offset[1]))