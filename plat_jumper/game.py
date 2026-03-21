import pygame
from entities import Jumper, Platform

class Game:
    def __init__(self):
        self.running = True

        # Init pygame
        pygame.init()
        pygame.display.set_caption("Jumper")
        self.screen = pygame.display.set_mode((800,600))
        self.clock = pygame.time.Clock()

        # Add jumper
        self.jumper = Jumper((400, 300))

        # Starting platforms
        self.platforms = [
            Platform((320, 420)),
            Platform((150, 340)),
            Platform((500, 260)),
            Platform((240, 190)),
            Platform((420, 110)),
        ]

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

                # Jump
                if event.key == pygame.K_SPACE:
                    self.jumper.jump()

        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_a]:
            self.jumper.move_sideways(False)
        elif keypress[pygame.K_d]:
            self.jumper.move_sideways(True)


    @property
    def game_objects(self):
        return [self.jumper] + self.platforms

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

            # Skip if no horizontal overlap
            if j_right <= p_left or j_left >= p_right:
                continue

            # Land if feet crossed the platform top this frame (pass-through from below allowed)
            if j_bottom_prev <= p_top <= j_bottom:
                jumper.position.y = p_top - jumper.height
                jumper.velocity.y = 0
                break

    def _game_logic(self):
        for obj in self.game_objects:
            obj.update(self.screen)
        self._check_collisions()

    def _draw(self):
        self.screen.fill(pygame.Color("skyblue"))
        for obj in self.game_objects:
            obj.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(60)