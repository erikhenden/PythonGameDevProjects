import pygame
from world import draw


class Game:
    def __init__(self):

        # Setup pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.running = True

    def main_loop(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self._handle_events()
            self._game_logic(dt)
            self._draw()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _game_logic(self, dt):
        pass

    def _draw(self):
        # Draw
        draw(self.screen)

        pygame.display.flip()

    def quit(self):
        self.running = False