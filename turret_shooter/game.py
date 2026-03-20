import pygame
from models import Turret, Rock
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

        self.bullets = []

        # Load turret
        self.turret = Turret((400, 300), self.bullets)

        # Load Rocks
        self.rocks = [Rock(self.screen, self.turret.position) for _ in range(6)]

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.turret is not None:
                    self.turret.shoot()


        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_ESCAPE] or keypress[pygame.K_q]:
            quit()

        # Exit input handling method early if turret does not exist
        if self.turret is None:
            return

        # Rotate
        elif keypress[pygame.K_d]:
            self.turret.rotate(clockwise=True)
        elif keypress[pygame.K_a]:
            self.turret.rotate(clockwise=False)

        # Accelerate
        elif keypress[pygame.K_w]:
            self.turret.accelerate()

    # Returns a list of all the game objects in the game
    @property
    def game_objects(self):
        return [*self.rocks, *self.bullets, self.turret]

    def _game_logic(self):
        # Where objects can be moved around
        for obj in self.game_objects:
            if obj is not None:
                obj.move(self.screen)

        # Remove bullets off-screen
        rect = self.screen.get_rect()
        for bullet in self.bullets[:]:
            if not rect.collidepoint(bullet.position):
                self.bullets.remove(bullet)

        # Check bullet-rock collision
        for bullet in self.bullets[:]:
            for rock in self.rocks[:]:
                if rock.collides_with(bullet):
                    self.rocks.remove(rock)
                    self.bullets.remove(bullet)
                    break

        # Check turret-rock collision
        if self.turret:
            for rock in self.rocks[:]:
                if rock.collides_with(self.turret):
                    self.turret = None
                    break

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for obj in self.game_objects:
            if obj is not None:
                obj.draw(self.screen)


        pygame.display.flip()
        self.clock.tick(60)

