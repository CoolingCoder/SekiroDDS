import pygame
from settings import *

class UI:
    '''Clase de las User Interfaces'''
    def __init__(self) -> None:
        ''' Elementos generales '''
        #General
        self.display_surface = pygame.display.get_surface()

        #bar setup
        self.health_bar_rect = pygame.Rect(10,670,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(490,670,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        #convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def show_bar(self,current,max_amount,bg_rect,color) -> None:
        ''' Función que te permite mostrar una stat'''
        #draw bg
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)  

        #converting stat to pixel
        ratio = current/max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        #draw bar
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect,3)

    def selection_box(self,left,top,has_switched) -> pygame.Rect:
        ''' Funcion que dibuja el marco de las armas '''
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if not has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched) -> None:
        ''' Funcion que dibuja el arma dentro del marco'''
        bg_rect = self.selection_box(1180,620,has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surf,weapon_rect)

    def display(self,player) -> None:
        ''' Funcion para la creacion de displays'''
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)

        self.weapon_overlay(player.weapon_index,player.can_switch_weapon)