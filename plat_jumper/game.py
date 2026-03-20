import pygame
from entities import Jumper

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
        return [self.jumper]

    def _game_logic(self):
        for obj in self.game_objects:
            obj.update(self.screen)

    def _draw(self):
        self.screen.fill(pygame.Color("skyblue"))
        for obj in self.game_objects:
            obj.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(60)