import pygame
import random
from sys import exit
from settings import *
from player import Player
from base import Base


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, base_group, False):
        for base in base_group:
            if player.sprite.rect.colliderect(base.rect):
                if player.sprite.gravity > 0:
                    player.sprite.rect.bottom = base.rect.top
                    player.sprite.gravity = 0
                    player.sprite.on_ground = True              



pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

bg_surf = pygame.image.load('Assets/Background/Blue.png').convert()
frame_surf = pygame.image.load('Assets/Terrain/wood_frame.png').convert_alpha()
floor_surf = pygame.image.load('Assets/Terrain/dirt_floor.png').convert_alpha()

#obstacles
colors = ["gray", "orange", "brown"]

base_group = pygame.sprite.Group()
base_group.add(Base('1', random.choice(colors)))
base_group.add(Base('2', random.choice(colors)))
base_group.add(Base('3', random.choice(colors)))
base_group.add(Base('4', random.choice(colors)))
base_group.add(Base('5', random.choice(colors)))
base_group.add(Base('6', random.choice(colors)))
base_group.add(Base('7', random.choice(colors)))
base_group.add(Base('8', random.choice(colors)))
base_group.add(Base('9', random.choice(colors)))
base_group.add(Base('10', random.choice(colors)))
base_group.add(Base('11', random.choice(colors)))
base_group.add(Base('12', random.choice(colors)))

player = pygame.sprite.GroupSingle()
player.add(Player())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    SCREEN.blit(bg_surf, (0,0))
    SCREEN.blit(floor_surf, (0,FLOOR))
    SCREEN.blit(frame_surf, (0,0))
    
    base_group.draw(SCREEN)
    player.draw(SCREEN)
    player.update()

    collision_sprite()

    pygame.display.update()
    clock.tick(60)