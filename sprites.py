import pygame as pg
from settings import *
import random

#making a class(player)
class Player(pg.sprite.Sprite):
    def __init__(self,game,option):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.option = option

        if option == 'Earth':
        #we can change the image for the player
            self.image = pg.transform.scale(player_img_list[0], (60,80))
            self.shield = 100

        if option == 'Mercury':
            self.image = pg.transform.scale(player_img_list[1], (60, 80))
            self.shield = 150

        if option == 'Pluto':
            self.image = pg.transform.scale(player_img_list[2], (60, 80))
            self.shield = 200

        if option == 'Saturn':
            self.image = pg.transform.scale(player_img_list[3], (60, 80))
            self.shield = 250

        if option == 'Venus':
            self.image = pg.transform.scale(player_img_list[4], (60, 80))
            self.shield = 300

        if option == 'Mars':
            self.image = pg.transform.scale(player_img_list[5], (60, 80))
            self.shield = 325

        if option == 'Moon':
            self.image = pg.transform.scale(player_img_list[6], (60, 80))
            self.shield = 400

        if option == 'Jupiter':
            self.image = pg.transform.scale(player_img_list[7], (60, 80))
            self.shield = 200

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
            # pg.draw.circle(self.image,RED,self.rect.center,self.radius,1)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 1
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.power = 1
        self.speed_lvl = 1
        self.speed_time = pg.time.get_ticks()
        self.power_time = pg.time.get_ticks()


    #making another function called update
    def update(self):
        #timeout for speedups
        if self.speed_lvl >= 2 and pg.time.get_ticks() - self.speed_time > SPEED_LAST:
            self.speed_lvl -= 1
            self.speed_time = pg.time.get_ticks()
       # timeout for powerups
        if self.power >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pg.time.get_ticks()
        # unhide if hidden
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0

        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            if self.speed_lvl == 1:
                self.speedx = -10
            if self.speed_lvl >= 2:
                self.speedx = -20
        if keystate[pg.K_RIGHT]:
           if self.speed_lvl == 1:
               self.speedx = 10
           if self.speed_lvl >= 2:
               self.speedx = 20
        if keystate[pg.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pg.time.get_ticks()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                if self.option == 'Earth' or 'Saturn' or 'Venus' or 'Moon':
                    blt = Bullet(self.rect.centerx, self.rect.top, 'ball')
                if self.option == 'Mercury' or 'Jupiter' :
                    blt = Bullet(self.rect.centerx, self.rect.top, 'laser')
                if self.option == 'Pluto' or 'Mars' :
                    blt_1 = Bullet(self.rect.left, self.rect.top, 'normal')
                    blt_2 = Bullet(self.rect.right, self.rect.top, 'normal')

                self.game.all_sprites.add(blt_1)
                self.game.all_sprites.add(blt_2)
                self.game.Bullets.add(blt_1)
                self.game.Bullets.add(blt_2)
                self.game.all_sprites.add(blt)
                self.game.Bullets.add(blt)


                shoot_sound.play()
            if self.power >= 2:
                blt1 = Bullet(self.rect.left, self.rect.centery,'ball')
                blt2 = Bullet(self.rect.right, self.rect.centery,'ball')
                blt3 = Bullet(self.rect.centerx, self.rect.centery,'ball')
                self.game.all_sprites.add(blt1)
                self.game.all_sprites.add(blt2)
                self.game.all_sprites.add(blt3)
                self.game.Bullets.add(blt1)
                self.game.Bullets.add(blt2)
                self.game.Bullets.add(blt3)
                shoot_sound.play()

    def hide(self):
        # hide the player temporary
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def speedup(self):
        self.speed_lvl += 1
        self.speed_time = pg.time.get_ticks()
        
#made a class called bullet
class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,option):
        pg.sprite.Sprite.__init__(self)
        self.option = option
        if option == 'normal':
        #we are going to make an image for our bullets'
            self.image = pg.transform.scale(bullet_img[0], (10,40))

        if option == 'laser':
            self.image = pg.transform.scale(bullet_img[1], (10, 10))
            self.image.set_colorkey(WHITE)

        if option == 'ball':
            self.image = pg.transform.scale(bullet_img[3], (10, 10))
            self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        if self.option == 'normal':
            self.rect.y += self.speedy
        if self.option == 'laser':
            self.rect.y += self.speedy
        if self.option == 'ball':
            self.rect.y += self.speedy

            if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left> WIDTH:
                self.kill()




#made a class called power
class Power(pg.sprite.Sprite):
    def __init__(self,center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'speed', 'coin', 'epic'])
        self.image = powerup_images[self.type]
        self.image = pg.transform.scale(self.image,(50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 7
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()



#we made a class called mob
class mob(pg.sprite.Sprite):
    def __init__(self,level):
        pg.sprite.Sprite.__init__(self)
        self.level = level
        #mob for level 1
        if self.level == 1:
            # we made an image for the enemies
            self.image_orig = random.choice(meteor_images)
        # mob for level 2
        if self.level == 2:
             # we made an image for the enemies
            self.image_orig = random.choice(lvl2_enemies_images)

        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image,RED,self.rect.center, self.radius,1)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-3, 3)
        self.turn = 0
        self.turn_speed = random.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 5:
            self.last_update = now
            self.turn = (self.turn + self.turn_speed) % 360
            new_image = pg.transform.rotate(self.image_orig,self.turn)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def update(self):
        if self.level == 1:
            self.rotate()
        else:
            pass
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 5 or self.rect.left < -25 or self.rect.right > WIDTH +20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)

#made a class called explosion
class explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Boss(pg.sprite.Sprite):
    def __init__(self,game,level):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.level = level
        if self.level == 1:
            self.image = pg.transform.scale(boss_img[0],(300,300))
        if self.level == 2:
            self.image = pg.transform.scale(boss_img[1],(300,300))
        if self.level == 3:
            self.image = pg.transform.scale(boss_img[2],(300,300))
        if self.level == 4:
            self.image = pg.transform.scale(boss_img[3],(300,300))

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 4
        self.last_update = pg.time.get_ticks()
        self.last_shot = pg.time.get_ticks()
        self.speedx = 10
        self.boss_hp = 100
        self.boss_shoot_stop = 250

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 20:
            self.last_update = now
            self.rect.x += self.speedx
            if self.rect.left  < 0:
                self.speedx = random.randrange(5,15)
            if self.rect.right > WIDTH:
                self.speedx = random.randrange(-15,-5)
        if now - self.last_shot > 200:
            self.last_shot = now
            self.shoot(    )
    def shoot(self):
        if self.game.boss_event:
            bullet = Boss_Bullet(self.rect.centerx,self.rect.centery)
            bullet2 = Boss_Bullet(self.rect.centerx,self.rect.centery)
            self.game.boss_group.add(bullet)
            self.game.boss_group.add(bullet2)
            self.game.Boss_bullets.add(bullet)
            self.game.Boss_bullets.add(bullet2)


# made a class called bboss_bullet
class Boss_Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
            pg.sprite.Sprite.__init__(self)
            # we are going to make an image for our bullets'
            self.image = pg.transform.scale(boss_bullet_img, (30,30))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y
            self.speedy = random.randrange(5,25)
            self.speedx = random.randrange(-25,25)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom > HEIGHT:
            self.kill()
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.kill()






