import pygame
from settings import *
from support import Support
from Entity import Entity

#IMPLEMENTAR BUILDER CUANDO SE CREEN LOS ENEMIGOS INTERFAZ ENTIDAD

class Player(Entity):
    ''' Clase del jugador '''
    def __init__(self, pos, groups,obstacle_sprites,create_attack,destroy_attack,health = 100,weapon_index = 0) -> None:
        super().__init__(groups)
        self.image = pygame.image.load('graficos/test/Sekiro0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-8,-26)

        #graphics setup
        self.import_player_assets()
        self.status = 'down'

        #attack
        self.attacking = False  #Estado del jugador (atacando o no)
        self.attack_cooldown:int= 280   
        self.attack_time:int = 0
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack


        self.obstacle_sprites = obstacle_sprites

        #Weapon
        self.weapon_index = weapon_index
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = 0
        self.switch_duration_cooldown = 200
        
        #Stats
        self.stats = {'health' : health,'energy':60,'attack':5,'speed':5}
        self.health = self.stats['health']
        self.max_energy = self.stats['energy']
        self.energy = self.max_energy
        self.speed = self.stats['speed']

        #Damage timer
        self.vulnerable = True
        self.hurt_time = 0
        self.invulnerability_duration = 500

    def movement_updown(self,keys)->None:
        ''' Funcion para determinar movimiento vertical del jugador'''
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

    def movement_leftright(self,keys)->None:
        ''' Funcion para determinar movimiento horizontal del jugador'''
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

    def movement_input(self,keys)->None:
        ''' Funcion para determinar movimiento del jugador'''
        self.movement_updown(keys)
        self.movement_leftright(keys)

    def attack_input(self,keys) -> None:
        ''' Funcion para determinar alguna accion del jugador'''
        #attack input
        if keys[pygame.K_SPACE] and self.energy > 8:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()  #se ejecuta 1 vez
            self.create_attack()

    def change_weapon_input(self,keys) -> None:
        '''Funcion que determina el cambio de armas del jugador'''
        if keys[pygame.K_q] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()

            if self.weapon_index < len(list(weapon_data.keys())) - 1:
                self.weapon_index += 1
            else:
                self.weapon_index = 0
            self.weapon = list(weapon_data.keys())[self.weapon_index]

    def input(self) -> None:
        ''' Keyboard input '''
        if not self.attacking: 
            keys = pygame.key.get_pressed()

            #Movement input
            self.movement_input(keys)
            #Attack input
            self.attack_input(keys)
            #switch weapon
            self.change_weapon_input(keys)

    def energy_regen(self) -> None:
        ''' Funcion para el auto regen de la energia'''
        if 'idle' in self.status or not 'attack' in self.status:
            if self.energy >= self.max_energy:
                self.energy = self.max_energy
            else:
                self.energy += 0.2

    def get_status(self) -> None:
        ''' funcion para conseguir el estado del jugador '''
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status: 
                self.status = self.status + '_idle'
        #attack status
        if self.attacking:
            self.direction.x = 0 
            self.direction.y = 0 
            if not 'attack' in self.status:
                self.energy -= 15
                if self.energy <= 0: self.energy = 0
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
            
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def import_player_assets(self) -> None:
        ''' funcion para conseguir los frames del jugador '''
        character_path = 'graficos/player/'

        self.animations = {
            'up' : [], 'down' : [], 'left' : [], 'right' : [], 
            'up_idle' : [], 'down_idle' : [], 'left_idle' : [], 'right_idle' : [], 
            'up_attack' : [], 'down_attack' : [], 'left_attack' : [], 'right_attack' : [] 
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = Support.import_folder(full_path)

    def cooldowns(self) -> None:
        ''' funcion para el cooldown de sus ataques/parry '''
        current_time = pygame.time.get_ticks()  #se ejecuta infinitas veces

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown: 
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown: 
                self.can_switch_weapon = True
            
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self) -> None:
        ''' funcion para animar al jugador'''
        
        animation = self.animations[self.status]
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        #flicker 
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_dmg(self) -> int:
        ''' Funcion para obtener el daño total del jugador '''
        base_dmg = self.stats['attack']
        weapon_dmg = weapon_data[self.weapon]['damage']
        return base_dmg + weapon_dmg

    def update(self) -> None:
        ''' Update input '''
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_regen()