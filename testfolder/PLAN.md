# Cave Mining Game — Implementation Plan

## Overview
A 2D **top-down** cave exploration game where the player moves around a procedurally generated cave, mines blocks, and gathers resources.

**Approach:** The developer (you) writes the code. Claude provides step-by-step guidance — explaining concepts, suggesting what to write next, reviewing your code, and helping debug. Each phase is broken into small, focused tasks so you always know exactly what to tackle next.

---

## Core Features

### 1. World / Map
- Tile-based grid representing the cave
- Tile types:
  - `AIR` — empty, walkable
  - `WALL` — solid rock, impassable
  - `DIRT` — mineable, yields dirt
  - `STONE` — mineable, yields stone
  - `COAL` — mineable, yields coal
  - `IRON` — mineable, yields iron ore
  - `GOLD` — mineable, yields gold ore
  - `GEM` — mineable, yields gems (rare)
- Cave generation using cellular automata
- Camera that follows the player (scrolling viewport)

### 2. Player
- Colored rectangle (placeholder) with WASD movement
- Collision detection against solid tiles
- Mining action triggered by mouse click on adjacent tile
- Inventory to hold gathered resources

### 3. Mining Mechanic
- Player targets the tile under the mouse cursor
- Holding left click drains a progress bar on the tile
- When progress hits 100%, tile breaks and drops a resource
- Different tiles have different hardness values

### 4. Inventory System
- List-based inventory with stacking (e.g., 12x Stone)
- Displayed on screen, toggled with `E`

### 5. Resources & Items
| Resource | Source Tile | Rarity    |
|----------|-------------|-----------|
| Dirt     | DIRT        | Common    |
| Stone    | STONE       | Common    |
| Coal     | COAL        | Common    |
| Iron Ore | IRON        | Uncommon  |
| Gold Ore | GOLD        | Rare      |
| Gem      | GEM         | Very Rare |

### 6. Tools (stretch goal)
- Pickaxe tiers: Wood → Stone → Iron → Gold
- Higher tier = faster mining + can break harder tiles

---

## Technical Architecture

```
testfolder/
├── game.py           # Entry point, game loop
├── settings.py       # Constants (tile size, screen size, colors, speeds)
├── world.py          # World grid, tile definitions, cave generation
├── player.py         # Player class: movement, collision, mining
├── inventory.py      # Inventory data and UI
├── camera.py         # Camera / viewport offset
└── ui.py             # HUD: inventory panel, mining progress bar
```

---

## Implementation Roadmap

Each step is a small, self-contained task. Complete one before moving to the next.

---

### Phase 1 — Window & Game Loop
> Goal: get a blank pygame window running with a stable game loop.

- [ ] **1a** — Install pygame and create `game.py` with a blank window
- [ ] **1b** — Add a game loop with `clock.tick()` and delta-time (`dt`)
- [ ] **1c** — Handle the quit event so the window closes cleanly

---

### Phase 2 — Settings & Tile Definitions
> Goal: define your constants and tile types before building the world.

- [ ] **2a** — Create `settings.py` with screen size, tile size, FPS, and colors
- [ ] **2b** — Define tile type constants (`AIR`, `WALL`, `DIRT`, etc.) in `world.py`
- [ ] **2c** — Create a `Tile` dataclass/dict with `hardness` and `color` per type

---

### Phase 3 — Static World & Rendering
> Goal: render a hardcoded cave map on screen.

- [ ] **3a** — Create a 2D list (grid) in `world.py` representing a small cave
- [ ] **3b** — Write a `draw()` function that renders each tile as a colored rectangle
- [ ] **3c** — Call `world.draw()` from the game loop and verify tiles appear

---

### Phase 4 — Player Movement
> Goal: a rectangle that moves around the cave.

- [ ] **4a** — Create `player.py` with a `Player` class (position, size, speed, color)
- [ ] **4b** — Read WASD keys each frame and update player position using `dt`
- [ ] **4c** — Draw the player rectangle on screen

---

### Phase 5 — Collision Detection
> Goal: player cannot walk through walls.

- [ ] **5a** — Write a helper that checks which tile a given pixel coordinate is in
- [ ] **5b** — Move player on the X axis, check for solid tile overlap, push back if needed
- [ ] **5c** — Repeat for the Y axis (handle axes separately to avoid corner sticking)

---

### Phase 6 — Scrolling Camera
> Goal: the view follows the player as they explore.

- [ ] **6a** — Create `camera.py` with an offset calculated from player position
- [ ] **6b** — Apply the camera offset when drawing tiles and the player
- [ ] **6c** — Clamp the camera so it does not scroll past world edges

---

### Phase 7 — Mining
> Goal: click on a tile to mine it over time.

- [ ] **7a** — Detect which tile the mouse cursor is hovering over (world coords)
- [ ] **7b** — Highlight the hovered tile with an outline
- [ ] **7c** — Hold left click to accumulate mining progress on the target tile
- [ ] **7d** — When progress reaches the tile's hardness value, remove the tile (set to `AIR`)
- [ ] **7e** — Draw a progress bar on the tile being mined

---

### Phase 8 — Resource Drops & Inventory
> Goal: breaking a tile adds a resource to the player's inventory.

- [ ] **8a** — Create `inventory.py` with a dict `{"Stone": 3, "Coal": 1, ...}`
- [ ] **8b** — When a tile breaks, add its resource to the inventory
- [ ] **8c** — Draw a simple inventory list in a corner of the screen
- [ ] **8d** — Toggle inventory visibility with `E`

---

### Phase 9 — Procedural Cave Generation
> Goal: replace the hardcoded map with a generated cave.

- [ ] **9a** — Fill the grid randomly with `WALL` and `AIR` based on a density value
- [ ] **9b** — Apply cellular automata smoothing (several passes)
- [ ] **9c** — Ensure the player spawn point starts on an `AIR` tile
- [ ] **9d** — Scatter ore tiles (`COAL`, `IRON`, `GOLD`, `GEM`) at tuned rarities

---

### Phase 10 — Polish (stretch goals)
> Only tackle these once the core game is working end-to-end.

- [ ] **10a** — Ambient lighting: dark overlay with a light radius around the player
- [ ] **10b** — Mining sound effect on each tick
- [ ] **10c** — Tile sprites instead of colored rectangles
- [ ] **10d** — Tool tiers with crafting
- [ ] **10e** — Save/load world state to a file
- [ ] **10f** — Main menu and pause screen

---

## Controls

| Key / Input   | Action             |
|---------------|--------------------|
| WASD / Arrows | Move player        |
| Left Click    | Mine targeted tile |
| E             | Toggle inventory   |
| ESC           | Pause / Menu       |

---

## Libraries
- `pygame` — rendering, input, sound
- `noise` (optional, Phase 9) — Perlin noise as alternative to cellular automata

---

## Decisions Made
- **Top-down free movement** (not side-scrolling) — simpler physics, better fit for mining in all directions
- **Cellular automata** for cave generation — no extra library needed, produces natural-looking caves
