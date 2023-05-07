from typing import Any
import pygame
from settings import * 
from Entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self,enemy_name,pos,groups,obstacle_sprites,damage_player):
        ''' Init de los enemigos'''
        super().__init__(groups)
        self.sprite_type='enemy'

        #graphics setup
        self.import_graphics(enemy_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft= pos)

        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        
        #stats
        self.enemy_name = enemy_name
        enemy_info = enemy_data[self.enemy_name]
        self.health = enemy_info['health']
        self.attack_damage = enemy_info['damage']
        self.speed = enemy_info['speed']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']

        #player interaction
        self.can_attack = True
        self.attack_time = 0
        self.attack_cooldown = 400
        self.damage_player = damage_player

        #invincibility timer
        self.vulnerable = True
        self.hit_time = 0
        self.invincibility_duration = 600

        self.give_health = True
        self.mini_boss = True
        self.final_boss = False

    def import_graphics(self,name) -> None:
        ''' Funcion para importar los gráficos de los enemigos '''
        self.animations = {'idle':[],'move':[],'attack':[],'dead':[]}
        main_path = f'graficos/entities/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = Support.import_folder_obj(main_path + animation)

    def get_player_distance_direction (self,player) -> tuple:
        ''' Funcion para obtener la distancia y la direccion con el jugador'''
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)

    def get_status(self,player) -> None:
        ''' Funcion para obtener el status del enemigo'''
        if self.status != 'dead':
            distance = self.get_player_distance_direction(player)[0]
            if distance <= self.attack_radius and self.can_attack:
                if self.status != 'attack':
                    self.frame_index = 0
                self.status = 'attack'
            elif distance <= self.notice_radius:
                self.status = 'move'
            else:
                self.status = 'idle'

    def actions(self,player) -> None:
        ''' Funcion para hacer una accion'''
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        ''' Funcion para animar a los enemigos'''
        animation = self.animations[self.status]
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self) -> None:
        ''' Funcion para el cooldown de los enemigos'''
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self,player) -> None:
        ''' Funcion para obtener el daño causado por el jugador'''
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            self.health -= player.get_full_weapon_dmg()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
            if self.health<=0 and self.give_health:
                player.health += 20
                if player.health > 100:
                    player.health = 100
                self.give_health = False

    def check_death(self) -> None:
        ''' Funcion para revisar si el enemigo muere'''
        if self.health <= 0 and self.health > -100:
            self.status = 'dead'
            if self.enemy_name == 'masked_ninja':
                self.mini_boss = False
            elif self.enemy_name == 'raccoon' or self.enemy_name == 'samurai':
                self.final_boss = True
        elif self.health <= -100:
            self.kill()
            
    def hit_reaction(self) -> None:
        ''' Funcion para afectar la direccion del enemigo al ser golpeado'''
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self) -> None:
        ''' Funcion para actualizar los enemigos'''
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()
    
    def enemy_update(self,player) -> None:
        ''' Funcion para actualizar al enemigo'''
        self.get_status(player)
        self.actions(player)