import pygame

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Camera Movement Example")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create some world objects (rectangles)
world_objects = [
    pygame.Rect(100, 100, 50, 50),
    pygame.Rect(400, 300, 80, 80),
    pygame.Rect(700, 500, 60, 60),
    pygame.Rect(1200, 800, 100, 100)
]

# Camera offset
camera_x, camera_y = 0, 0
camera_speed = 5

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling for camera movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= camera_speed
    if keys[pygame.K_RIGHT]:
        camera_x += camera_speed
    if keys[pygame.K_UP]:
        camera_y -= camera_speed
    if keys[pygame.K_DOWN]:
        camera_y += camera_speed

    # Clear screen
    screen.fill(WHITE)

    # Draw world objects with camera offset
    for obj in world_objects:
        # Apply camera offset (negative because moving camera right means world moves left)
        draw_rect = obj.move(-camera_x, -camera_y)
        pygame.draw.rect(screen, GREEN, draw_rect)

    # Draw a fixed player in the center of the screen
    player_rect = pygame.Rect(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25, 50, 50)
    pygame.draw.rect(screen, RED, player_rect)

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()