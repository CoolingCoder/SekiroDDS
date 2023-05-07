import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from weapon import Weapon
from ui import UI
from enemy import Enemy

class Level:    #PONER QUE RECUPERE LA LISTA DE LOS PERSONAJES Y EL STATUS
    ''' clase para el nivel del juego '''
    def __init__(self,player_pos:tuple=(0,0),health = 100,weapon_index = 0,miniboss = True,finalboss =False) -> None:
        ''' get disp_surf '''
        self.display_surface = pygame.display.get_surface()

        ''' Sprite group setup '''
        self.visible_sprites = YSortCameraGroup('graficos/map/map.png')
        self.obstacle_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        ''' attack sprites '''
        self.current_attack = None
        
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        
        ''' Player transfer stats'''
        self.player_xy = player_pos
        self.player_health = health
        self.player_weapon_index = weapon_index

        ''' Para el update del miniboss '''
        self.mini_boss_status = miniboss
        self.finalboss_status = finalboss
        self.easter_Egg_status = False

        ''' sprite setup '''
        self.create_map()

        ''' User Interface '''
        self.ui = UI()

        self.endscreen = False
        
        ''' Para el cambio de niveles'''
        self.change = False 
        self.id = 0
        self.where_2_change = 0 #0 - MAIN MAP, 1 - SAMURAI, 2-MINIBOSS



        


    def create_map(self)->None:
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
                        if style == 'change':
                            surf =graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'change',surf)
                        if style == 'entities':
                            if col == '5' : monstername = 'raccoon'
                            elif col == '2' : monstername = 'redninja'
                            else: monstername = 'blueninja'
                            Enemy(monstername,
                                    (x,y),
                                    [self.visible_sprites,self.attackable_sprites],
                                    self.obstacle_sprites,self.damage_player)
        
        
        self.player = Player(self.player_xy,[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack,self.player_health,self.player_weapon_index)
        
    def create_attack(self) -> None:
        ''' Método para crear el ataque '''
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def destroy_attack(self) -> None:
        ''' Método para desaparecer el ataque'''
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self) -> None:
        ''' Metodo para atacar a los enemigos'''
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player)

    def damage_player(self,amount) -> None:
        ''' Metodo para recibir daño'''
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def game_over(self) -> None:
        ''' Funcion para el GAME OVER'''
        if self.player.health <= 0:
            self.endscreen = True

    def change_level(self) -> None:
        ''' Funcion para el cambio de niveles '''
        doors = pygame.sprite.spritecollide(self.player,self.door_sprites,False)
        if doors:
            self.change = True
            if self.id == 0:
                for target_sprite in doors:
                    y = target_sprite.get_pos()[1] 
                    if(y == 3712):
                        self.where_2_change = 1
                    elif(y == 1472):
                        self.where_2_change = 2
                    else:
                        self.where_2_change = 3
            #aqui guardar
        #guardar en el memento la salud y el weapon index
        #guardar tambien el status del miniboss

    def run(self)->None:
        ''' Update and draw the game '''
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        self.game_over()
        self.change_level()


       

class YSortCameraGroup(pygame.sprite.Group):
    ''' Sprite group para la camara '''
    def __init__(self,map) -> None:

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surf=pygame.image.load(map).convert()
        self.floor_rect=self.floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self,player)->None:
        ''' Funcion para dibujar en la surface el sprite / camara '''
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #draw floor
        floor_offset_pos=self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos) #rect = floor_offset_pos

        #for sprites
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):#Para crear efecto 3d y posicionar la camara
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos) #offset from player
            
    def enemy_update(self,player):
        ''' Funcion para actualizar a los enemigos '''
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
    