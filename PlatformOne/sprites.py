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
        self.standing_frames = [self.game.sprite_alien.get_image(70, 0, 66, 92),
                                self.game.sprite_alien.get_image(67, 378, 66, 92)]

        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)

        self.walk_frames_r = [self.game.sprite_alien.get_image(67, 285, 66, 93),
                              self.game.sprite_alien.get_image(0, 356, 67, 96)]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        self.jump_frame = self.game.sprite_alien.get_image(67, 192, 66, 93)
        self.jump_frame.set_colorkey(BLACK)

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
            #self.current_frame = (self.current_frame + 1) % len(self.jump_frame)
            bottom = self.rect.bottom
            self.image = self.jump_frame
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
            if now - self.last_update > 230:
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
	<SubTexture name="dirtCliffLeft.png" x="720" y="720" width="70" height="70"/>
	<SubTexture name="dirtCliffLeftAlt.png" x="720" y="648" width="70" height="70"/>
	<SubTexture name="dirtCliffRight.png" x="720" y="576" width="70" height="70"/>
	<SubTexture name="dirtCliffRightAlt.png" x="720" y="504" width="70" height="70"/>
	<SubTexture name="dirtHalf.png" x="720" y="432" width="70" height="70"/>
	<SubTexture name="dirtHalfLeft.png" x="720" y="360" width="70" height="70"/>
	<SubTexture name="dirtHalfMid.png" x="720" y="288" width="70" height="70"/>
	<SubTexture name="dirtHalfRight.png" x="720" y="216" width="70" height="70"/>
	<SubTexture name="dirtHillLeft.png" x="720" y="144" width="70" height="70"/>
	<SubTexture name="dirtHillLeft2.png" x="720" y="72" width="70" height="70"/>
	<SubTexture name="dirtHillRight.png" x="720" y="0" width="70" height="70"/>
	<SubTexture name="dirtHillRight2.png" x="648" y="864" width="70" height="70"/>
	<SubTexture name="dirtLedgeLeft.png" x="842" y="892" width="5" height="18"/>
	<SubTexture name="dirtLedgeRight.png" x="842" y="912" width="5" height="18"/>
	<SubTexture name="dirtLeft.png" x="504" y="432" width="70" height="70"/>
	<SubTexture name="dirtMid.png" x="504" y="360" width="70" height="70"/>
	<SubTexture name="dirtRight.png" x="648" y="504" width="70" height="70"/>
        '''

        images = [self.game.sprite_tiles.get_image(648,  0,  70, 70),   #0  "grass.png"
                  self.game.sprite_tiles.get_image(576, 864, 70, 70),   #1  "grassCenter.png"
                  self.game.sprite_tiles.get_image(576, 792, 70, 70),   #2  "grassCenter_rounded.png"
                  self.game.sprite_tiles.get_image(576, 720, 70, 70),   #3  "grassCliffLeft.png"
                  self.game.sprite_tiles.get_image(576, 648, 70, 70),   #4  "grassCliffLeftAlt.png"
                  self.game.sprite_tiles.get_image(576, 576, 70, 70),   #5  "grassCliffRight.png"
                  self.game.sprite_tiles.get_image(576, 504, 70, 70),   #6  "grassCliffRightAlt.png"
                  self.game.sprite_tiles.get_image(576, 432, 70, 70),   #7  "grassHalf.png"
                  self.game.sprite_tiles.get_image(576, 360, 70, 70),   #8  "grassHalfLeft.png"
                  self.game.sprite_tiles.get_image(576, 288, 70, 70),   #9  "grassHalfMid.png"
                  self.game.sprite_tiles.get_image(576, 216, 70, 70),   #10  "grassHalfRight.png"
                  self.game.sprite_tiles.get_image(576, 144, 70, 70),   #11  "grassHillLeft.png"
                  self.game.sprite_tiles.get_image(576, 72,  70, 70),   #12  "grassHillLeft2.png"
                  self.game.sprite_tiles.get_image(576, 0,   70, 70),   #13  "grassHillRight.png"
                  self.game.sprite_tiles.get_image(504, 864, 70, 70),   #14  "grassHillRight2.png"
                  self.game.sprite_tiles.get_image(849, 868,  5, 24),   #15  "grassLedgeLeft.png"
                  self.game.sprite_tiles.get_image(849, 894,  5, 24),   #16  "grassLedgeRight.png"
                  self.game.sprite_tiles.get_image(504, 648, 70, 70),   #17  "grassLeft.png"
                  self.game.sprite_tiles.get_image(504, 576, 70, 70),   #18  "grassMid.png"
                  self.game.sprite_tiles.get_image(504, 504, 70, 70),   #19  "grassRight.png"
                  self.game.sprite_tiles.get_image(792, 0,   70, 70),   #20  "dirt.png"
                  self.game.sprite_tiles.get_image(720, 864, 70, 70),   #21 "dirtCenter.png"
                  self.game.sprite_tiles.get_image(720, 792, 70, 70),   #22 "dirtCenter_rounded.png"
                  ]

        self.image = images[type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
