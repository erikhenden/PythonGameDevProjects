# CLAUDE.md — plat_jumper

## How to Run

Run from the **parent directory**:

```
cd C:\Users\erikh\PycharmProjects\PythonProject\PythonGameDevProjects
python plat_jumper
```

Controls: A/D — move left/right | Space — jump | Escape or Q — quit

---

## Game Design Vision

Doodle Jump-style upward-scrolling platformer.

1. Player jumps upward, landing on platforms.
2. Camera scrolls up as the player climbs; platforms are procedurally generated above.
3. Old platforms scroll off the bottom and are removed.
4. Score increases with height reached.
5. Game over when the player falls off the bottom of the screen.

Simple, readable aesthetic. Do not add visual complexity for its own sake.

---

## Tech Stack and Constraints

- **Python 3.14**, **pygame only** — no other runtime dependencies.
- No external game frameworks (no Arcade, Pyglet, etc.).
- No build step. Runs directly with `python plat_jumper`.

---

## Architecture

```
plat_jumper/
├── __main__.py   Entry point. Instantiates Game, runs main_loop(), calls pygame.quit().
├── game.py       Game class. Window, clock, all game objects. Loop: input → logic → draw at 60 FPS.
├── entities.py   All game objects. GameObject base class; Jumper extends it with physics.
├── utils.py      Pure helpers. Currently: load_image(name, with_alpha).
└── assets/images/  PNG sprites (jumper.png, jumper2.png).
```

- `game_objects` is a `@property` on `Game` — add new entity types there.
- `GameObject.update(surface)` receives the screen surface for boundary checks.
- Entity behaviour belongs in entity classes, not in `game.py`.

---

## Physics Constants (do not change without understanding the gameplay impact)

| Constant | File | Value | Meaning |
|---|---|---|---|
| `gravity` | `entities.py` Jumper.__init__ | `Vector2(0, 0.25)` | Downward accel per frame |
| Jump velocity | `entities.py` Jumper.jump() | `-13` (y) | Upward impulse |
| `SPEED` | `entities.py` Jumper.SPEED | `6` | Horizontal px/frame |
| Frame rate | `game.py` _draw() | `60` FPS | Target tick rate |
| Window | `game.py` __init__ | `800 x 600` | Do not resize without testing |

`jump()` resets `velocity.y = 0` before applying the impulse — intentional, ensures consistent jump height regardless of falling speed.

---

## Code Style

- Keep it simple. This is a small game, not a game engine.
- No over-engineering: no ECS, no event buses, no dependency injection.
- One responsibility per file. Keep it that way.
- Comments explain *why*, not *what*.
- PEP 8, 4-space indentation.

---

## Adding New Entities

1. Subclass `GameObject` in `entities.py`.
2. Override `update(self, surface)` and optionally `draw(self, surface)`.
3. Add instance to `Game.game_objects`.

---

## Planned Features (add incrementally, do not pre-empt)

- **Platform class** — static platforms; collision detection in `_game_logic`.
- **Procedural generation** — spawn above visible area, remove when off-bottom.
- **Camera scroll** — `camera_offset` on `Game`; shift all entity positions downward as player climbs.
- **Screen wrapping** — exit left → reappear right (two-line change in `Jumper.update`).
- **Score display** — derived from total upward distance; `pygame.font` in `_draw`.
- **Game-over state** — player falls off bottom; show score, allow restart without restarting process.
- **Sound effects** — jump/land sounds via `pygame.mixer`; files in `assets/sounds/`.
- **Platform variants** — crumbling, spring-boost; subclass `Platform` in `entities.py`.

---

## What to Avoid

- Do not use `pygame.sprite.Group` unless object count makes manual iteration a bottleneck.
- Do not change the run invocation from `python plat_jumper` (parent-dir package style).
- Do not add `requirements.txt` unless a second dependency is actually introduced.
