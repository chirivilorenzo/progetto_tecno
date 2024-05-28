class Floor():
    def __init__(self, game, f_type, variant, pos):
        self.game = game
        self.type = f_type
        self.variant = variant
        self.pos = list(pos)

        self.image = self.game.assets[self.type][self.variant]
        self.rect = self.image.get_rect(topleft=pos)

    def player_collision(self, player_rect, velocity):
        if self.rect.colliderect(player_rect):
            if player_rect.bottom <= self.rect.top + 10 and velocity > 0:
                player_rect.y = self.rect.top - player_rect.height
                return True
        return False
    
    def place(self, surf, offset=(0,0)):
        surf.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Floors:
    def __init__(self):
        self.floors = []

    def add_floor(self, *floors):
        for floor in floors:
            self.floors.append(floor)

    def check_player_collision(self, player_rect, velocity):        
        for floor in self.floors:
            if floor.player_collision(player_rect, velocity):
                return True
        return False            
    
    def render(self, surf, offset=(0,0)):
        for floor in self.floors:
            floor.place(surf, offset)