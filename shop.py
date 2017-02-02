from settings import *
import pygame as pg
from os import path

class Item:
    def __init__(self):
        self.image = player_img_list[0]
        self.rect = self.image.get_rect()

class Button(pg.sprite.Sprite):
    def __init__(self,filename,text,size,parent_surface,x,y):
        pg.sprite.Sprite.__init__(self)
        self.parent_surface = parent_surface
        self.toggle = 1
        self.pos_x = x
        self.pos_y = y
        self.text = text
        self.image = pg.image.load(path.join(img_dir,filename)).convert_alpha()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #create a surface for button and show the image
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.blit(self.image,(0,0))
        #set label for the button
        self.font = pg.font.SysFont("monospace", size)
        self.text_surface = self.font.render(self.text, True, WHITE)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midtop = (self.rect.width/2,self.rect.height/2 - 10)
        self.surface.blit(self.text_surface, (self.rect.width/2 -52 , self.rect.height/2-10))
        #parent surface show the combination button image and text
        self.rect= self.parent_surface.blit(self.surface,(self.pos_x,self.pos_y))

    def update(self):
        if self.toggle == -1:
            self.text_surface = self.font.render(self.text, True, RED)
            self.surface.blit(self.text_surface, (self.rect.width/2 -52 , self.rect.height/2-10))
            self.parent_surface.blit(self.surface, (self.pos_x, self.pos_y))
        else:
            self.text_surface = self.font.render(self.text, True, WHITE)
            self.surface.blit(self.text_surface, (self.rect.width/2 -52 , self.rect.height/2-10))
            self.parent_surface.blit(self.surface, (self.pos_x, self.pos_y))



