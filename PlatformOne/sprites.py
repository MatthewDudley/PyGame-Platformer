# Sprite class for platform game

import pygame as pg
from settings import *
vec = pg.math.Vector2

class Spritesheet:
    # utility for loading sprites
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of larger spritesheet
        image = pg.Surface((width,height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        #image = pg.transform.scale(image, ((width // 4)*3, (height // 4)*3))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT*(3/4))
        self.pos = vec(40, HEIGHT*(3/4))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def load_images(self):

        '''

    <SubTexture name="playerGrey_dead.png"	x="890"	y="759"	width="36"	height="39" frameX="-0" frameY="-0" frameWidth="36" frameHeight="39"/>
	<SubTexture name="playerGrey_duck.png"	x="650"	y="808"	width="56"	height="30" frameX="-0" frameY="-0" frameWidth="56" frameHeight="30"/>
	<SubTexture name="playerGrey_fall.png"	x="890"	y="616"	width="36"	height="45" frameX="-0" frameY="-0" frameWidth="36" frameHeight="45"/>
	<SubTexture name="playerGrey_hit.png"	x="710"	y="427"	width="49"	height="36" frameX="-0" frameY="-0" frameWidth="49" frameHeight="36"/>
	<SubTexture name="playerGrey_roll.png"	x="890"	y="102"	width="36"	height="36" frameX="-0" frameY="-0" frameWidth="36" frameHeight="36"/>
	<SubTexture name="playerGrey_stand.png"	x="890"	y="799"	width="36"	height="45" frameX="-0" frameY="-0" frameWidth="36" frameHeight="45"/>
	<SubTexture name="playerGrey_swim1.png"	x="805"	y="823"	width="43"	height="41" frameX="-0" frameY="-0" frameWidth="43" frameHeight="41"/>
	<SubTexture name="playerGrey_swim2.png"	x="805"	y="656"	width="44"	height="42" frameX="-0" frameY="-0" frameWidth="44" frameHeight="42"/>
	<SubTexture name="playerGrey_switch1.png"	x="707"	y="705"	width="50"	height="45" frameX="-0" frameY="-0" frameWidth="50" frameHeight="45"/>
	<SubTexture name="playerGrey_switch2.png"	x="707"	y="608"	width="50"	height="45" frameX="-0" frameY="-0" frameWidth="50" frameHeight="45"/>
	<SubTexture name="playerGrey_up1.png"	x="927"	y="578"	width="36"	height="45" frameX="-0" frameY="-0" frameWidth="36" frameHeight="45"/>
	<SubTexture name="playerGrey_up2.png"	x="890"	y="537"	width="37"	height="40" frameX="-0" frameY="-0" frameWidth="37" frameHeight="40"/>
	<SubTexture name="playerGrey_up3.png"	x="764"	y="55"	width="44"	height="36" frameX="-0" frameY="-0" frameWidth="44" frameHeight="36"/>
	<SubTexture name="playerGrey_walk1.png"	x="927"	y="791"	width="36"	height="45" frameX="-0" frameY="-0" frameWidth="36" frameHeight="45"/>
	<SubTexture name="playerGrey_walk2.png"	x="890"	y="417"	width="37"	height="43" frameX="-0" frameY="-0" frameWidth="37" frameHeight="43"/>
	<SubTexture name="playerGrey_walk3.png"	x="890"	y="494"	width="37"	height="42" frameX="-0" frameY="-0" frameWidth="37" frameHeight="42"/>
	<SubTexture name="playerGrey_walk4.png"	x="713"	y="343"	width="48"	height="36" frameX="-0" frameY="-0" frameWidth="48" frameHeight="36"/>
	<SubTexture name="playerGrey_walk5.png"	x="455"	y="682"	width="64"	height="36" frameX="-0" frameY="-0" frameWidth="64" frameHeight="36"/>

        '''

        self.standing_frames = [self.game.spritesheet.get_image(890, 799, 36, 45)]

        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)

        self.walk_frames_r = [self.game.spritesheet.get_image(927, 791, 36, 45),
                              self.game.spritesheet.get_image(890, 417, 37, 43),
                              self.game.spritesheet.get_image(890, 494, 37, 42)]
                              #self.game.spritesheet.get_image(713, 343, 48, 36),]
                              #self.game.spritesheet.get_image(455, 682, 64, 36)]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        self.jump_frame = [self.game.spritesheet.get_image(890, 537, 37, 40)]

        self.jump_frame_l = []
        for frame in self.jump_frame:
            frame.set_colorkey(BLACK)
            self.jump_frame_l.append(pg.transform.flip(frame, True, False))

    def jump(self):
        now = pg.time.get_ticks()
        # jump only if platform is below
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_snd.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.jump_frame)
            bottom = self.rect.bottom
            print(self.vel.x )
            if self.vel.x >= 0:
                self.image = self.jump_frame[0]
            else:
                self.image = self.jump_frame_l[0]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # walking
        if self.walking and not self.jumping:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # idle
        if not self.jumping and not self.walking:
            if now - self.last_update > 400:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        '''
        
    <SubTexture name="tileBlue_01.png"	x="390"	y="636"	width="64"	height="50" frameX="-0" frameY="-0" frameWidth="64" frameHeight="50"/>
	<SubTexture name="tileBlue_02.png"	x="390"	y="585"	width="64"	height="50" frameX="-0" frameY="-0" frameWidth="64" frameHeight="50"/>
	<SubTexture name="tileBlue_03.png"	x="390"	y="520"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_04.png"	x="390"	y="455"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_05.png"	x="390"	y="390"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_06.png"	x="390"	y="325"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_07.png"	x="390"	y="260"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_08.png"	x="390"	y="195"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_09.png"	x="390"	y="130"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_10.png"	x="390"	y="65"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_11.png"	x="390"	y="0"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_12.png"	x="325"	y="947"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_13.png"	x="325"	y="882"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_14.png"	x="325"	y="817"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_15.png"	x="325"	y="752"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_16.png"	x="325"	y="687"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_17.png"	x="325"	y="622"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_18.png"	x="325"	y="557"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_19.png"	x="325"	y="492"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_20.png"	x="390"	y="882"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_21.png"	x="325"	y="362"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_22.png"	x="325"	y="297"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_23.png"	x="325"	y="232"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_24.png"	x="325"	y="167"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_25.png"	x="325"	y="102"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileBlue_26.png"	x="325"	y="51"	width="64"	height="50" frameX="-0" frameY="-0" frameWidth="64" frameHeight="50"/>
	<SubTexture name="tileBlue_27.png"	x="325"	y="0"	width="64"	height="50" frameX="-0" frameY="-0" frameWidth="64" frameHeight="50"/>

        
        '''


        images = [self.game.spritesheet.get_image(390, 390, 64, 64),
                  self.game.spritesheet.get_image(390, 520, 64, 64)]

        self.image = images[type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
