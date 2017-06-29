import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:

    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()


    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load spritesheets
                self.sprite_alien = Spritesheet(path.join(img_dir, SPRITESHEET_ALIENS))
                self.sprite_enemies = Spritesheet(path.join(img_dir, SPRITESHEET_ENEMIES))
                self.sprite_items = Spritesheet(path.join(img_dir, SPRITESHEET_ITEMS))
                self.sprite_tiles = Spritesheet(path.join(img_dir, SPRITESHEET_TILES))


    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
           p = Platform(self, *plat)
           self.all_sprites.add(p)
           self.platforms.add(p)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0

        # Camera movement forward
        if self.player.rect.right > ((2 / 3) * WIDTH):
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.right -= abs(self.player.vel.x)
                #if plat.rect.top >= WIDTH:
                #    plat.kill()

        # Camera move up

        # Camera movement Backwards
        if self.player.rect.left <= ((1 / 8) * WIDTH):
            self.player.pos.x -= self.player.vel.x


        # die
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False


    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()


    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()


    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(MOVE_TEXT, 24, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(DIR_TEXT, 24, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text(HS_TEXT + str(self.highscore), 24, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()


    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text(GO_TEXT, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(SCORE_TEXT + str(self.score), 24, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(DIR_TEXT, 24, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 24, WHITE, WIDTH/2, HEIGHT/2 + 40 )
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("Highscore: " + str(self.highscore), 24, WHITE, WIDTH / 2, HEIGHT/2 +40)

        pg.display.flip()
        self. wait_for_key()


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


    def draw_text(self, text, size, color, x,y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()