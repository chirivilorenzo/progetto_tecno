class Checkpoint():
    def __init__(self, game, t_type, variant, pos):
        self.game = game
        self.type = t_type
        self.variant = variant
        self.pos = list(pos)

        self.image = self.game.assets[self.type][self.variant]
        self.rect = self.image.get_rect(topleft=pos)

    def player_collision(self, player_rect):
        if self.rect.colliderect(player_rect):
            self.game.win = True
    
    def place(self, surf, offset=(0,0)):
        surf.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Checkpoints:
    def __init__(self):
        self.checkpoints = []

    def add_checkpoint(self, *checkpoints):
        for checkpoint in checkpoints:
            self.checkpoints.append(checkpoint)

    def check_player_collision(self, player_rect):        
        for checkpoint in self.checkpoints:
            if checkpoint.player_collision(player_rect):
                return True
        return False            
    
    def render(self, surf, offset=(0,0)):
        for checkpoint in self.checkpoints:
            checkpoint.place(surf, offset)