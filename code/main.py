import pygame, sys
from settings import *
from level import Level
from stages import *
#PYREVERSE

class Game:
    ''' Clase general del juego'''
    def __init__(self) -> None:
        ''' General setup of the game '''

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Sekiro 1.0')
        self.clock = pygame.time.Clock()

        self.bg_Music = pygame.mixer.Sound('graficos/sound/Gaur_Plains.wav')
        self.end_Music = pygame.mixer.Sound('graficos/sound/Game_over.wav')
        self.end_Music.set_volume(0.05)
        self.bg_Music.set_volume(0.05)

        self.win_Music = pygame.mixer.Sound('graficos/sound/Win.wav')
        self.win_Music.set_volume(0.1)
        self.win_lenght = self.win_Music.get_length() * 1000
        self.win_flag = False

        self.eg_Music = pygame.mixer.Sound('graficos/sound/Easter_egg.wav')
        self.eg_Music.set_volume(0.3)
        self.eg_lenght = self.eg_Music.get_length() * 1000
        self.eg_flag = False
        

        self.end = True     #FLAGS PARA QUE SE REPRODUZCA UNICAMENTE UNA ANIMACION FINAL
        self.easter_egg = True
        self.win = True 
        
        self.font = pygame.font.Font(UI_FONT,150)
        self.font2 = pygame.font.Font(UI_FONT,30)

        self.sound_play_time = 0    #Tiempo de reproduccion de los sonidos de win

        self.start_game()
        
    def start_game(self) -> None:
        ''' Funcion para iniciar el juego'''
        self.bg_Music.play(loops=-1)
        self.level = Samurai()
        


    def get_text(self,msg:str,color,type) -> tuple:
        ''' Funcion para obtener el texto centrado en la pantalla'''
        if type == 0:
            text_surf = self.font.render(msg,False,color)
        else:
            text_surf = self.font2.render(msg,False,color)
        x = pygame.display.get_surface().get_size()[0] / 2
        if type == 0:
            y = pygame.display.get_surface().get_size()[1] / 2
        else:
            y = pygame.display.get_surface().get_size()[1] / 2 + 200
        text_rect = text_surf.get_rect(center = (x,y))
        return (text_surf,text_rect)
    
    def game_state(self) -> None: 
        ''' Funcion para revisar el estado del juego'''
        if self.level.endscreen:
            text = self.get_text('GAME OVER',TEXT_COLOR,0)
            pygame.display.get_surface().blit(text[0],text[1])

            text = self.get_text('Press space to restart',TEXT_COLOR,1)
            pygame.display.get_surface().blit(text[0],text[1])

            if self.end:
                self.bg_Music.stop()
                self.end_Music.play()
                self.end = False
        else:
            self.level.run()
            self.play_music_state()
            self.text_status()
            self.change_level()

    def text_status(self) -> None:
        ''' Funcion para poner win durante la cancion'''
        current_time = pygame.time.get_ticks()
        if self.win_flag:
            if current_time-self.sound_play_time >= self.win_lenght:
                self.win_flag = False
                self.bg_Music.play(loops=-1)
            else:
                text = self.get_text('YOU WIN','#A7A7A7',0)
                pygame.display.get_surface().blit(text[0],text[1])
        elif self.eg_flag:
            if current_time-self.sound_play_time >= self.eg_lenght:
                self.eg_flag = False
                self.bg_Music.play(loops=-1)
            else:
                text = self.get_text('TRUE WIN','#FFD700',0)
                pygame.display.get_surface().blit(text[0],text[1])

    def play_music_state(self) -> None:
        ''' Funcion para poner musica si acabó el juego'''
        if self.level.finalboss_status and self.win:
            self.bg_Music.stop()
            self.sound_play_time = pygame.time.get_ticks()
            self.win_Music.play()
            self.win = False
            self.win_flag = True

        if self.level.easter_Egg_status and self.easter_egg:
            self.bg_Music.stop()
            self.sound_play_time = pygame.time.get_ticks()
            self.eg_Music.play()
            self.easter_egg = False
            self.eg_flag = True

    def change_level(self) -> None:
        ''' Método para el cambio de niveles'''
        if self.level.change:
            if self.level.where_2_change == 0:
                if self.level.id == 1:
                    player_pos = (1220,3800)
                else:
                    player_pos = (1410,1545)
                Memento = self.level.save_stats()
                del self.level
                self.level = Main_map(player_pos,Memento._player_health,Memento._weapon_index,Memento._mini_boss_status,Memento._finalboss_status)
            elif self.level.where_2_change == 1:
                Memento = self.level.save_stats()
                del self.level
                self.level = Samurai((0,0),Memento._player_health,Memento._weapon_index,Memento._mini_boss_status,Memento._finalboss_status)  
            elif self.level.where_2_change == 2:
                Memento = self.level.save_stats()
                del self.level
                self.level = Mini_boss((0,0),Memento._player_health,Memento._weapon_index,Memento._mini_boss_status,Memento._finalboss_status)
            else:
                Memento = self.level.save_stats()
                del self.level
                self.level = Easter_egg((0,0),Memento._player_health,Memento._weapon_index,Memento._mini_boss_status,Memento._finalboss_status)

    def run(self) -> None:
        ''' Método para ejecutar el juego '''
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  
            self.screen.fill('black')
            self.game_state()
            pygame.display.update()
            self.clock.tick(FPS)

            if self.end == False:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.end_Music.stop()
                    self.end = True
                    del self.level
                    self.start_game()



if __name__ == '__main__':
    game = Game()
    game.run()
