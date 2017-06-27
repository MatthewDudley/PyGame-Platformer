# game options/settings

TITLE = "Jumpy!"
WIDTH = 600
HEIGHT = 500
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"

# player props
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.11
PLAYER_GRAV = 1
PLAYER_JUMP = -15

# start platforms (x, y, w, h)
PLATFORM_LIST = [(50, 400, WIDTH - 100, 20),
                 (170, 300, 100,20),
                 (375, 200, 100, 20 ),
                 (HEIGHT + 200, 350, 300, 20)]


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (65, 190, 244)
BGCOLOR = LIGHTBLUE