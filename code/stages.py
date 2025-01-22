import pygame

from level import *
from settings import *
from tile import Tile
from player import Player
from support import *
from weapon import Weapon
from ui import UI
from enemy import Enemy

class Main_map(Level):
    def __init__(self, player_pos: tuple,health = 100,weapon_index = 0,miniboss = True,finalboss = False) -> None:   #CAMBIAR A TRUE MINIBOSS
        super().__init__(player_pos,health,weapon_index,miniboss,finalboss)
        self.visible_sprites = YSortCameraGroup('graficos/map/map.png')
        self.create_map()
        self.where_2_change = 2
        self.id = 0

    def create_map(self) -> None:
        ''' Map creation '''
        layouts={
            'boundary' : Support.import_csv_layout('graficos/map/map_layers/map/map._FLOOR BLOCKS.csv'),
            'object' : Support.import_csv_layout('graficos/map/map_layers/map/map._Objects.csv'),
            'details' : Support.import_csv_layout('graficos/map/map_layers/map/map._Objects_Details.csv'),
            'entities' : Support.import_csv_layout('graficos/map/map_layers/map/map._Entities.csv'),
            'doors' :Support.import_csv_layout('graficos/map/map_layers/map/map._Level_change.csv'),
            'change' : Support.import_csv_layout('graficos/map/map_layers/map/map._CHANGE.csv')
        }
        graphics = {
            'objects': Support.import_folder_obj('graficos/map/Objects'),
            'details': Support.import_folder_obj('graficos/map/Objects_Details')
        }
        
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'object':
                            surf =graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'objects',surf)
                        if style == 'details':
                            surf =graphics['details'][int(col)]
                            Tile((x,y),[self.visible_sprites],'details',surf)
                        if style == 'doors':
                            Tile((x,y),[self.obstacle_sprites,self.door_sprites],'doors')
                        if style == 'change' and self.mini_boss_status:
                            surf =graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'change',surf)
                        if style == 'entities':
                            if col == '5' and self.finalboss_status == False: 
                                monstername = 'raccoon'
                            elif col == '2' : monstername = 'redninja'
                            elif col == '4' : monstername = 'samurai'
                            elif col == '1': monstername = 'blueninja'
                            else: monstername = 'samurai'
                            Enemy(monstername,
                                    (x,y),
                                    [self.visible_sprites,self.attackable_sprites],
                                    self.obstacle_sprites,self.damage_player)
                            
        self.player = Player(self.player_xy,[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack,self.player_health,self.player_weapon_index)

    def check_if_win(self) -> None:
        ''' Metodo para indicar si ganaste'''
        for sprite in self.attackable_sprites:
            if sprite.enemy_name == 'raccoon':
                self.finalboss_status = sprite.final_boss


    def run(self)->None:
        ''' Update and draw the game '''
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        self.game_over()
        self.check_if_win()
        self.change_level()                        

class Mini_boss(Level):
    def __init__(self, player_pos: tuple=(0,0),health = 100,weapon_index = 0,miniboss = True,finalboss = False) -> None:
        super().__init__(player_pos,health,weapon_index,miniboss,finalboss)
        self.visible_sprites = YSortCameraGroup('graficos/map/miniboss.png')
        self.create_map()
        self.id = 2
    def create_map(self) -> None:
        ''' Map creation '''
        layouts={
            'boundary' : Support.import_csv_layout('graficos/map/map_layers/miniboss/interior_miniboss_WALLS.csv'),
            'doors' : Support.import_csv_layout('graficos/map/map_layers/miniboss/interior_miniboss_Level_change.csv'),
            'entities' : Support.import_csv_layout('graficos/map/map_layers/miniboss/interior_miniboss_Entities.csv'),
            'change' : Support.import_csv_layout('graficos/map/map_layers/miniboss/interior_miniboss_BLOCK.csv')
        }
        graphics = {
            'objects': Support.import_folder_obj('graficos/map/Objects')
        }
        
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'doors':
                            Tile((x,y),[self.obstacle_sprites,self.door_sprites],'doors')
                        if style == 'change' and self.mini_boss_status:
                            surf =graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'change',surf)
                        if style == 'entities':
                            if col == '0':
                                self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack,self.player_health,self.player_weapon_index)
                            elif col == '3' and self.mini_boss_status: #AQUI PONER QUE SE REVISE SI EL SAMURAI YA FUE MATADO
                                Enemy('masked_ninja',
                                    (x,y),
                                    [self.visible_sprites,self.attackable_sprites],
                                    self.obstacle_sprites,self.damage_player)                           

    def update_miniboss_stage(self) -> None:
        ''' Metodo para actualizar la arena en caso de haber derrotado al boss'''
        for sprite in self.attackable_sprites:
            self.mini_boss_status = sprite.mini_boss
        if self.mini_boss_status == False:
            for sprite in self.obstacle_sprites:
                if sprite.sprite_type == 'change':
                    sprite.kill()

    def run(self)->None:
        ''' Update and draw the game '''
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.update_miniboss_stage()
        self.ui.display(self.player)
        self.game_over()
        self.change_level()

