import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #immagini per animazione player fermo
        player_idle_1 = pygame.image.load('Assets/Characters/Virtual Guy/idle/virtual_guy_idle_1.png').convert_alpha()
        player_idle_2 = pygame.image.load('Assets/Characters/Virtual Guy/idle/virtual_guy_idle_2.png').convert_alpha()
        player_idle_3 = pygame.image.load('Assets/Characters/Virtual Guy/idle/virtual_guy_idle_3.png').convert_alpha()
        player_idle_4 = pygame.image.load('Assets/Characters/Virtual Guy/idle/virtual_guy_idle_4.png').convert_alpha()
        player_idle_5 = pygame.image.load('Assets/Characters/Virtual Guy/idle/virtual_guy_idle_5.png').convert_alpha()
        player_idle_6 = pygame.image.load('Assets/Characters/Virtual Guy/idle/virtual_guy_idle_6.png').convert_alpha()
        player_idle_7 = pygame.image.load('Assets/Characters/Virtual Guy/idle/virtual_guy_idle_7.png').convert_alpha()
        player_idle_8 = pygame.image.load('Assets/Characters/Virtual Guy/idle/virtual_guy_idle_8.png').convert_alpha()
        player_idle_9 = pygame.image.load('Assets/Characters/Virtual Guy/idle/virtual_guy_idle_9.png').convert_alpha()
        player_idle_10 = pygame.image.load('Assets/Characters/Virtual Guy/idle/virtual_guy_idle_10.png').convert_alpha()
        player_idle_11 = pygame.image.load('Assets/Characters/Virtual Guy/idle/virtual_guy_idle_11.png').convert_alpha()

        self.player_idle = [
            player_idle_1,
            player_idle_2,
            player_idle_3,
            player_idle_4,
            player_idle_5,
            player_idle_6,
            player_idle_7,
            player_idle_8,
            player_idle_9,
            player_idle_10,
            player_idle_11
        ]
        self.player_idle_index = 0
        self.image = self.player_idle[self.player_idle_index]
        self.player_jump = pygame.image.load('Assets/Characters/Virtual Guy/Jump.png').convert_alpha()
        self.player_fall = pygame.image.load('Assets/Characters/Virtual Guy/Fall.png').convert_alpha()

        #immagini per animazione player in corsa
        player_run_1 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_1.png').convert_alpha()
        player_run_2 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_2.png').convert_alpha()
        player_run_3 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_3.png').convert_alpha()
        player_run_4 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_4.png').convert_alpha()
        player_run_5 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_5.png').convert_alpha()
        player_run_6 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_6.png').convert_alpha()
        player_run_7 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_7.png').convert_alpha()
        player_run_8 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_8.png').convert_alpha()
        player_run_9 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_9.png').convert_alpha()
        player_run_10 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_10.png').convert_alpha()
        player_run_11 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_11.png').convert_alpha()
        player_run_12 = pygame.image.load('Assets/Characters/Virtual Guy/run/virtual_guy_run_12.png').convert_alpha()

        self.player_run = [
            player_run_1,
            player_run_2,
            player_run_3,
            player_run_4,
            player_run_5,
            player_run_6,
            player_run_7,
            player_run_8,
            player_run_9,
            player_run_10,
            player_run_11,
            player_run_12
        ]
        self.player_run_index = 0

        self.rect = self.image.get_rect(midbottom = START_POINT)
        self.gravity = 0
        self.on_ground = True
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.gravity = -15
            self.on_ground = False
        if keys[pygame.K_LEFT]:
            if self.rect.left <= BORDER_LEFT: self.rect.left = BORDER_LEFT
            else: self.rect.left -= 5
        if keys[pygame.K_RIGHT]:
            if self.rect.right >= BORDER_RIGHT: self.rect.right = BORDER_RIGHT
            else: self.rect.right += 5
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= FLOOR:
            self.rect.bottom = FLOOR
            self.gravity = 0
            self.on_ground = True

    def animation_state(self):
        if self.rect.bottom < FLOOR and self.gravity < 0 and self.on_ground == False:
            self.image = self.player_jump
        elif self.rect.bottom < FLOOR and self.gravity > 0 and self.on_ground == False:
            self.image = self.player_fall
        else:
            keys = pygame.key.get_pressed()
            if not any(keys):
                self.player_idle_index += 0.2
                if self.player_idle_index >= len(self.player_idle): self.player_idle_index = 0
                self.image = self.player_idle[int(self.player_idle_index)]
            else:
                self.player_run_index += 0.4
                if self.player_run_index >= len(self.player_run): self.player_run_index = 0
                self.image = self.player_run[int(self.player_run_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()