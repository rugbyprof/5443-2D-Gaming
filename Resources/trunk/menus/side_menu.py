import pygame

# Initialize Pygame
pygame.init()

# Set screen size and title
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Side Menu")

# Define colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Draw the side menu
def draw_side_menu():
    menu_width = 150
    menu_rect = pygame.Rect(0, 0, menu_width, 600)
    pygame.draw.rect(screen, GRAY, menu_rect)
    pygame.display.update()


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the side menu
    draw_side_menu()

    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()
