# game options/settings
import random

TITLE = "GAME TITLE"
WIDTH = 600
HEIGHT = 500
FPS = 60
FONT_NAME = "arial"
HS_FILE = "highscore.txt"

# spritesheets
SPRITESHEET_ALIENS = "aliensBlue.png"
SPRITESHEET_ENEMIES = "enemies.png"
SPRITESHEET_ITEMS = "items_spritesheet.png"
SPRITESHEET_TILES = "tiles_spritesheet.png"

# start screen
MOVE_TEXT = "Arrows keys to move, Space to jump "
DIR_TEXT = "PRESS ANY KEY "
HS_TEXT = "HIGH SCORE HERE "

# game over screen
GO_TEXT = "GAME OVER "
SCORE_TEXT = "Score: "

# player props
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.11
PLAYER_GRAV = 1
PLAYER_JUMP = -15

# start platform(s) (x, y, w, h)
PLATFORM_LIST = [(0,HEIGHT*(3/4), WIDTH-300, HEIGHT+1 - HEIGHT/3)]


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (65, 190, 244)
BGCOLOR = (247, 177, 177)