class Samurai(Level):
    def __init__(self, player_pos: tuple = (0,0),health = 100,weapon_index = 0,miniboss = True,finalboss = False) -> None:
        super().__init__(player_pos,health,weapon_index,miniboss,finalboss)
        self.visible_sprites = YSortCameraGroup('graficos/map/samurai.png')
        self.create_map()
        self.id = 1
    def create_map(self) -> None:
        ''' Map creation '''
        layouts={
            'boundary' : Support.import_csv_layout('graficos/map/map_layers/samurai/interior_samurai_WALLS.csv'),
            'doors' : Support.import_csv_layout('graficos/map/map_layers/samurai/interior_samurai_Level_change.csv'),
            'entities' : Support.import_csv_layout('graficos/map/map_layers/samurai/interior_samurai_Entities.csv')
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'doors':
                            Tile((x,y),[self.obstacle_sprites,self.door_sprites],'doors')
                        if style == 'entities':
                            if col == '0':
                                self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack,self.player_health,self.player_weapon_index)
                            elif col == '4': #AQUI PONER QUE SE REVISE SI EL SAMURAI YA FUE MATADO
                                Enemy('samurai',
                                    (x,y),
                                    [self.visible_sprites,self.attackable_sprites],
                                    self.obstacle_sprites,self.damage_player)
                                
class Easter_egg(Level):
    def __init__(self, player_pos: tuple=(0,0), health=100, weapon_index=0, miniboss=True,finalboss = False) -> None:
        super().__init__(player_pos,health,weapon_index,miniboss,finalboss)
        self.visible_sprites = YSortCameraGroup('graficos/map/easter_Egg.png')
        self.create_map()
        self.id = 3
    def create_map(self) -> None:
        ''' Map creation '''
        layouts={
            'boundary' : Support.import_csv_layout('graficos/map/map_layers/easter_egg/easter_Egg_Walls.csv'),
            'entities' : Support.import_csv_layout('graficos/map/map_layers/easter_egg/easter_Egg_Entities.csv')
        }        
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'entities':
                            if col == '0':
                                self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack,self.player_health,self.player_weapon_index)
                            else:
                                if col == '5' : monstername = 'raccoon'
                                elif col == '3' : monstername = 'masked_ninja'
                                else: monstername = 'samurai'
                                Enemy(monstername,
                                        (x,y),
                                        [self.visible_sprites,self.attackable_sprites],
                                        self.obstacle_sprites,self.damage_player)
                                
    def check_if_win(self) -> None:
        ''' Metodo para indicar si ganaste en el easter egg'''
        for sprite in self.attackable_sprites:
            if sprite.enemy_name == 'samurai':
                self.easter_Egg_status = sprite.final_boss


    def run(self)->None:
        ''' Update and draw the game '''
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        self.game_over()
        self.check_if_win()
        self.change_level()