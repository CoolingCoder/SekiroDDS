import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self,speed) -> None:
        ''' Funcion para el movimiento del player '''
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def vertical_collision(self,direction:str)->None:
        ''' funcion para la colision vertical '''
        for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0: #Moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0: #Moving down
                        self.hitbox.bottom = sprite.hitbox.top
    
    def horizontal_collision(self,direction:str)->None:
        ''' funcion para la colision vertical '''
        for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #Moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #Moving left
                        self.hitbox.left = sprite.hitbox.right

    def collision(self,direction:str ) -> None:
        ''' funcion para la colosión del jugador '''
        if direction == 'horizontal':
            self.horizontal_collision(direction)
        if direction == 'vertical':
            self.vertical_collision(direction)

    def wave_value(self) -> int:
        ''' Funcion para darle un valor a alpha'''
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0 