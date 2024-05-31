class Trap():
    def __init__(self, game, t_type, variant, pos):
        self.game = game
        self.type = t_type
        self.variant = variant
        self.pos = list(pos)

        self.image = self.game.assets[self.type][self.variant]
        self.rect = self.image.get_rect(topleft=pos)

    def player_collision(self, player_rect):
        if self.rect.colliderect(player_rect):
            #self.game.die = True
            return True
    
    def place(self, surf, offset=(0,0)):
        surf.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Traps:
    def __init__(self):
        self.traps = []

    def add_trap(self, *traps):
        for trap in traps:
            self.traps.append(trap)

    def check_player_collision(self, player_rect):        
        for trap in self.traps:
            if trap.player_collision(player_rect):
                return True
        return False

    def get_next_trap(self, player_rect, offset=(0,0)):
        min_distance = float('inf')
        next_trap = None
        for trap in self.traps:
            distance = trap.rect.x - player_rect.x - player_rect.width
            if distance > 0 and distance < min_distance:
                min_distance = distance
                next_trap = trap
        return next_trap
    
    def render(self, surf, offset=(0,0)):
        for trap in self.traps:
            trap.place(surf, offset)