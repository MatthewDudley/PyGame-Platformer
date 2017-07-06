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

    <SubTexture name="playerGreen_dead.png"	x="890"	y="272"	width="38"	height="43" frameX="-0" frameY="-0" frameWidth="38" frameHeight="43"/>
	<SubTexture name="playerGreen_duck.png"	x="650"	y="573"	width="56"	height="31" frameX="-0" frameY="-0" frameWidth="56" frameHeight="31"/>
	<SubTexture name="playerGreen_fall.png"	x="890"	y="316"	width="38"	height="49" frameX="-0" frameY="-0" frameWidth="38" frameHeight="49"/>
	<SubTexture name="playerGreen_hit.png"	x="758"	y="689"	width="46"	height="40" frameX="-0" frameY="-0" frameWidth="46" frameHeight="40"/>
	<SubTexture name="playerGreen_roll.png"	x="849"	y="599"	width="40"	height="40" frameX="-0" frameY="-0" frameWidth="40" frameHeight="40"/>
	<SubTexture name="playerGreen_stand.png"	x="890"	y="0"	width="38"	height="50" frameX="-0" frameY="-0" frameWidth="38" frameHeight="50"/>
	<SubTexture name="playerGreen_swim1.png"	x="849"	y="823"	width="40"	height="53" frameX="-0" frameY="-0" frameWidth="40" frameHeight="53"/>
	<SubTexture name="playerGreen_swim2.png"	x="808"	y="92"	width="41"	height="54" frameX="-0" frameY="-0" frameWidth="41" frameHeight="54"/>
	<SubTexture name="playerGreen_switch1.png"	x="707"	y="508"	width="51"	height="50" frameX="-0" frameY="-0" frameWidth="51" frameHeight="50"/>
	<SubTexture name="playerGreen_switch2.png"	x="707"	y="654"	width="50"	height="50" frameX="-0" frameY="-0" frameWidth="50" frameHeight="50"/>
	<SubTexture name="playerGreen_up1.png"	x="890"	y="51"	width="38"	height="50" frameX="-0" frameY="-0" frameWidth="38" frameHeight="50"/>
	<SubTexture name="playerGreen_up2.png"	x="849"	y="877"	width="38"	height="43" frameX="-0" frameY="-0" frameWidth="38" frameHeight="43"/>
	<SubTexture name="playerGreen_up3.png"	x="849"	y="429"	width="40"	height="39" frameX="-0" frameY="-0" frameWidth="40" frameHeight="39"/>
	<SubTexture name="playerGreen_walk1.png"	x="890"	y="366"	width="38"	height="50" frameX="-0" frameY="-0" frameWidth="38" frameHeight="50"/>
	<SubTexture name="playerGreen_walk2.png"	x="889"	y="963"	width="38"	height="48" frameX="-0" frameY="-0" frameWidth="38" frameHeight="48"/>
	<SubTexture name="playerGreen_walk3.png"	x="889"	y="877"	width="38"	height="48" frameX="-0" frameY="-0" frameWidth="38" frameHeight="48"/>
	<SubTexture name="playerGreen_walk4.png"	x="713"	y="259"	width="48"	height="43" frameX="-0" frameY="-0" frameWidth="48" frameHeight="43"/>
	<SubTexture name="playerGreen_walk5.png"	x="455"	y="642"	width="64"	height="39" frameX="-0" frameY="-0" frameWidth="64" frameHeight="39"/>

        '''

        self.standing_frames = [self.game.spritesheet.get_image(890, 0, 38, 50)]

        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)

        self.walk_frames_r = [self.game.spritesheet.get_image(890, 366, 38, 50),
                              self.game.spritesheet.get_image(889, 963, 38, 48),
                              self.game.spritesheet.get_image(889, 877, 38, 48)]
                              #self.game.spritesheet.get_image(713, 259, 48, 43),
                              #self.game.spritesheet.get_image(455, 642, 64, 39)]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        self.jump_frame = [self.game.spritesheet.get_image(849, 877, 38, 43)]

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
        
    <SubTexture name="tileYellow_01.png"	x="65"	y="574"	width="64"	height="53" frameX="-0" frameY="-0" frameWidth="64" frameHeight="53"/>
	<SubTexture name="tileYellow_02.png"	x="65"	y="520"	width="64"	height="53" frameX="-0" frameY="-0" frameWidth="64" frameHeight="53"/>
	<SubTexture name="tileYellow_03.png"	x="0"	y="964"	width="64"	height="53" frameX="-0" frameY="-0" frameWidth="64" frameHeight="53"/>
	<SubTexture name="tileYellow_04.png"	x="585"	y="260"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_05.png"	x="65"	y="455"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_06.png"	x="65"	y="390"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_07.png"	x="65"	y="325"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_08.png"	x="65"	y="260"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_09.png"	x="65"	y="195"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_10.png"	x="65"	y="130"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_11.png"	x="65"	y="65"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_12.png"	x="65"	y="0"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_13.png"	x="0"	y="899"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_14.png"	x="0"	y="834"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_15.png"	x="0"	y="769"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_16.png"	x="0"	y="704"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_17.png"	x="0"	y="639"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_18.png"	x="0"	y="574"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_19.png"	x="0"	y="509"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_20.png"	x="0"	y="444"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_21.png"	x="0"	y="379"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_22.png"	x="0"	y="314"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_23.png"	x="0"	y="249"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_24.png"	x="0"	y="184"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_25.png"	x="0"	y="119"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_26.png"	x="0"	y="54"	width="64"	height="64" frameX="-0" frameY="-0" frameWidth="64" frameHeight="64"/>
	<SubTexture name="tileYellow_27.png"	x="0"	y="0"	width="64"	height="53" frameX="-0" frameY="-0" frameWidth="64" frameHeight="53"/>
	
        '''


        images = [self.game.spritesheet.get_image(65, 390, 64, 64),
                  self.game.spritesheet.get_image(585, 260, 64, 64)]

        self.image = images[type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
