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
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = self.game.sprite_alien.get_image(676,368,66,92)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec((WIDTH/2), (HEIGHT/2))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def jump(self):
        # jump only if platform is below
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = PLAYER_JUMP

    def update(self):
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

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y