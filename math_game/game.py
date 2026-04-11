import pygame
import settings as s
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    STATE_MENU, STATE_LEVEL_SELECT, STATE_PLAYING,
    LEVELS, COINS_CORRECT_FIRST, COINS_CORRECT_SECOND,
    COINS_STREAK_BONUS, STREAK_MILESTONE,
    WHITE, BLACK, GOLD, YELLOW, GREEN_DARK, GREEN_MID, GREEN_LIGHT,
    ORANGE, RED, CREAM, BROWN, DARK_PANEL, GREY, BLUE_LIGHT,
)
from entities import (
    InputBox, QuestionDisplay, FeedbackLabel,
    CoinDisplay, StreakDisplay, Monkey, JungleBackground,
)
from utils import generate_question, check_answer, load_save, save_data


# ---------------------------------------------------------------------------
# Attempt state within a question
# ---------------------------------------------------------------------------
ATTEMPT_FIRST  = 1
ATTEMPT_SECOND = 2


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(s.TITLE)
        self.clock  = pygame.time.Clock()
        self.running = True

        s.load_fonts()

        # Persistent save data
        self._save = load_save()

        # Current UI state
        self._state         = STATE_MENU
        self._selected_level = 1

        # --- Shared background ---
        self._bg = JungleBackground(SCREEN_WIDTH, SCREEN_HEIGHT)

        # --- Menu screen ---
        self._menu_buttons = self._build_menu_buttons()

        # --- Level select screen ---
        self._level_buttons = self._build_level_buttons()

        # --- Playing screen ---
        self._question       = None
        self._attempt        = ATTEMPT_FIRST
        self._streak         = 0

        self._question_disp  = QuestionDisplay(SCREEN_WIDTH // 2, 160)
        self._input_box      = InputBox(SCREEN_WIDTH // 2 - 140, 220, 280, 80)
        self._feedback       = FeedbackLabel(SCREEN_WIDTH // 2, 340)
        self._coin_display   = CoinDisplay(SCREEN_WIDTH - 20, 16)
        self._streak_display = StreakDisplay(SCREEN_WIDTH - 20, 52)
        self._monkey         = Monkey(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 180)

        self._stats_correct  = 0
        self._stats_answered = 0

    # -----------------------------------------------------------------------
    # Main loop
    # -----------------------------------------------------------------------

    def main_loop(self):
        while self.running:
            dt = self.clock.tick(FPS)
            self._handle_events()
            self._update(dt)
            self._draw()

    # -----------------------------------------------------------------------
    # Event handling (routes to current state)
    # -----------------------------------------------------------------------

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_escape()
                else:
                    self._handle_key(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click(event.pos)

    def _handle_escape(self):
        if self._state == STATE_PLAYING:
            self._go_to_level_select()
        elif self._state == STATE_LEVEL_SELECT:
            self._state = STATE_MENU
        else:
            self._quit()

    def _handle_key(self, event):
        if self._state == STATE_PLAYING:
            submitted = self._input_box.handle_event(event)
            if submitted is not None:
                self._process_answer(submitted)

    def _handle_click(self, pos):
        if self._state == STATE_MENU:
            for label, rect, action in self._menu_buttons:
                if rect.collidepoint(pos):
                    action()

        elif self._state == STATE_LEVEL_SELECT:
            for level, rect in self._level_buttons:
                if rect.collidepoint(pos):
                    self._start_playing(level)
            # Back button
            if self._back_button_rect.collidepoint(pos):
                self._state = STATE_MENU

    # -----------------------------------------------------------------------
    # Update
    # -----------------------------------------------------------------------

    def _update(self, dt: int):
        if self._state == STATE_PLAYING:
            self._input_box.update(dt)
            self._feedback.update(dt)
            self._coin_display.update(dt)
            self._monkey.update(dt)

    # -----------------------------------------------------------------------
    # Draw (routes to current state)
    # -----------------------------------------------------------------------

    def _draw(self):
        if self._state == STATE_MENU:
            self._draw_menu()
        elif self._state == STATE_LEVEL_SELECT:
            self._draw_level_select()
        elif self._state == STATE_PLAYING:
            self._draw_playing()

        pygame.display.flip()

    # -----------------------------------------------------------------------
    # Game logic — answer processing
    # -----------------------------------------------------------------------

    def _process_answer(self, raw: str):
        if not raw.strip():
            return

        self._stats_answered += 1
        self._save["total_answered"] += 1

        if check_answer(self._question, raw):
            # --- Correct ---
            self._stats_correct += 1
            self._save["total_correct"] += 1
            self._streak += 1

            coins_earned = (COINS_CORRECT_FIRST
                            if self._attempt == ATTEMPT_FIRST
                            else COINS_CORRECT_SECOND)

            streak_bonus = 0
            if self._streak > 0 and self._streak % STREAK_MILESTONE == 0:
                streak_bonus = COINS_STREAK_BONUS

            self._save["coins"] += coins_earned + streak_bonus
            save_data(self._save)

            self._coin_display.set_coins(self._save["coins"])
            self._monkey.set_happy()

            if streak_bonus:
                self._feedback.show(
                    f"+{coins_earned} coins  STREAK BONUS +{streak_bonus}!",
                    GOLD
                )
            else:
                self._feedback.show(f"+{coins_earned} coins", GREEN_LIGHT)

            self._input_box.flash_green()
            self._next_question()

        else:
            # --- Wrong ---
            if self._attempt == ATTEMPT_FIRST:
                self._attempt = ATTEMPT_SECOND
                self._input_box.shake()
                self._input_box.clear()
                self._monkey.set_sad()
                self._feedback.show("Try again!", ORANGE)
            else:
                # second wrong — show answer
                self._streak = 0
                self._monkey.set_sad()
                self._feedback.show(
                    f"Answer was {self._question['answer']}", RED
                )
                self._input_box.clear()
                self._next_question()

    def _next_question(self):
        self._question = generate_question(self._selected_level)
        self._question_disp.set_question(self._question["text"])
        self._attempt  = ATTEMPT_FIRST
        self._input_box.clear()
        self._streak_display.set_streak(self._streak)

    # -----------------------------------------------------------------------
    # State transitions
    # -----------------------------------------------------------------------

    def _go_to_level_select(self):
        save_data(self._save)
        self._state = STATE_LEVEL_SELECT

    def _start_playing(self, level: int):
        self._selected_level  = level
        self._streak          = 0
        self._stats_correct   = 0
        self._stats_answered  = 0
        self._state           = STATE_PLAYING
        self._coin_display.set_coins(self._save["coins"])
        self._streak_display.set_streak(0)
        self._next_question()

    def _quit(self):
        save_data(self._save)
        self.running = False

    # -----------------------------------------------------------------------
    # ---- MENU SCREEN -------------------------------------------------------
    # -----------------------------------------------------------------------

    def _build_menu_buttons(self):
        """Returns list of (label, Rect, callback)."""
        cx = SCREEN_WIDTH // 2
        buttons = [
            ("PLAY",  pygame.Rect(cx - 120, 300, 240, 60), self._go_to_level_select),
            ("QUIT",  pygame.Rect(cx - 120, 390, 240, 60), self._quit),
        ]
        return buttons

    def _draw_menu(self):
        self._bg.draw(self.screen)

        # Title panel
        panel = pygame.Surface((500, 120), pygame.SRCALPHA)
        panel.fill((20, 60, 20, 180))
        self.screen.blit(panel, (150, 100))

        title = s.FONT_LARGE.render("Math Jungle", True, YELLOW)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 160)))

        sub = s.FONT_SMALL.render("Learn maths in the jungle!", True, WHITE)
        self.screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, 210)))

        # Coin total
        coins_txt = s.FONT_MEDIUM.render(
            f"Your coins: {self._save['coins']}", True, GOLD
        )
        self.screen.blit(coins_txt, coins_txt.get_rect(center=(SCREEN_WIDTH // 2, 262)))

        mouse_pos = pygame.mouse.get_pos()
        for label, rect, _ in self._menu_buttons:
            self._draw_button(self.screen, label, rect, mouse_pos)

    # -----------------------------------------------------------------------
    # ---- LEVEL SELECT SCREEN -----------------------------------------------
    # -----------------------------------------------------------------------

    def _build_level_buttons(self):
        """Returns list of (level_int, Rect)."""
        buttons = []
        start_y = 140
        for level in range(1, 6):
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 240, start_y + (level - 1) * 76, 480, 62)
            buttons.append((level, rect))
        self._back_button_rect = pygame.Rect(20, SCREEN_HEIGHT - 60, 120, 44)
        return buttons

    def _draw_level_select(self):
        self._bg.draw(self.screen)

        heading = s.FONT_MEDIUM.render("Choose Your Level", True, YELLOW)
        self.screen.blit(heading, heading.get_rect(center=(SCREEN_WIDTH // 2, 90)))

        mouse_pos = pygame.mouse.get_pos()
        for level, rect in self._level_buttons:
            cfg      = LEVELS[level]
            hovered  = rect.collidepoint(mouse_pos)
            bg_color = GREEN_LIGHT if hovered else GREEN_MID
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=12)
            pygame.draw.rect(self.screen, BROWN, rect, 3, border_radius=12)

            # Level name + description
            name_surf = s.FONT_MEDIUM.render(
                f"Level {level}: {cfg['name']}", True, WHITE
            )
            desc_surf = s.FONT_SMALL.render(cfg["desc"], True, CREAM)

            self.screen.blit(name_surf, name_surf.get_rect(
                midleft=(rect.x + 16, rect.centery - 10)))
            self.screen.blit(desc_surf, desc_surf.get_rect(
                midleft=(rect.x + 16, rect.centery + 16)))

        # Total coins bottom-right
        coins_txt = s.FONT_SMALL.render(
            f"Total coins: {self._save['coins']}", True, GOLD
        )
        self.screen.blit(coins_txt,
                         coins_txt.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)))

        # Back button
        back_hovered = self._back_button_rect.collidepoint(mouse_pos)
        self._draw_button(self.screen, "< Back", self._back_button_rect, mouse_pos)

    # -----------------------------------------------------------------------
    # ---- PLAYING SCREEN ----------------------------------------------------
    # -----------------------------------------------------------------------

    def _draw_playing(self):
        self._bg.draw(self.screen)

        # Top panel
        panel = pygame.Surface((SCREEN_WIDTH, 70), pygame.SRCALPHA)
        panel.fill((20, 60, 20, 200))
        self.screen.blit(panel, (0, 0))

        # Level label
        cfg       = LEVELS[self._selected_level]
        lvl_surf  = s.FONT_SMALL.render(
            f"Level {self._selected_level}: {cfg['name']}", True, WHITE
        )
        self.screen.blit(lvl_surf, (16, 22))

        # Stats
        if self._stats_answered > 0:
            pct = int(self._stats_correct / self._stats_answered * 100)
            stat_txt = s.FONT_SMALL.render(
                f"Correct: {self._stats_correct}/{self._stats_answered}  ({pct}%)",
                True, WHITE
            )
            self.screen.blit(stat_txt, stat_txt.get_rect(
                midtop=(SCREEN_WIDTH // 2, 10)))

        self._coin_display.draw(self.screen)
        self._streak_display.draw(self.screen)

        # Question panel
        q_panel = pygame.Surface((520, 200), pygame.SRCALPHA)
        q_panel.fill((20, 60, 20, 190))
        self.screen.blit(q_panel, (SCREEN_WIDTH // 2 - 260, 100))

        self._question_disp.draw(self.screen)
        self._input_box.draw(self.screen)
        self._feedback.draw(self.screen)

        # Attempt indicator
        if self._attempt == ATTEMPT_SECOND:
            hint = s.FONT_SMALL.render("Last chance!", True, ORANGE)
            self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 315)))

        self._monkey.draw(self.screen)

        # ESC hint
        esc_surf = s.FONT_SMALL.render("ESC = back to levels", True, GREY)
        self.screen.blit(esc_surf, (10, SCREEN_HEIGHT - 28))

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _draw_button(self, surface, label, rect, mouse_pos):
        hovered  = rect.collidepoint(mouse_pos)
        bg_color = GREEN_LIGHT if hovered else GREEN_MID
        pygame.draw.rect(surface, bg_color, rect, border_radius=12)
        pygame.draw.rect(surface, BROWN, rect, 3, border_radius=12)
        txt  = s.FONT_MEDIUM.render(label, True, WHITE)
        surface.blit(txt, txt.get_rect(center=rect.center))
