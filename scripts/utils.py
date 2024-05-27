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