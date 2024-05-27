import pygame
import os

BASE_PATH = 'Assets/'

def load_image(path):
    image = pygame.image.load(BASE_PATH + path).convert_alpha()
    return image

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    return images

class Animation:
    def __init__(self, images, increment=0.3):
        self.images = images
        self.frame = 0
        self.increment = increment
    
    def copy(self):
        return Animation(self.images, self.increment)

    def update(self):
        self.frame += self.increment
        if self.frame >= len(self.images):
            self.frame = 0
    
    def img(self):
        return self.images[int(self.frame)]