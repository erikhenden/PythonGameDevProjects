from game import TurretShooter
import pygame

if __name__ == '__main__':
    game = TurretShooter()
    game.main_loop()
    pygame.quit()