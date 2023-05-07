from csv import reader
from os import walk
import pygame
from natsort import natsorted

#CLASE ESTÁTICA
class Support:
    @classmethod
    def import_csv_layout(cls,path) -> list:
        ''' Funcion para leer el archivo csv '''
        terrain_map = []

        with open(path) as level_map:
            layout = reader(level_map,delimiter=',')
            for row in layout:
                terrain_map.append(list(row))  #6157 para el delimiter
            return terrain_map
        
    @classmethod
    def import_folder(cls,path) -> list:
        ''' funcion para poder hacer el path a archivos en una carpeta y hacerlos superficies'''
        surface_list = []

        for _,__,img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                image_surf = pygame.transform.scale_by(image_surf,0.9)
                surface_list.append(image_surf)

        return surface_list

    @classmethod
    def import_folder_obj(cls,path) -> list:
        ''' funcion para poder hacer el path a archivos en una carpeta y hacerlos superficies para objetos'''
        surface_list = []

        for _,__,img_files in walk(path):
            img_files_sorted = natsorted(img_files)
            for image in img_files_sorted:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                image_surf = pygame.transform.scale_by(image_surf,4)
                surface_list.append(image_surf)

        return surface_list