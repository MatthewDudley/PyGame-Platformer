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
        image = pg.transform.scale(image, ((width // 4)*3, (height // 4)*3))
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
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec((WIDTH/4), HEIGHT*(3/4))
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
        # jump only if platform is below
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = PLAYER_JUMP

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
        self.pos += self.vel + 0.5 * self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # walking
        if self.walking:
            if now - self.last_update > 200:
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
            if now - self.last_update > 390:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        images = [self.game.sprite_alien.get_image(648,  0,  70, 70),   #"grass.png"
                  self.game.sprite_alien.get_image(576, 864, 70, 70),   #"grassCenter.png"
                  self.game.sprite_alien.get_image(576, 792, 70, 70),   #"grassCenter_rounded.png"
                  self.game.sprite_alien.get_image(576, 720, 70, 70),   #"grassCliffLeft.png"
                  self.game.sprite_alien.get_image(576, 648, 70, 70),   #"grassCliffLeftAlt.png"
                  self.game.sprite_alien.get_image(576, 576, 70, 70),   #"grassCliffRight.png"
                  self.game.sprite_alien.get_image(576, 504, 70, 70),   #"grassCliffRightAlt.png"
                  self.game.sprite_alien.get_image(576, 432, 70, 70),   #"grassHalf.png"
                  self.game.sprite_alien.get_image(576, 360, 70, 70),   #"grassHalfLeft.png"
                  self.game.sprite_alien.get_image(576, 288, 70, 70),   #"grassHalfMid.png"
                  self.game.sprite_alien.get_image(576, 216, 70, 70),   #"grassHalfRight.png"
                  self.game.sprite_alien.get_image(576, 144, 70, 70),   #"grassHillLeft.png"
                  self.game.sprite_alien.get_image(576, 72,  70, 70),   #"grassHillLeft2.png"
                  self.game.sprite_alien.get_image(576, 0,   70, 70),   #"grassHillRight.png"
                  self.game.sprite_alien.get_image(504, 864, 70, 70),   #"grassHillRight2.png"
                  self.game.sprite_alien.get_image(849, 868,  5, 24),   #"grassLedgeLeft.png"
                  self.game.sprite_alien.get_image(849, 894,  5, 24),   #"grassLedgeRight.png"
                  self.game.sprite_alien.get_image(504, 648, 70, 70),   #"grassLeft.png"
                  self.game.sprite_alien.get_image(504, 576, 70, 70),   #"grassMid.png"
                  self.game.sprite_alien.get_image(504, 504, 70, 70)]    #"grassRight.png"

        self.image = images[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y