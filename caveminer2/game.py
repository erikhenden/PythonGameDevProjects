import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.running = True
        self.bg = pygame.Color('lightgreen')

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

    def _game_logic(self):
        # Update / move game objects
        pass

    def _draw(self):
        self.screen.fill(self.bg)
        pygame.display.flip()
        self.clock.tick(self.FPS)

    @staticmethod
    def quit():
        pygame.quit()