import pygame
import random
from entities import Jumper, Platform, CrumblingPlatform, SpringPlatform

SCREEN_W, SCREEN_H = 800, 600
# Camera scrolls when player rises above this Y position
SCROLL_THRESHOLD = SCREEN_H * 0.4


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Jumper")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.font_large = pygame.font.SysFont(None, 72)

        self.running = True
        self._reset()

    def _reset(self):
        """Initialise (or reinitialise) all game state for a new run."""
        self.jumper = Jumper((400, 300))
        self.platforms = [Platform((360, 340))]
        self._top_platform_y = 340
        self.score = 0
        self.game_over = False
        self._fill_platforms()

    def main_loop(self):
        while self.running:
            self._handle_input()
            if not self.game_over:
                self._game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False
                if self.game_over and event.key == pygame.K_r:
                    self._reset()

        if not self.game_over:
            keypress = pygame.key.get_pressed()
            if keypress[pygame.K_a]:
                self.jumper.move_sideways(False)
            elif keypress[pygame.K_d]:
                self.jumper.move_sideways(True)

    @property
    def game_objects(self):
        return [self.jumper] + self.platforms

    def _make_platform(self, x, y):
        """Pick a platform variant by weighted chance."""
        roll = random.random()
        if roll < 0.10:
            return SpringPlatform((x, y))
        if roll < 0.30:
            return CrumblingPlatform((x, y))
        return Platform((x, y))

    def _fill_platforms(self):
        """Spawn platforms above _top_platform_y until comfortably above the screen top."""
        while self._top_platform_y > -200:
            y = self._top_platform_y - random.randint(60, 100)
            x = random.randint(40, SCREEN_W - Platform.WIDTH - 40)
            self.platforms.append(self._make_platform(x, y))
            self._top_platform_y = y

    def _scroll_camera(self):
        """When the player climbs above the scroll threshold, shift every entity downward."""
        if self.jumper.position.y >= SCROLL_THRESHOLD:
            return
        shift = SCROLL_THRESHOLD - self.jumper.position.y
        self.jumper.position.y = SCROLL_THRESHOLD
        for p in self.platforms:
            p.position.y += shift
        self._top_platform_y += shift
        self.score += int(shift)

    def _cull_platforms(self):
        """Remove platforms that have scrolled below the screen or crumbled away."""
        self.platforms = [p for p in self.platforms if p.position.y < SCREEN_H and not p.dead]

    def _check_collisions(self):
        jumper = self.jumper
        # Only resolve landing when falling downward
        if jumper.velocity.y <= 0:
            return

        j_left = jumper.position.x
        j_right = jumper.position.x + jumper.width
        j_bottom = jumper.position.y + jumper.height
        j_bottom_prev = j_bottom - jumper.velocity.y  # feet position last frame

        for platform in self.platforms:
            p_left = platform.position.x
            p_right = platform.position.x + Platform.WIDTH
            p_top = platform.position.y

            if j_right <= p_left or j_left >= p_right:
                continue

            # Land if feet crossed the platform top this frame (pass-through from below allowed)
            if j_bottom_prev <= p_top <= j_bottom:
                jumper.position.y = p_top - jumper.height
                platform.on_land(jumper)  # each variant handles its own jump + side effects
                break

    def _game_logic(self):
        for obj in self.game_objects:
            obj.update(self.screen)
        self._check_collisions()
        self._scroll_camera()
        self._cull_platforms()
        self._fill_platforms()

        if self.jumper.position.y > SCREEN_H:
            self.game_over = True

    def _draw(self):
        self.screen.fill(pygame.Color("skyblue"))
        for obj in self.game_objects:
            obj.draw(self.screen)

        score_surf = self.font.render(f"Score: {self.score}", True, pygame.Color("black"))
        self.screen.blit(score_surf, (10, 10))

        if self.game_over:
            self._draw_game_over()

        pygame.display.flip()
        self.clock.tick(60)

    def _draw_game_over(self):
        # Semi-transparent dark overlay
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        over_surf = self.font_large.render("GAME OVER", True, pygame.Color("white"))
        score_surf = self.font.render(f"Score: {self.score}", True, pygame.Color("white"))
        hint_surf = self.font.render("R — restart    Q — quit", True, pygame.Color("lightgray"))

        cx = SCREEN_W // 2
        self.screen.blit(over_surf, over_surf.get_rect(center=(cx, 230)))
        self.screen.blit(score_surf, score_surf.get_rect(center=(cx, 310)))
        self.screen.blit(hint_surf, hint_surf.get_rect(center=(cx, 360)))
