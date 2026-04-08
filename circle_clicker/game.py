"""
🎯 Klikk-spillet
Konsept: En sirkel dukker opp på et tilfeldig sted på skjermen. Klikk på den før tiden går ut – og prøv å få høyest mulig score!
Krav:

En farget sirkel vises på en tilfeldig posisjon
Klikker du på den: +1 poeng, ny sirkel dukker opp
Du har 10 sekunder totalt
Vis gjenværende tid og score på skjermen
Når tiden er ute: vis "Game Over" og din score

Strekk-mål (hvis du blir fort ferdig):

Sirkelen krymper jo lenger du venter (press!)
Høyere poeng jo raskere du klikker


"""

import pygame
from random import randint


# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Klikk")
clock = pygame.time.Clock()
font = pygame.font.SysFont("console", 36)

score = 0
timer = 2
time_out = False

# Circle setup
circle_radius = 20
circle_pos = (400, 400)

# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    screen.fill((0, 0, 0))

    # Draw circle
    circle_rect = pygame.draw.circle(screen, (255, 255, 255), circle_pos, circle_radius)

    # Check if mouse clicks on circle
    mouse_pos = pygame.mouse.get_pos()
    if circle_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not time_out:
        circle_pos = (randint(0 + circle_radius, WIDTH - circle_radius), randint(0 + circle_radius, HEIGHT - circle_radius))
        score += 1
        timer = 2

    # Update timer
    if timer > 0: timer -= dt
    else: timer = 0
    if timer <= 0:
        time_out = True

    # Draw score on screen
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    timer_text = font.render(f"Timer: {round(timer, 1)}", True, (255, 255, 255))
    screen.blit(timer_text, (550, 10))

    # Game over text
    if time_out:
        game_over_text = font.render(f"Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH / 2 - 100, HEIGHT / 2 - 20))

    pygame.display.flip()

pygame.quit()