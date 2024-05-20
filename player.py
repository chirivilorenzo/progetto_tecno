import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('Assets/Characters/virtual_guy_1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (50,335))
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 335:
            self.gravity = -15
        if keys[pygame.K_LEFT]:
            if self.rect.left <= BORDER_LEFT: self.rect.left = BORDER_LEFT
            else: self.rect.left -= 5
        if keys[pygame.K_RIGHT]:
            if self.rect.right >= BORDER_RIGHT: self.rect.right = BORDER_RIGHT
            else: self.rect.right += 5
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 335:
            self.rect.bottom = 335
            self.gravity = 0         
    
    def update(self):
        self.player_input()
        self.apply_gravity()