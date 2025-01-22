
class Memento:
    def __init__(self, player_health:int,weapon_index:int,mini_boss:bool,finalboss:bool):
        self._player_health = player_health
        self._weapon_index = weapon_index
        self._mini_boss_status = mini_boss
        self._finalboss_status = finalboss
