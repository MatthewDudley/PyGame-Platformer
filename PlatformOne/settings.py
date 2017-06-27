# game options/settings
import random

TITLE = "GAME TITLE"
WIDTH = 600
HEIGHT = 500
FPS = 60
FONT_NAME = "arial"
HS_FILE = "highscore.txt"

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

# start platforms (x, y, w, h)
PLATFORM_LIST = [(50, 400, WIDTH - 100, 20),
                 (170, 300, 100,20)]

PLAT_X_RANGE = random.randrange(WIDTH/2, WIDTH)
PLAT_Y_RANGE = random.randrange(200,450)
PLAT_W_RANGE = random.randrange(50,200)
PLAT_H_RANGE = random.randrange(15,25)

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (65, 190, 244)
BGCOLOR = LIGHTBLUE