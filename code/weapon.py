import pygame

class Weapon(pygame.sprite.Sprite):
    ''' clase para el uso de armas '''
    def __init__(self,player, groups) -> None:
        super().__init__(groups)
        direciton = player.status.split('_')[0]
        
        #graphic
        full_path = f'graficos/weapons/{player.weapon}/{direciton}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        self.image = pygame.transform.scale_by(self.image,0.9)

        #placement
        match direciton:
            case 'right' : self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,17)) 
            case 'left' : self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,17))
            case 'up' : self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(14,0))
            case 'down' : self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-14,-5))