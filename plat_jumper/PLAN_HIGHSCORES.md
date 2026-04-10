# Highscores Feature — Implementation Plan

## Overview

Add a persistent top-10 leaderboard with name entry to `plat_jumper`. Scores are
stored in `highscores.json`. The game-over flow becomes:

```
game over → name entry (qualifying score) → highscores screen
         ↘ highscores screen (non-qualifying)
```

---

## 1. Data Schema — `highscores.json`

Lives at `plat_jumper/highscores.json`, resolved via `Path(__file__).parent` (same
pattern as `assets/` in `utils.py`). Gitignored — it is runtime data, not source.

```json
{
  "scores": [
    {"name": "AAA", "score": 4200},
    {"name": "BB",  "score": 3100}
  ]
}
```

Rules:
- `"scores"` is always sorted descending by `score`.
- Maximum 10 entries; on insert, re-sort and truncate.
- `name` is 1–3 uppercase letters (enforced during entry).
- `score` is a plain integer matching `self.score`.
- Missing or malformed file → treat as empty list (graceful degradation, no crash).

---

## 2. New File: `plat_jumper/highscores.py`

Pure-data module, no pygame dependency. Four plain functions (no classes), consistent
with the `utils.py` pattern.

| Function | Signature | Description |
|---|---|---|
| `load` | `() -> list[dict]` | Reads `highscores.json`; returns `[]` on any error. |
| `save` | `(scores: list[dict]) -> None` | Sorts descending, truncates to 10, writes with `indent=2`. |
| `qualifies` | `(score: int, scores: list[dict]) -> bool` | True if score > 0 AND (len < 10 OR score > last entry). |
| `insert` | `(name: str, score: int, scores: list[dict]) -> list[dict]` | Returns a new sorted, truncated list; does not mutate input. |

### `qualifies` logic

```
if score <= 0:         return False
if len(scores) < 10:  return True
return score > scores[-1]["score"]
```

- Score of 0 never qualifies (prevents immediate-death spam on the name-entry screen).
- `scores[-1]` is safe because the `len < 10` guard above ensures non-empty access.
- Ties with 10th place do **not** qualify (`>` not `>=`) to keep the list bounded.

---

## 3. Game State Machine

### Replace `game_over: bool` with `state: str`

Add three module-level constants at the top of `game.py`:

```python
STATE_PLAYING    = "playing"
STATE_NAME_ENTRY = "name_entry"
STATE_HIGHSCORES = "highscores"
```

Plain string constants (not `enum.Enum`) — readable, comparable with `==`, no import needed.

### Transitions

| From | Trigger | To | Side Effect |
|---|---|---|---|
| `playing` | jumper falls off screen (qualifies) | `name_entry` | `_reset_for_game_over()` |
| `playing` | jumper falls off screen (no qualify) | `highscores` | `_reset_for_game_over()` |
| `name_entry` | RETURN pressed (≥ 1 char) | `highscores` | `insert()` + `save()` |
| `name_entry` | ESC pressed | `highscores` | score discarded |
| `highscores` | R pressed | `playing` | `_reset()` |
| `highscores` | Q or ESC pressed | exit | `self.running = False` |
| Any | QUIT event | exit | `self.running = False` |

---

## 4. Changes to `game.py`

### `__init__`
- Add `self.font_medium = pygame.font.SysFont(None, 48)`.
- Add `self._scores = highscores.load()`.
- Add `self._pending_name: list[str] = []`.
- Add `self._final_score: int = 0`.

### `_reset()`
- Replace `self.game_over = False` with `self.state = STATE_PLAYING`.

### New `_reset_for_game_over()`
Called exactly once when the jumper falls off screen. Does **not** reinitialise the
game world (the frozen world stays visible under overlays).

1. Set `self._final_score = self.score`.
2. Clear `self._pending_name = []`.
3. Reload `self._scores = highscores.load()` (keeps in-memory list fresh).
4. Set `self.state = STATE_NAME_ENTRY` if `highscores.qualifies(...)`, else `STATE_HIGHSCORES`.

### `_game_logic()` — one-line change
```python
# before
self.game_over = True
# after
self._reset_for_game_over()
```

### `main_loop()` — one-line change
```python
# before
if not self.game_over:
# after
if self.state == STATE_PLAYING:
```

### `_handle_input()` — split into three sub-methods

Collect events once per frame and pass them down:

```python
def _handle_input(self):
    events = pygame.event.get()
    keys   = pygame.key.get_pressed()
    if self.state == STATE_PLAYING:
        self._input_playing(events, keys)
    elif self.state == STATE_NAME_ENTRY:
        self._input_name_entry(events)
    elif self.state == STATE_HIGHSCORES:
        self._input_highscores(events)
```

**`_input_playing(events, keys)`**
- QUIT / ESC / Q → `self.running = False`.
- A/LEFT or D/RIGHT in `keys` → `jumper.move_sideways(...)`.

**`_input_name_entry(events)`**
- QUIT → `self.running = False`.
- ESC → `self.state = STATE_HIGHSCORES` (discard entry).
- BACKSPACE → pop last char from `self._pending_name` if non-empty.
- RETURN → if `len(self._pending_name) >= 1`: commit name, update `self._scores`, save, set `STATE_HIGHSCORES`.
- Letter key + `len < 3` → append `event.unicode.upper()` (filter with `event.unicode.isalpha()`).

