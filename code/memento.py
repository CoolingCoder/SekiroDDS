import pygame
from level import Level

class Memento:
    def __init__(self, player_health:int,weapon_index:int,mini_boss:bool,finalboss:bool):
        self._player_health = player_health
        self._weapon_index = weapon_index
        self._mini_boss_status = mini_boss
        self._finalboss_status = finalboss

    def get_position(self) -> tuple:
        return (self._x,self._y)
    
    def get_player_stats(self) -> list:
        return [self._player_health,self._weapon_index]

# 3.- Clase cuidadora
class Stats_saver:
    def __init__(self, cuenta:Level):
        self._cuenta = cuenta # Cuenta de banco del negocio
        self._historial = []  # Lista de mementos
    
    def save(self, cliente:str, cantidad:int): # Un cliente necesita pagar un producto
        memento = self._cuenta.depositar(cliente, cantidad)
        self._historial.append(memento)
    
    def get_back(self):
        self._historial.pop()
        memento = self._historial[-1]
        self._cuenta.restaurar(memento)