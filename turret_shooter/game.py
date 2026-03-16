import pygame
from models import GameObject
from utils import load_sprite


class TurretShooter:
    def __init__(self):
        # Init pygama
        pygame.init()
        pygame.display.set_caption("Turret Shooter")
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)

        # Load spaceship
        sprite = load_sprite("turret2")
        self.ship = GameObject((400, 300), sprite, (0, 0))

        # Load astroid
        sprite = load_sprite("astroid")
        self.astroid = GameObject((50, 300), sprite, (1, 0))

        self.collision_count = 0

        self.running = True

    def main_loop(self):
        while self.running:
            self._handle_input()
            self._game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Quit if q is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False

    def _game_logic(self):
        # Where objects can be moved around
        self.ship.move()
        self.astroid.move()

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.ship.draw(self.screen)
        self.astroid.draw(self.screen)

        if self.ship.collides_with(self.astroid):
            self.collision_count += 1
            print(f"Collision #{self.collision_count}")

        pygame.display.flip()
        self.clock.tick(60)

