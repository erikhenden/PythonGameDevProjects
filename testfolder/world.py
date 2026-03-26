from dataclasses import dataclass
from random import randint, choices
from settings import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE
import pygame

# Tile type constants
AIR = 0
WALL = 1
DIRT = 2
STONE = 3
IRON = 4
COAL = 5
GOLD = 6
DIAMOND = 7

tile_types =    [AIR,   WALL,   DIRT,   STONE,  IRON,   COAL,   GOLD,   DIAMOND]
weights =       [15,    50,     10,     10,     4,      8,      2,      1]

# Tile types dataclass
@dataclass
class Tile:
    hardness: int
    color: tuple

# Tile data dict
TILE_DATA = {
    AIR:        Tile(hardness=0,        color=(20, 20, 20)),
    WALL:       Tile(hardness=999,      color=(80, 80, 80)),
    DIRT:       Tile(hardness=1,        color=(139, 90, 43)),
    STONE:      Tile(hardness=3,        color=(120, 120, 120)),
    IRON:       Tile(hardness=5,        color=(180, 130, 90)),
    COAL:       Tile(hardness=2,        color=(180, 180, 180)),
    GOLD:       Tile(hardness=6,        color=(255, 215, 0)),
    DIAMOND:    Tile(hardness=8,        color=(100, 220, 220))
  }

# World grid-map
WORLD_GRID = [
    [choices(tile_types, weights)[0] for _ in range(GRID_WIDTH)]
    for _ in range(GRID_HEIGHT)
]

def draw(screen):
    for row in range(GRID_HEIGHT):
        for column in range(GRID_WIDTH):
            tile_type = WORLD_GRID[row][column]
            color = TILE_DATA[tile_type].color
            rect = pygame.Rect(column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)