class Platform:
    def __init__(self, game, p_type, variant, pos):
        self.game = game
        self.type = p_type
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

class Platforms:
    def __init__(self):
        self.platforms = []

    def add_platform(self, *platforms):
        for platform in platforms:
            self.platforms.append(platform)
    
    def check_player_collision(self, player_rect, velocity):        
        for platform in self.platforms:
            if platform.player_collision(player_rect, velocity):
                return True
        return False

    def get_next_platform(self, player_rect):
        min_distance = float('inf')
        next_platform = None
        for platform in self.platforms:
            distance = platform.rect.x - player_rect.x
            if distance > 0 and distance < min_distance:
                min_distance = distance
                next_platform = platform
        return next_platform
    
    def render(self, surf, offset=(0,0)):
        for platform in self.platforms:
            platform.place(surf, offset)