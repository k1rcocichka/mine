"""Конфиг игры"""

# Размеры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 16
GRID_HEIGHT = 16
MINES_COUNT = 40
PANEL_HEIGHT = 60

# Цвета
BACKGROUND = (200, 200, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Состояния клетки
HIDDEN = 0
OPENED = 1
FLAGGED = 2
QUESTION = 3

# Цвета цифр
NUMBER_COLORS = {
    1: BLUE,
    2: GREEN,
    3: RED,
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: BLACK,
    8: DARK_GRAY
}