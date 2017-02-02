from os import path
import pygame as pg

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
amie_dir = path.join(path.dirname(__file__), 'expl')

font_type = pg.font.match_font('arial')

#settings
WIDTH = 1000
HEIGHT = 650
FPS = 60
POWERUP_TIME= 5000
SPEED_LAST = 5000
speed_change = 10
BackDrop_rolling_Speed = 3

#define all the colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)



#load all game pictures
pg.init()
pg.display.set_mode((800,600))

background = pg.image.load(path.join(img_dir, "backdrop.jpg")).convert()
background = pg.transform.scale(background,(WIDTH,HEIGHT))
background_rect = background.get_rect()
menu_background = pg.image.load(path.join(img_dir, "menu_backdrop.png")).convert()
menu_background_rect = menu_background.get_rect()

menu_cover = pg.image.load(path.join(img_dir,'menu_cover.png')).convert()

#player image list
description_list = [pg.image.load(path.join(img_dir, 'Earth.png')).convert(),
                    pg.image.load(path.join(img_dir, 'Mercury.png')).convert(),
                    pg.image.load(path.join(img_dir, 'Pluto.png')).convert(),
                    pg.image.load(path.join(img_dir, 'Saturn.png')).convert(),
                    pg.image.load(path.join(img_dir, 'Venus.png')).convert(),
                    pg.image.load(path.join(img_dir, 'Mars.png')).convert(),
                    pg.image.load(path.join(img_dir, 'Moon.png')).convert(),
                    pg.image.load(path.join(img_dir, 'Jupiter.png')).convert()]

option_list = ['Earth','Mercury','Pluto','Saturn','Venus','Mars','Moon', 'Jupiter']

player_img_list = []
for i in range(0,8):
    filename = 'spaceship{}.png'.format(i)
    image = pg.image.load(path.join(img_dir, filename)).convert_alpha()
    image = pg.transform.scale(image, (60, 80))
    image.set_colorkey(WHITE)
    player_img_list.append(image)
player_img = player_img_list[1]

#boss image list
boss_img = []
boss_list = ['boss1.png','boss2.jpg','boss3.png','boss4.png']
for img in boss_list:
    boss_img.append(pg.image.load(path.join(img_dir,img)).convert())



player_mini_img = pg.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

bullet_img = []
bullet_list = ['laser.png','laser2.png','laser3.png','laser4.png']
for img in bullet_list:
    bullet_img.append(pg.image.load(path.join(img_dir, img)).convert())




boss_bullet_img = pg.image.load(path.join(img_dir,"red_bullet.png")).convert()


meteor_images = []
meteor_list = ['b1.png', 'b2.png','b3.png','b4.png','m1.png', 'm2.png','m3.png', 's1.png', 's2.png', 't1.png']
for img in meteor_list:
    meteor_images.append(pg.image.load(path.join(img_dir, img)).convert())
#level 2 enemies images
lvl2_enemies_images = []
lvl2_enemies_list = ['lvl2_enemy1.png','lvl2_enemy2.png','lvl2_enemy3.png','lvl2_enemy4.png','lvl2_enemy5.png','lvl2_enemy6.png']
for img in lvl2_enemies_list:
    lvl2_enemies_images.append(pg.image.load(path.join(img_dir, img)).convert())



explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'expl_03_000{}.png'.format(i)
    img = pg.image.load(path.join(amie_dir, filename )).convert()
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img, (45,45))
    explosion_anim['sm'].append(img_sm)
    filename = 'expl_10_000{}.png'.format(i)
    img = pg.image.load(path.join(amie_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pg.image.load(path.join(img_dir, 'shield.png')).convert()
powerup_images['gun'] = pg.image.load(path.join(img_dir, 'lightning.png')).convert()
powerup_images['speed'] = pg.image.load(path.join(img_dir, 'speed.png')).convert()
powerup_images['coin'] = pg.image.load(path.join(img_dir, 'coin.png')).convert()
powerup_images['epic'] = pg.image.load(path.join(img_dir, 'epic.png')).convert()

# load all sounds



gun_sound = pg.mixer.Sound(path.join(snd_dir, 'gun.wav'))
shield_sound = pg.mixer.Sound(path.join(snd_dir, 'shield.wav'))
exp_sound = []
for snd in ['boom.wav', 'kadoosh.wav']:
    exp_sound.append(pg.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pg.mixer.Sound(path.join(snd_dir, 'boom.wav'))
pg.mixer.music.load(path.join(snd_dir, 'backdrop_sound.ogg'))
pg.mixer.music.set_volume(1.0)


pg.mixer.music.play(-1)

shoot_sound = pg.mixer.Sound(path.join(snd_dir, 'shoot.wav'))
shoot_sound.set_volume(1.0)