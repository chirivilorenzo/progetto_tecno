import pygame

class PhisicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = pos
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.action = ''
        self.flip = False
        self.set_action('idle')

    def set_action(self, action):
        if action != self.action:
            self.action = action
            #animazione