class Fruit():
    def __init__(self, game, f_type, variant, pos):
        self.game = game
        self.type = f_type
        self.variant = variant
        self.pos = list(pos)

        self.image = self.game.assets[self.type][self.variant]
        self.rect = self.image.get_rect(topleft=pos)

    def player_collision(self, player_rect):
        if self.rect.colliderect(player_rect):
            return True
        return False
    
    def place(self, surf, offset=(0,0)):
        surf.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Fruits:
    def __init__(self):
        self.fruits = []

    def add_fruit(self, *fruits):
        for fruit in fruits:
            self.fruits.append(fruit)

    def check_player_collision(self, player_rect):        
        for fruit in self.fruits:
            if fruit.player_collision(player_rect):
                self.fruits.remove(fruit)

    def get_next_fruit(self, player_rect):
        min_distance = float('inf')
        next_fruit = None
        for fruit in self.fruits:
            distance = fruit.rect.x - player_rect.x
            if distance > 0 and distance < min_distance:
                min_distance = distance
                next_fruit = fruit
        return next_fruit       
    
    def render(self, surf, offset=(0,0)):
        for fruit in self.fruits:
            fruit.place(surf, offset)