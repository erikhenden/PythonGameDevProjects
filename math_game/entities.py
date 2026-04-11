import pygame
import math
import settings as s


# ---------------------------------------------------------------------------
# InputBox
# ---------------------------------------------------------------------------

class InputBox:
    """Typed text input. Player types digits and presses Enter."""

    def __init__(self, x, y, w, h):
        self.rect   = pygame.Rect(x, y, w, h)
        self.text   = ""
        self.active = True

        # shake animation
        self._shake_timer    = 0
        self._shake_duration = 400   # ms
        self._shake_offset_x = 0

        # flash animation (green on correct)
        self._flash_timer    = 0
        self._flash_duration = 300
        self._flash_color    = None

    # --- public API ---

    def clear(self):
        self.text = ""

    def shake(self):
        self._shake_timer = self._shake_duration

    def flash_green(self):
        self._flash_timer = self._flash_duration
        self._flash_color = s.GREEN_LIGHT

    # --- event handling ---

    def handle_event(self, event) -> str | None:
        """
        Process a keydown event.
        Returns the submitted text string when Enter is pressed,
        or None otherwise.
        """
        if not self.active:
            return None
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            submitted = self.text
            return submitted

        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]

        elif event.unicode.lstrip("-").isdigit():
            # allow digits (and one leading minus for potential negatives)
            if len(self.text) < 6:
                self.text += event.unicode

        return None

    # --- update / draw ---

    def update(self, dt: int):
        if self._shake_timer > 0:
            self._shake_timer -= dt
            # oscillate left-right
            progress = self._shake_timer / self._shake_duration
            self._shake_offset_x = int(math.sin(progress * math.pi * 8) * 10)
        else:
            self._shake_offset_x = 0

        if self._flash_timer > 0:
            self._flash_timer -= dt

    def draw(self, surface: pygame.Surface):
        draw_rect = self.rect.move(self._shake_offset_x, 0)

        # background
        if self._flash_timer > 0:
            box_color = s.GREEN_LIGHT
        else:
            box_color = s.CREAM
        pygame.draw.rect(surface, box_color, draw_rect, border_radius=12)
        pygame.draw.rect(surface, s.BROWN, draw_rect, 3, border_radius=12)

        # text
        font = s.FONT_LARGE
        txt_surf = font.render(self.text if self.text else "", True, s.BLACK)
        txt_rect = txt_surf.get_rect(center=draw_rect.center)
        surface.blit(txt_surf, txt_rect)

        # blinking cursor
        if self.active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = txt_rect.right + 4 if self.text else draw_rect.centerx
            cursor_top    = draw_rect.centery - 22
            cursor_bottom = draw_rect.centery + 22
            pygame.draw.line(surface, s.BLACK, (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)


# ---------------------------------------------------------------------------
# QuestionDisplay
# ---------------------------------------------------------------------------

class QuestionDisplay:
    """Shows the current math question in large text."""

    def __init__(self, x, y):
        self.pos   = (x, y)
        self._text = ""

    def set_question(self, text: str):
        self._text = text + " = ?"

    def draw(self, surface: pygame.Surface):
        font = s.FONT_LARGE
        surf = font.render(self._text, True, s.WHITE)
        rect = surf.get_rect(center=self.pos)
        # soft shadow
        shadow = font.render(self._text, True, s.GREEN_DARK)
        surface.blit(shadow, rect.move(3, 3))
        surface.blit(surf, rect)


# ---------------------------------------------------------------------------
# FeedbackLabel
# ---------------------------------------------------------------------------

class FeedbackLabel:
    """Temporary feedback message that fades out."""

    def __init__(self, x, y):
        self.pos     = (x, y)
        self._text   = ""
        self._color  = s.WHITE
        self._timer  = 0
        self._duration = 1200   # ms

    def show(self, text: str, color):
        self._text   = text
        self._color  = color
        self._timer  = self._duration

    def update(self, dt: int):
        if self._timer > 0:
            self._timer -= dt

    def draw(self, surface: pygame.Surface):
        if self._timer <= 0:
            return
        alpha = min(255, int(255 * self._timer / self._duration))
        font  = s.FONT_MEDIUM
        surf  = font.render(self._text, True, self._color)
        surf.set_alpha(alpha)
        rect  = surf.get_rect(center=self.pos)
        surface.blit(surf, rect)


# ---------------------------------------------------------------------------
# CoinDisplay  (HUD coin counter)
# ---------------------------------------------------------------------------

class CoinDisplay:
    """Top-right HUD showing total coins."""

    def __init__(self, x, y):
        self.pos    = (x, y)
        self._coins = 0
        # pop animation
        self._pop_timer    = 0
        self._pop_duration = 400

    def set_coins(self, coins: int):
        if coins != self._coins:
            self._pop_timer = self._pop_duration
        self._coins = coins

    def update(self, dt: int):
        if self._pop_timer > 0:
            self._pop_timer -= dt

    def draw(self, surface: pygame.Surface):
        scale = 1.0
        if self._pop_timer > 0:
            progress = self._pop_timer / self._pop_duration
            scale = 1.0 + 0.25 * math.sin(progress * math.pi)

        font = s.FONT_MEDIUM
        text = f"Coins: {self._coins}"
        surf = font.render(text, True, s.GOLD)

        if scale != 1.0:
            w = int(surf.get_width() * scale)
            h = int(surf.get_height() * scale)
            surf = pygame.transform.scale(surf, (w, h))

        rect = surf.get_rect(topright=self.pos)
        surface.blit(surf, rect)


# ---------------------------------------------------------------------------
# StreakDisplay
# ---------------------------------------------------------------------------

class StreakDisplay:
    """Shows current streak below the coin counter."""

    def __init__(self, x, y):
        self.pos    = (x, y)
        self._streak = 0

    def set_streak(self, streak: int):
        self._streak = streak

    def draw(self, surface: pygame.Surface):
        if self._streak < 2:
            return
        font = s.FONT_SMALL
        text = f"Streak: {self._streak}!"
        surf = font.render(text, True, s.ORANGE)
        rect = surf.get_rect(topright=self.pos)
        surface.blit(surf, rect)


# ---------------------------------------------------------------------------
# Monkey mascot
# ---------------------------------------------------------------------------

class Monkey:
    """
    Drawn-with-pygame monkey mascot.
    States: idle, happy, sad
    Falls back to pure pygame shapes — no image file required.
    """

    IDLE  = "idle"
    HAPPY = "happy"
    SAD   = "sad"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = self.IDLE

        self._state_timer = 0
        self._state_duration = 1200   # ms before returning to idle

        # idle bobbing
        self._bob_offset = 0.0
        self._bob_t      = 0.0

    def set_happy(self):
        self.state         = self.HAPPY
        self._state_timer  = self._state_duration

    def set_sad(self):
        self.state        = self.SAD
        self._state_timer = self._state_duration

    def update(self, dt: int):
        if self._state_timer > 0:
            self._state_timer -= dt
            if self._state_timer <= 0:
                self.state = self.IDLE

        self._bob_t += dt * 0.003
        self._bob_offset = math.sin(self._bob_t) * 6

    def draw(self, surface: pygame.Surface):
        cx = self.x
        cy = int(self.y + self._bob_offset)

        if self.state == self.HAPPY:
            cy -= 10   # jump up a little

        # ----- body -----
        body_color = (160, 100, 40)
        face_color = (220, 170, 100)
        pygame.draw.ellipse(surface, body_color, (cx - 28, cy - 10, 56, 64))

        # ----- head -----
        pygame.draw.circle(surface, body_color, (cx, cy - 38), 32)

        # ----- ears -----
        pygame.draw.circle(surface, body_color, (cx - 30, cy - 38), 12)
        pygame.draw.circle(surface, face_color, (cx - 30, cy - 38), 7)
        pygame.draw.circle(surface, body_color, (cx + 30, cy - 38), 12)
        pygame.draw.circle(surface, face_color, (cx + 30, cy - 38), 7)

        # ----- face patch -----
        pygame.draw.ellipse(surface, face_color, (cx - 18, cy - 52, 36, 30))

        # ----- eyes -----
        eye_y = cy - 44
        eye_white = (255, 255, 255)
        pygame.draw.circle(surface, eye_white, (cx - 10, eye_y), 7)
        pygame.draw.circle(surface, eye_white, (cx + 10, eye_y), 7)

        if self.state == self.SAD:
            pupil_offset = 2   # pupils look down
        else:
            pupil_offset = 0
        pygame.draw.circle(surface, s.BLACK, (cx - 10, eye_y + pupil_offset), 4)
        pygame.draw.circle(surface, s.BLACK, (cx + 10, eye_y + pupil_offset), 4)

        # ----- mouth -----
        mouth_y = cy - 30
        if self.state == self.HAPPY:
            # big smile
            pygame.draw.arc(surface, s.BLACK,
                            (cx - 14, mouth_y - 4, 28, 16),
                            math.pi, 2 * math.pi, 3)
        elif self.state == self.SAD:
            # frown
            pygame.draw.arc(surface, s.BLACK,
                            (cx - 14, mouth_y + 4, 28, 16),
                            0, math.pi, 3)
        else:
            # neutral line
            pygame.draw.line(surface, s.BLACK,
                             (cx - 10, mouth_y + 6), (cx + 10, mouth_y + 6), 3)

        # ----- arms -----
        pygame.draw.line(surface, body_color, (cx - 28, cy + 10), (cx - 50, cy + 30), 8)
        pygame.draw.line(surface, body_color, (cx + 28, cy + 10), (cx + 50, cy + 30), 8)

        # ----- tail -----
        tail_pts = [
            (cx + 28, cy + 40),
            (cx + 50, cy + 55),
            (cx + 60, cy + 40),
            (cx + 55, cy + 30),
        ]
        if len(tail_pts) >= 2:
            pygame.draw.lines(surface, body_color, False, tail_pts, 7)

        # ----- happy stars -----
        if self.state == self.HAPPY:
            self._draw_star(surface, cx - 55, cy - 50, 10, s.GOLD)
            self._draw_star(surface, cx + 55, cy - 55, 8,  s.YELLOW)

    @staticmethod
    def _draw_star(surface, cx, cy, r, color):
        points = []
        for i in range(10):
            angle = math.pi / 5 * i - math.pi / 2
            radius = r if i % 2 == 0 else r * 0.45
            points.append((cx + math.cos(angle) * radius,
                           cy + math.sin(angle) * radius))
        pygame.draw.polygon(surface, color, points)


# ---------------------------------------------------------------------------
# JungleBackground
# ---------------------------------------------------------------------------

class JungleBackground:
    """Simple procedural jungle background drawn with pygame shapes."""

    def __init__(self, width, height):
        self.w = width
        self.h = height
        self._surface = pygame.Surface((width, height))
        self._build()

    def _build(self):
        surf = self._surface

        # sky gradient (approximated with horizontal bands)
        for y in range(self.h):
            t = y / self.h
            r = int(50  + (80  - 50)  * t)
            g = int(120 + (160 - 120) * t)
            b = int(50  + (40  - 50)  * t)
            pygame.draw.line(surf, (r, g, b), (0, y), (self.w, y))

        # back tree layer (dark)
        tree_positions = [60, 160, 280, 400, 520, 660, 760]
        for tx in tree_positions:
            self._draw_tree(surf, tx, self.h - 60, 110, 38, (30, 80, 30))

        # ground strip
        pygame.draw.rect(surf, (40, 100, 30), (0, self.h - 60, self.w, 60))
        pygame.draw.rect(surf, (60, 130, 40), (0, self.h - 60, self.w, 10))

        # front tree layer (lighter)
        front_positions = [0, 120, 320, 500, 680, 800]
        for tx in front_positions:
            self._draw_tree(surf, tx, self.h - 40, 130, 44, (50, 110, 40))

        # some bushes
        for bx in [80, 220, 380, 560, 720]:
            pygame.draw.ellipse(surf, (40, 110, 30),
                                (bx - 40, self.h - 80, 80, 40))

    @staticmethod
    def _draw_tree(surf, x, base_y, height, trunk_w, color):
        # trunk
        trunk_h = height // 3
        pygame.draw.rect(surf, (80, 50, 20),
                         (x - trunk_w // 4, base_y - trunk_h, trunk_w // 2, trunk_h))
        # canopy layers
        for i, (ratio, y_off) in enumerate([(1.0, 0), (0.75, -height // 3), (0.5, -height * 2 // 3)]):
            r = int(trunk_w * ratio * 1.2)
            cy = base_y - trunk_h - y_off
            pygame.draw.circle(surf, color, (x, cy), r)

    def draw(self, surface: pygame.Surface):
        surface.blit(self._surface, (0, 0))
