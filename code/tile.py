import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    ''' clase Tile para tiles (elementos del mapa) '''
    def __init__(self, pos, groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))) -> None:
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.position = pos
        if sprite_type == 'object': 
            self.rect = self.image.get_rect(topleft = (self.position[0],self.position[1] - TILESIZE))
            #self.rect = self.image.get_rect(topleft = pos)
        else:
            self.rect = self.image.get_rect(topleft = self.position)
        self.hitbox = self.rect.inflate(0,-10)
    
    def get_pos(self):
        return self.position