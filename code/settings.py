

''' GAME SETUP '''
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

#UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 300
ITEM_BOX_SIZE = 80
UI_FONT = 'graficos/font/joystix.ttf'

#GENERAL COLORS
UI_BG_COLOR = '#222222'
UI_BG_COLOR_ENERGY = '#4C3E2D'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

#UI COLORS
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'orange'
UI_BORDER_COLOR_ACTIVE = 'gold'

#enemy
enemy_data = {
    'raccoon' : {'health':500,'damage':33,'speed':5,'resistance':2,'attack_radius':150,'notice_radius' : 600},    #FINAL BOSS
    'blueninja' : {'health':100,'damage':17,'speed':3.5,'resistance':2,'attack_radius':80,'notice_radius' : 300}, #ENEMY1
    'redninja' :{'health':100,'damage':17,'speed':3.5,'resistance':2,'attack_radius':80,'notice_radius' : 300},   #ENEMY2
    'masked_ninja':{'health':300,'damage':25,'speed':6.5,'resistance':2,'attack_radius':90,'notice_radius' : 600},#MINIBOSS
    'samurai': {'health':50,'damage':5,'speed':2,'resistance':2,'attack_radius':60,'notice_radius' : 100}     #MASTER
}

weapon_data = {
    'sword': {'damage':30,'graphic':'graficos/weapons/sword/full.png'},
    'lance': {'damage':20,'graphic':'graficos/weapons/lance/full.png'},
    'axe': {'damage':26,'graphic':'graficos/weapons/axe/full.png'},
    'rapier': {'damage':30,'graphic':'graficos/weapons/rapier/full.png'},
    'sai': {'damage':35,'graphic':'graficos/weapons/sai/full.png'}
}