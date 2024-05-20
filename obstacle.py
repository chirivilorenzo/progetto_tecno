import pygame
from settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'gray_base_1':
            self.image = pygame.image.load('Assets/Terrain/gray_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (200,250))
        elif type == 'gray_base_2':
            self.image = pygame.image.load('Assets/Terrain/gray_base_2.png').convert_alpha()
            self.rect = self.image.get_rect(center = (250,200))