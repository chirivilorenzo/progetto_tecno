import pygame
import json
from scripts.platforms import Platform, Platforms

class Map:
    def __init__(self, game, fileName):
        self.game = game
        self.fileName = fileName

    def load(self):
        #carica il json con tutte le info
        #json c'è l'oggetto con la sua posizione
        f = open(self.fileName, 'r')
        map_data = json.load(f)
        f.close()
        return map_data

    def save(self, fileJson):
        #salva la mappa con tutte le info nel json
        f = open(self.fileName, 'w')
        json.dump(fileJson, f)
        f.close()

