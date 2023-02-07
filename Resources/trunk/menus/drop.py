import pygame

# Initialize Pygame
pygame.init()

# Set screen size and title
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Dropdown Menu")

# Define colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Dropdown menu options


# Draw the dropdown menu
class Menu:
    def __init__(self, **kwargs):
        self.menu_width = kwargs.get("menu_width", 150)
        self.menu_height = kwargs.get("menu_width", 50)
        self.menu_x = kwargs.get("menu_x", 50)
        self.menu_y = kwargs.get("menu_y", 50)
        self.options = kwargs.get("options", ["Message", "Broadcast", "Fire"])
        self.selected_option = kwargs.get("selected_option", 0)

        # Draw the background
        pygame.draw.rect(
            screen, GRAY, (self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        )

        # Draw the selected option
        self.font = pygame.font.Font(None, 20)
        self.text = self.font.render(self.options[self.selected_option], True, BLACK)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (
            self.menu_x + self.menu_width // 2,
            self.menu_y + self.menu_height // 2,
        )
        screen.blit(self.text, self.text_rect)

        # Update the screen
        pygame.display.update()

    # Draw the dropdown menu
    def draw_dropdown_menu(self):
        self.menu_width = 150
        self.menu_height = 50
        self.menu_x = 50
        self.vmenu_y = 50

        # Draw the background
        pygame.draw.rect(
            screen, GRAY, (self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        )

        text = self.font.render(self.options[self.selected_option], True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (
            self.menu_x + self.menu_width // 2,
            self.menu_y + self.menu_height // 2,
        )
        screen.blit(text, text_rect)

        # Update the screen
        pygame.display.update()


menu = Menu(
    menu_width=150,
    menu_height=50,
    menu_x=50,
    menu_y=50,
    options=["Message", "Broadcast", "Fire"],
)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            # Check if the menu was clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            menu_width = 150
            menu_height = 50
            menu_x = 50
            menu_y = 50
            if (
                menu.menu_x <= mouse_x <= menu.menu_x + menu_width
                and menu.menu_y <= mouse_y <= menu.menu_y + menu_height
            ):
                # Toggle the selected option
                menu.selected_option = (menu.selected_option + 1) % len(menu.options)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the dropdown menu
    menu.draw_dropdown_menu()

    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()
