import pygame
from sys import exit
from settings import *
from player import Player
from obstacle import Obstacle


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        for obstacle in obstacle_group:
            if player.sprite.rect.colliderect(obstacle.rect):
                if player.sprite.gravity > 0:
                    player.sprite.rect.bottom = obstacle.rect.top
                    player.sprite.gravity = 0                    



pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

bg_surf = pygame.image.load('Assets/Background/Blue.png').convert()
frame_surf = pygame.image.load('Assets/Terrain/wood_frame.png').convert_alpha()
floor_surf = pygame.image.load('Assets/Terrain/dirt_floor.png').convert_alpha()

#obstacles
obstacle_group = pygame.sprite.Group()
obstacle_group.add(Obstacle('gray_base_1'))
obstacle_group.add(Obstacle('gray_base_2'))

player = pygame.sprite.GroupSingle()
player.add(Player())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    SCREEN.blit(bg_surf, (0,0))
    SCREEN.blit(floor_surf, (0,335))
    SCREEN.blit(frame_surf, (0,0))
    
    obstacle_group.draw(SCREEN)
    player.draw(SCREEN)
    player.update()

    collision_sprite()

    pygame.display.update()
    clock.tick(60)