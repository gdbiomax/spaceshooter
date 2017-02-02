import pygame as pg
from settings import *
from sprites import *
from os import path
from shop import *


class Game:

    def __init__(self):
        # create window and initiliaze pygame
        pg.init()
        pg.mixer.init()
        self.start = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("neil's game")
        self.time = pg.time.Clock()
        self.game_over = False
        self.start_scr = True
        self.playing = False
        self.running = True
        self.score = 0
        self.selection = 0
        self.hs_list = self.load_highscore()
        self.level = 1
        self.boss_event = False

        #screen rolling initialization,need to blit two backdrop which needs two sets of coordination
        self.x1 = 0
        self.y1 = -HEIGHT
        self.x2 = 0
        self.y2 = 0

    def load_highscore(self):
        hs_data = []
        with open('score.txt','rt') as f:
            for line in f:
                hs_data.append(line.strip())
        return hs_data


    def new(self):

        self.all_sprites = pg.sprite.Group()
        self.Bullets = pg.sprite.Group()
        self.Boss_bullets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.boss_group = pg.sprite.Group()

        #crate a new player
        self.player = Player(self,option_list[self.selection])
        self.all_sprites.add(self.player)
        self.boss = Boss(self, self.level)
        self.boss_group.add(self.boss)

        # a loop for spawning enemies(40)
        for i in range(self.level*10+5):
            self.newmob()


 ######################################################################################################################
            #main game loop start from here
    def run(self):
        # keep loop running at the correct speed
        self.time.tick(FPS)
        self.event()
        self.update()
        self.draw()
    def event(self):
        # process input (event)
        for event in pg.event.get():
            # scan for closing window
            if event.type == pg.QUIT:
                self.running = False
            #call pause function
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.show_pause_screen()

        if self.start_scr:
            self.show_start_screen()
            self.start_scr = False
            self.game_over = False
            self.player.lives = 3
        if self.game_over:
            self.show_go_screen()
            self.start_scr = True
            self.game_over = True

        if self.level == 1:
            if self.score > 1000 and not self.boss_event:
                self.boss_event = True
                print("alive")
        if self.level == 2:
            if self.score > 2000 and not self.boss_event:
                self.boss_event = True
                print("alive")

    def update(self):

        self.bullet_hit_mob()
        self.player_hit_enemies()
        self.player_powerup()
        if self.boss_event and self.boss.alive():
            self.bossbullet_hit_player()
            self.bullet_hit_boss()
        # update

        self.all_sprites.update()
        self.boss_group.update()
        self.enemies.update()

    def draw(self):
        # render/draw
        self.screen.fill(BLACK)

    ####################################################################################################
       # Screen rollling
        self.screen.blit(background, (self.x1,self.y1))
        self.screen.blit(background, (self.x2,self.y2))

        self.y1 += BackDrop_rolling_Speed + 3
        self.y2 += BackDrop_rolling_Speed + 3

        if self.y1 >= HEIGHT:
            self.y1 = self.y2 -HEIGHT
        if self.y2 >= HEIGHT:
            self.y2 = self.y1-HEIGHT

    ##################################################################################################
        if not self.boss_event:
            self.enemies.draw(self.screen)
        else:
            self.all_sprites.remove(self.enemies)
            self.enemies.empty()
            self.hit = self.player_powerup()
            self.boss_group.draw(self.screen)
            self.draw_boss_hp_bar(self.screen, self.boss.rect.x + 100, self.boss.rect.y * 25, self.boss.boss_hp)



        self.draw_lives(self.screen, WIDTH - 100, 5, self.player.lives, player_mini_img)
        self.draw_shield_bar(self.screen, 5, 5, self.player.shield)
        self.draw_text(self.screen, str(self.score), 20, WIDTH / 2, 10)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
                                    #main game loop end at here
