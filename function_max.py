import pygame as pg
import sys,random,time
from os import path
from sprites import *
import pytmx
from pytmx.util_pygame import load_pygame

# Read TXT file
def read_txtfile(filename):
    root_dir = path.dirname(__file__)
    txt_folder = path.join(root_dir,'txt')
    txt_file = path.join(txt_folder,filename)
    content = []
    with open(txt_file, 'rt') as f:
        for line in f:
            content.append(line)
    return content


#read txt file and return list from xml, file name, x,y and width,height
def reading_line_text(filename):
    root_dir = path.dirname(__file__)
    txt_folder = path.join(root_dir, 'txt')
    txt_file = path.join(txt_folder, filename)
    lines = []
    result = []
    with open (txt_file, 'rt') as f:
        for line in f:
            lines.append(line.strip('\n'))
        for line in lines:
            scan =[]
            n = 0
            couple = False
            while n <= len(line):
                if line.find('"', n) > 0 :
                    if couple == False:
                        first = line.find('"', n)
                        n = first + 1
                        couple = True
                    else:
                        second = line.find('"', n)
                        n = second + 1
                        scan.append(line[first+1:second])
                        couple = False
                else:
                    break
            result.append(scan)
    return result





def load_txt_map(filename):
    map_data = []
    with open (filename,'rt') as f:
       for line in f:
           map_data.append(line)
    return map_data
def load_tmx_map(filename):
    tmx_data = load_pygame(filename)
    return tmx_data

def render(tmx_data,surface):
    ti = tmx_data.get_tile_image_by_gid
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid, in layer:
                tile = ti(gid)
                if tile:
                    surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))
















# Write TXT file
def write_txtfile(content,filename):
    txt_content = str(content)
    txt_folder = path.join((path.dirname(__file__)), 'txt')
    txt_file = path.join(txt_folder,filename)
    with open(txt_file,'w') as f:
        f.write(txt_content)

# Load and Play music
def load_sound(filename):
    pg.mixer.init()
    music_folder = path.join(path.dirname(__file__),'music')
    music_file = path.join(music_folder,filename)
    pg.mixer.music.load(music_file)
    pg.mixer.music.play(-1)

#load Image file
def load_image(filename):
    img_folder = path.join(path.dirname(__file__),'img')
    img_file = path.join(img_folder,filename)
    image_loaded = pg.image.load(img_file).convert()
    return image_loaded

#extract sprites from sprite sheet,sheet must be a loaded image
def extract_sprite(sheet,position_x,position_y,size_width,size_height):
    clip_rect = pg.Rect(position_x,position_y,size_width,size_height)
    sheet.set_clip(clip_rect)
    extracted = sheet.subsurface(sheet.get_clip())
    return extracted

#create Imgage list for anumation
def create_imagelist_animation(file_list):
    img_list = []
    for i in range(9):
        filename = 'file_list{}.png'.format(i)
        img = pg.image.load(filename).convert()
        img_list.append(img)
    return img_list

#play animation from files in the list
def play_anim(surface,img_list):
    now = pg.time.get_ticks()
    for image in img_list:
        img = image
        img_rect = img.get_rect()
        surface.blit(img,img_rect)


#print text on the screen
def draw_text(surf,text, size, x,y,color,font_type):
    font = pg.font.Font(font_type, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)











