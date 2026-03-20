import pygame
from models import GameObject, Turret
from pygame.transform import rotozoom
from utils import load_sprite


class TurretShooter:
    def __init__(self):
        # Init pygama
        pygame.init()
        pygame.display.set_caption("Turret Shooter")
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)

        # Load turret
        self.turret = Turret((400, 300))

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


        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_ESCAPE] or keypress[pygame.K_q]:
            quit()

        # Rotate
        elif keypress[pygame.K_d]:
            self.turret.rotate(clockwise=True)
        elif keypress[pygame.K_a]:
            self.turret.rotate(clockwise=False)

        # Accelerate
        elif keypress[pygame.K_w]:
            self.turret.accelerate()

    def _game_logic(self):
        # Where objects can be moved around
        self.turret.move(self.screen)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.turret.draw(self.screen)


        pygame.display.flip()
        self.clock.tick(60)

