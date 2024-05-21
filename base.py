import pygame
from settings import *

class Base(pygame.sprite.Sprite):
    def __init__(self, type, color):
        super().__init__()
        
        if type == '1':
            self.image = pygame.image.load('Assets/Terrain/' + color + '_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (200,650))
        elif type == '2':
            self.image = pygame.image.load('Assets/Terrain/' + color + '_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (200,550))
        elif type == '3':
            self.image = pygame.image.load('Assets/Terrain/' + color + '_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (400,550))
        elif type == '4':
            self.image = pygame.image.load('Assets/Terrain/' + color + '_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (500,450))
        elif type == '5':
            self.image = pygame.image.load('Assets/Terrain/' + color + '_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (700,550))
        elif type == '6':
            self.image = pygame.image.load('Assets/Terrain/' + color + '_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (745,460))
        elif type == '7':
            self.image = pygame.image.load('Assets/Terrain/' + color + '_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (745,360))
        elif type == '8':
            self.image = pygame.image.load('Assets/Terrain/' + color + '_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (655,260))
        elif type == '9':
            self.image = pygame.image.load('Assets/Terrain/' + color + '_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (455,260))
        elif type == '10':
            self.image = pygame.image.load('Assets/Terrain/' + color + '_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (255,260))
        elif type == '11':
            self.image = pygame.image.load('Assets/Terrain/' + color + '_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (255,160))
        elif type == '12':
            self.image = pygame.image.load('Assets/Terrain/yellow_base_1.png').convert_alpha()
            self.rect = self.image.get_rect(center = (400,70))