######################################################################################################################


    def draw_text(self,surf, text, size, x, y):
        font = pg.font.Font(font_type, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    # def functions(newmob, draw_shield, draw_lives)
    def newmob(self):
        m = mob(self.level)
        self.all_sprites.add(m)
        self.enemies.add(m)

    def draw_shield_bar(self,surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(surf, GREEN, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_boss_hp_bar(self,surf, x, y, pct):
        if self.boss.alive():
            if pct < 0:
                pct = 0
            BAR_LENGTH = 100
            BAR_HEIGHT = 10
            fill = (pct / 100) * BAR_LENGTH
            outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
            fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
            pg.draw.rect(surf, RED, fill_rect)
            pg.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_lives(self,surf, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            surf.blit(img, img_rect)


    def bullet_hit_mob(self):
        # check to see if a bullet hit a mob
        hits = pg.sprite.groupcollide(self.enemies, self.Bullets, True, True)
        for hit in hits:
            random.choice(exp_sound).set_volume(1.0)
            random.choice(exp_sound).play()
            self.score += 50 - hit.radius
            # hits += 50 - hit.radius
            expl = explosion(hit.rect.center, 'lg')
            self.all_sprites.add(expl)
            if random.random() > 0.95:
                pow = Power(hit.rect.center)
                self.all_sprites.add(pow)
                self.powerups.add(pow)
            self.newmob()
    def bullet_hit_boss(self):
        # check to see if bullet hit boss
        if self.boss.alive() and self.boss_event:0
        hits = pg.sprite.spritecollide(self.boss, self.Bullets, True, pg.sprite.collide_circle)
        for hit in hits:
                self.boss.boss_hp -= hit.radius * 0.02
                if self.boss.boss_hp <= 0:
                    self.boss.kill()
                    self.boss_event = False
                    self.level += 1
                    self.show_level_finished_screen()
    def player_hit_enemies(self):
        # check to see if player collides with enemy
        hits = pg.sprite.spritecollide(self.player, self.enemies, True, pg.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= hit.radius * 1.2
            expl = explosion(hit.rect.center, 'lg')
            self.all_sprites.add(expl)
            self.newmob()
            if self.player.shield <= 0:
                player_die_sound.play()
                self.death_explosion = explosion(self.player.rect.center, 'player')
                self.all_sprites.add(self.death_explosion)
                self.player.hide()
                self.player.lives -= 1
                self.player.shield = 100
        if self.player.lives == 0 and not self.death_explosion.alive() and self.game_over == False:
            self.game_over = True

    def bossbullet_hit_player(self):
        # check if boss bullet hit player
        hits = pg.sprite.spritecollide(self.player, self.Boss_bullets, True, pg.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= hit.radius * 1.1
            expl = explosion(hit.rect.center, 'lg')
            self.all_sprites.add(expl)
            if self.player.shield <= 0:
                player_die_sound.play()
                self.death_explosion = explosion(self.player.rect.center, 'player')
                self.all_sprites.add(self.death_explosion)
                self.player.hide()
                self.player.lives -= 1
                self.player.shield = 100
        # if player has died and explosion had finished
        if self.player.lives == 0 and not self.death_explosion.alive() and self.game_over == False:
            self.game_over = True
    def player_powerup(self):
        # check to see if player obtain power up
        hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                self.player.shield += random.randrange(5, 15)
                shield_sound.play()
                if self.player.shield >= 100:
                    self.player.shield = 100
            if hit.type == 'gun':
                self.player.powerup()
                gun_sound.play()

            if hit.type == 'speed':
                self.player.speedup()
                gun_sound.play()
            if hit.type == 'coin':
                shield_sound.play()
                self.score += random.randrange(500, 1000)
            if hit.type == 'epic':
                shield_sound.play()
                self.player.speedup()
                self.player.powerup()
                self.score += random.randrange(50, 100)
                self.player.shield += 10
                if self.player.shield >= 100:
                    self.player.shield = 100
        return hits

    # def functions for showing game over and start screen
    def show_go_screen(self):
        self.screen.blit(background, background_rect)
        self.draw_text(self.screen, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "press any key to go to start", 18, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        waiting = True
        while waiting:
            self.time.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        self.screen.blit(menu_background, menu_background_rect)
        button_select = Button('button_temp.png','SELECTION',20,self.screen,132,530)
        button_left = Button('left.png',"",0,self.screen,50,485)
        button_right = Button('right.png', "", 0, self.screen, 300, 485)
        button_newgame = Button('button_temp.png','New Game',20,self.screen,500,380)
        button_help = Button('button_temp.png','  Help',20,self.screen,500,450)
        button_highscore = Button('button_temp.png','High Score',18,self.screen,500,520)
        self.browse = Item()
        self.scale = (140,180)
        waiting = True
        while waiting:
            self.time.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pg.mouse.get_pos()
                    if button_left.rect.collidepoint(pos):
                        button_left.update()
                        self.selection -= 1
                    if button_right.rect.collidepoint(pos):
                        button_right.update()
                        self.selection += 1
                    if button_select.rect.collidepoint(pos):
                        button_select.toggle = -button_select.toggle
                        button_select.update()
                        self.screen.blit(menu_cover, (590, 80))
                        self.screen.blit(self.browse.image, (650, 110))
                    if button_newgame.rect.collidepoint(pos):
                        waiting = False
                        self.playing = True
                    if button_help.rect.collidepoint(pos):
                        self.show_help_screen()
                        waiting = False
                    if button_highscore.rect.collidepoint(pos):
                        self.show_high_score_screen()
                        waiting = False
                    if self.selection < 0:
                        self.selection = 7
                    if self.selection > 7:
                        self.selection = 0
                if event.type == pg.QUIT:
                    waiting = False
                    pg.quit()

            self.browse.image = player_img_list[self.selection]
            self.browse.image = pg.transform.scale(self.browse.image, self.scale)
            self.browse.image.set_colorkey(BLACK)
            #make a cover surface for image update
            cover_surface = pg.Surface(self.scale)
            cover_surface.fill(BLACK)
            self.screen.blit(cover_surface, (140, 145))

            self.screen.blit(self.browse.image, (140, 145))
            self.screen.blit(description_list[self.selection], (45, 330))
            pg.display.flip()
            self.all_sprites.remove(self.player)
            self.player = Player(self,option_list[self.selection])
            self.all_sprites.add(self.player)
            self.all_sprites.update()

    def show_help_screen(self):
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    pg.quit()
            keyState = pg.key.get_pressed()
            if keyState[pg.K_ESCAPE]:
                waiting = False
                self.show_start_screen()
            help_screen = pg.display.set_mode((WIDTH,HEIGHT))
            help_screen.fill(BLACK)
            self.draw_text(help_screen,"Help",40,WIDTH/2,20)
            self.draw_text(help_screen, "Press Escape Key to Return", 40, WIDTH / 2, 80)
            pg.display.flip()

    def show_high_score_screen(self):
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    pg.quit()
            keyState = pg.key.get_pressed()
            if keyState[pg.K_ESCAPE]:
                waiting = False
                self.show_start_screen()
            help_screen = pg.display.set_mode((WIDTH, HEIGHT))
            help_screen.fill(BLACK)
            self.draw_text(help_screen, "High Score", 40, WIDTH / 2, 20)
            for i in range(len(self.hs_list)):
                self.draw_text(help_screen,self.hs_list[i],30,WIDTH/2,80+i*40)
            self.draw_text(help_screen, "Press Escape Key to Return", 40, WIDTH / 2, 480)
            pg.display.flip()

    def show_pause_screen(self):
        pause = True
        while pause:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pause = False
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pg.mouse.get_pos()
                    if button_continue.rect.collidepoint(pos):
                        button_continue.update()
                        pause = False
                    if button_exit.rect.collidepoint(pos):
                        button_exit.update()
                        pause = False
                        self.playing = False
                        self.show_start_screen()
            keyState = pg.key.get_pressed()
            if keyState[pg.K_ESCAPE]:
                pause = False
            self.draw_text(self.screen, "Pause", 40, WIDTH / 2, 20)
            self.draw_text(self.screen, "Press Escape Key to Continue", 40, WIDTH / 2, 80)
            button_continue = Button('button_temp.png','Continue',20,self.screen,WIDTH/2-100, 200)
            button_exit = Button('button_temp.png',' Exit',20,self.screen,WIDTH/2-100, 300)

            pg.display.update()

    def show_level_finished_screen(self):
        pause = True
        while pause:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pause = False
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pause = False
                if event.type == pg.mouse.get_pressed() and event.key == 1:
                    pass

            self.draw_text(self.screen,'Congratulation!',80,WIDTH/2,HEIGHT/2)
            pg.display.update()



g = Game()
g.new()
while g.running and g.level == 1:
    g.run()
g.new()
while g.running and g.level == 2:
    g.run()
g.new()
while g.running and g.level == 3:
    g.run()
#quit pygame
pg.quit()