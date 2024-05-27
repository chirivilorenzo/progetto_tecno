class Platform:
    def __init__(self, game, p_type, variant, pos):
        self.game = game
        self.type = p_type
        self.variant = variant
        self.pos = list(pos)

        self.image = self.game.assets[self.type][self.variant]
        self.rect = self.image.get_rect(topleft=pos)

    def place(self, surf, offset=(0,0)):
        surf.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Platforms:
    def __init__(self):
        self.platforms = []

    def add_platform(self, *platforms):
        for platform in platforms:
            self.platforms.append(platform)
    
    def render(self, surf, offset=(0,0)):
        for platform in self.platforms:
            platform.place(surf, offset)