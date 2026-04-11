import pygame

# --- Screen ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Math Jungle"

# --- Colors ---
WHITE       = (255, 255, 255)
BLACK       = (0,   0,   0)
GREEN_DARK  = (34,  85,  34)
GREEN_MID   = (60,  140,  60)
GREEN_LIGHT = (120, 200,  80)
YELLOW      = (255, 220,  50)
GOLD        = (255, 185,  15)
ORANGE      = (230, 130,  30)
RED         = (210,  50,  50)
BLUE_LIGHT  = (130, 190, 255)
BROWN       = (120,  75,  30)
CREAM       = (255, 245, 210)
GREY        = (180, 180, 180)
DARK_PANEL  = (20,  60,  20)

# --- Game states ---
STATE_MENU         = "menu"
STATE_LEVEL_SELECT = "level_select"
STATE_PLAYING      = "playing"

# --- Difficulty levels ---
# Each level: (name, emoji-label, operations, max_number, description)
LEVELS = {
    1: {
        "name": "Cub",
        "ops": ["+"],
        "max_num": 10,
        "desc": "Addition up to 10",
    },
    2: {
        "name": "Explorer",
        "ops": ["+", "-"],
        "max_num": 20,
        "desc": "Add & subtract up to 20",
    },
    3: {
        "name": "Adventurer",
        "ops": ["+", "-", "*"],
        "max_num": 50,
        "tables_max": 5,
        "desc": "Mixed with x-tables up to 5",
    },
    4: {
        "name": "Hunter",
        "ops": ["+", "-", "*", "/"],
        "max_num": 100,
        "tables_max": 10,
        "desc": "All ops, x-tables up to 10",
    },
    5: {
        "name": "Jungle King",
        "ops": ["+", "-", "*", "/"],
        "max_num": 999,
        "tables_max": 12,
        "desc": "Big numbers, all operations",
    },
}

# --- Coins ---
COINS_CORRECT_FIRST  = 3   # correct on first attempt
COINS_CORRECT_SECOND = 1   # correct on second attempt
COINS_STREAK_BONUS   = 5   # awarded every 5 correct in a row
STREAK_MILESTONE     = 5

# --- Fonts (loaded at runtime) ---
FONT_LARGE  = None
FONT_MEDIUM = None
FONT_SMALL  = None

def load_fonts():
    global FONT_LARGE, FONT_MEDIUM, FONT_SMALL
    FONT_LARGE  = pygame.font.SysFont("Arial", 64, bold=True)
    FONT_MEDIUM = pygame.font.SysFont("Arial", 36, bold=True)
    FONT_SMALL  = pygame.font.SysFont("Arial", 24)
