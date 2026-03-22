import pygame
from pygame.math import Vector2
from entitites import Shooter, Mouse, Bullet
import random
from utils import load_sprite, get_direction


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.FPS = 60
        self.running = True

        # Load images
        self.img_bullet = load_sprite("bullet")

        # Groups
        self.shooter_group = pygame.sprite.Group()
        self.mouse_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()

        # Add shooter
        self.shooter = Shooter((self.WIDTH // 2, self.HEIGHT // 2))
        self.shooter_group.add(self.shooter)

        # Add mice
        self.mouse_group.add([self._add_mouse()] for _ in range(5))

    def _add_mouse(self):
        while True:
            pos_x = random.randrange(self.WIDTH)
            pos_y = random.randrange(self.HEIGHT)
            pos = Vector2(pos_x, pos_y)
            if self.shooter.position.distance_to(pos) >= 200 and 0 <= pos_x < self.WIDTH + 75 and 0 <= pos_y < self.HEIGHT + 75:
                return Mouse(pos)

    def main_loop(self):
        while self.running:
            self._handle_events()
            self._game_logic()
            self._draw()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    direction = get_direction(Vector2(self.shooter.rect.center), Vector2(pygame.mouse.get_pos()))
                    self.bullet_group.add(Bullet(self.img_bullet, self.shooter.rect.center, direction))


    def _game_logic(self):
        dt = self.clock.tick(self.FPS) / 1000.0

        # Move game objects
        self.shooter_group.update()
        self.mouse_group.update(dt, self.screen)
        self.bullet_group.update(self.screen)

        """Collision checks"""
        # Bullet-mouse
        pygame.sprite.groupcollide(self.bullet_group, self.mouse_group, True, True)

    def _draw(self):
        self.screen.fill(pygame.Color("skyblue"))

        # Draw
        self.shooter_group.draw(self.screen)
        self.mouse_group.draw(self.screen)
        self.bullet_group.draw(self.screen)

        # Print text
        text = self.font.render(f"# Bullets: {len(self.bullet_group)}", True, pygame.Color("white"))
        self.screen.blit(text, (0, 0))

        # Draw line
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(self.screen, pygame.Color("black"), self.shooter.position, mouse_pos, 1)

        pygame.display.flip()

    @staticmethod
    def quit():
        pygame.quit()