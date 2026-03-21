import pygame
import random
from entities import Jumper, Platform

SCREEN_W, SCREEN_H = 800, 600
# Camera scrolls when player rises above this Y position
SCROLL_THRESHOLD = SCREEN_H * 0.4


class Game:
    def __init__(self):
        self.running = True

        pygame.init()
        pygame.display.set_caption("Jumper")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.jumper = Jumper((400, 300))

        # One platform directly under the starting position
        self.platforms = [Platform((360, 340))]
        self._top_platform_y = 340  # world Y of highest generated platform so far
        self.score = 0

        self._fill_platforms()

    def main_loop(self):
        while self.running:
            self._handle_input()
            self._game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False

        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_a]:
            self.jumper.move_sideways(False)
        elif keypress[pygame.K_d]:
            self.jumper.move_sideways(True)

    @property
    def game_objects(self):
        return [self.jumper] + self.platforms

    def _fill_platforms(self):
        """Spawn platforms above _top_platform_y until comfortably above the screen top."""
        while self._top_platform_y > -200:
            y = self._top_platform_y - random.randint(60, 100)
            x = random.randint(40, SCREEN_W - Platform.WIDTH - 40)
            self.platforms.append(Platform((x, y)))
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
        """Remove platforms that have scrolled below the screen."""
        self.platforms = [p for p in self.platforms if p.position.y < SCREEN_H]

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
                jumper.jump()  # auto-jump on landing, Doodle Jump style
                break

    def _game_logic(self):
        for obj in self.game_objects:
            obj.update(self.screen)
        self._check_collisions()
        self._scroll_camera()
        self._cull_platforms()
        self._fill_platforms()

        # Game over: player fell off the bottom of the screen
        if self.jumper.position.y > SCREEN_H:
            self.running = False

    def _draw(self):
        self.screen.fill(pygame.Color("skyblue"))
        for obj in self.game_objects:
            obj.draw(self.screen)

        score_surf = self.font.render(f"Score: {self.score}", True, pygame.Color("black"))
        self.screen.blit(score_surf, (10, 10))

        pygame.display.flip()
        self.clock.tick(60)
