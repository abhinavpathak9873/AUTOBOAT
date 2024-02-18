import pygame
import sys

# Set up display
width, height = 1200, 800
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("IFOR CB 23 Simulator")
background_color = (69, 212, 255)

running = True

while running:
    screen.fill(background_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    pygame.display.update()

pygame.quit()
sys.exit()