**`_input_highscores(events)`**
- QUIT / Q / ESC → `self.running = False`.
- R → `self._reset()`.

### `_draw()` — dispatch
```python
def _draw(self):
    self.screen.fill(pygame.Color("skyblue"))
    for obj in self.game_objects:
        obj.draw(self.screen)
    score_surf = self.font.render(f"Score: {self.score}", True, pygame.Color("black"))
    self.screen.blit(score_surf, (10, 10))
    if self.state == STATE_NAME_ENTRY:
        self._draw_name_entry()
    elif self.state == STATE_HIGHSCORES:
        self._draw_highscores()
    pygame.display.flip()
    self.clock.tick(60)
```

The frozen game world is drawn first in all states — overlays sit on top. No extra state needed.

### Delete `_draw_game_over()`
Its role is split across `_draw_name_entry()` and `_draw_highscores()`.

### New `_draw_name_entry()`

Semi-transparent dark overlay (alpha 160), then centered on `cx = SCREEN_W // 2`:

| Element | Font | y |
|---|---|---|
| "GAME OVER" | `font_large` | 180 |
| `f"Score: {self._final_score}"` | `font` | 260 |
| "New High Score! Enter your name:" | `font_medium` | 310 |
| Name display (entered chars + `_` padding to 3) | `font_large` | 370 |
| "RETURN — confirm    ESC — skip" | `font` | 440 |

Name display: build a string of length 3 where entered characters fill from the left
and remaining slots are `_`. E.g. after pressing A: `"A__"`.

### New `_draw_highscores()`

Semi-transparent dark overlay (alpha 180), then:

| Element | Font | Position |
|---|---|---|
| "HIGH SCORES" | `font_large` | y=60, centered |
| Rank rows (up to 10) | `font_medium` | y=130 + rank*40, left-anchored at cx−160 |
| Empty-list message | `font` | y=280, centered |
| "R — play again    Q — quit" | `font` | y=560, centered |

Row format: `f"{rank}.  {entry['name']:<3}  {entry['score']}"`.

Highlight: render the row matching `self._final_score` in `pygame.Color("yellow")`
instead of white. (Cosmetic — tie-breaking is not needed here.)

---

## 5. `.gitignore` (new file at repo root)

```
# Runtime data
plat_jumper/highscores.json

# Python bytecode
__pycache__/
*.pyc

# IDE
.idea/
```

---

## 6. Files Changed

| File | Change |
|---|---|
| `plat_jumper/highscores.py` | **New** — `load`, `save`, `qualifies`, `insert` |
| `plat_jumper/game.py` | **Modify** — state machine, new draw/input methods |
| `.gitignore` | **New** — ignore `highscores.json` and bytecode |
| `plat_jumper/utils.py` | No change |
| `plat_jumper/entities.py` | No change |
| `plat_jumper/__main__.py` | No change |

---

## 7. Ordered Implementation Steps

Follow this sequence — the game remains runnable after each step.

1. **Create `highscores.py`**: write the four functions. Verify in a REPL:
   `load()` → `[]`; `save([...])` creates the file; `qualifies(0, [])` → `False`;
   `qualifies(50, [])` → `True`. Zero impact on running game.

2. **Refactor state in `game.py`**: add `STATE_*` constants; replace `game_over = False`
   with `self.state = STATE_PLAYING`; update `main_loop` and `_draw` guards. Game
   behaviour is identical.

3. **Add new `__init__` fields**: `font_medium`, `_scores`, `_pending_name`, `_final_score`.
   No behavioural change.

4. **Add `_reset_for_game_over()`**: replace `self.game_over = True` with
   `self._reset_for_game_over()`. Temporarily keep `_draw_game_over` reachable via a
   `state != STATE_PLAYING` guard to confirm the transition fires correctly.

5. **Add `_draw_name_entry()` and `_draw_highscores()`**: update `_draw()` dispatch;
   delete `_draw_game_over()`. Test both screens visually.

6. **Refactor `_handle_input()`**: rewrite into three sub-methods. Test all transitions
   manually (qualifying die → name entry → confirm → highscores → restart; non-qualifying
   die → highscores → quit; ESC discards name; backspace works).

7. **Test persistence**: play, enter name, quit, relaunch — score persists. Fill top 10 —
   11th entry displaces the lowest.

8. **Add `.gitignore`**: confirm `git status` no longer shows `highscores.json` or
   `__pycache__/` as untracked.

---

## 8. Key Design Decisions

- **`highscores.py` as a new module**: serialisation and ranking are data concerns, not
  game-loop concerns. Precedent: `utils.py` for pure helpers. Avoids polluting `game.py`
  with `json` import and file I/O.

- **String constants, not `enum.Enum`**: three constants are readable and require no
  extra import. An Enum would add noise at this scale.

- **Three input sub-methods**: prevents a single 50-line `_handle_input` with nested
  conditionals. Each sub-method has a single clear context and stays under 15 lines.

- **`_pending_name` as `list[str]`**: supports efficient `append`/`pop`; converted to
  string only at render and save time.

- **`_final_score` separate from `self.score`**: `_reset()` zeroes `self.score`.
  `_final_score` lets `_draw_highscores` highlight the just-achieved row even after a
  reset has cleared the live score counter.

- **Game world rendered behind overlays**: the frozen world is drawn first in every
  state; overlays composite on top. This is free (objects already exist) and gives
  overlays visual depth without extra state.
