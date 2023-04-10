import pygame

from module import *


if __name__=='__main__':

    pygame.init()

    # sets the window title
    pygame.display.set_caption("Test Game Menu")

    # Set up the drawing window
    screen = pygame.display.set_mode((800,800))

    menu = GameMenu(game_width=800,game_height=800)
    kwargs = {
        "font_size":32,
        "font_color":Colors.RGB('white'),
        "txt_box_fill":False,
        "txt_box_color":Colors.RGB("white"),
        "txt_box_shadow":Colors.RGB("gray"),
        "txt_box_fill_roll":Colors.RGB('purple'),
        "roll_fg_color":Colors.RGB("purple"),
        "roll_bg_color":Colors.RGB("orchid"),
        "drop_txt_shadow":1
    }
    menu.addChoice(card_text="Edit Profile",**kwargs)
    menu.addChoice(card_text="View High Scores",**kwargs)
    menu.addChoice(card_text="Start Game",**kwargs)

    # Run until the user asks to quit
    # Basic game loop
    running = True
    while running:

        #screen.fill((0,0,0))

        events = pygame.event.get()
        # Did the user click the window close button?
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            # Not used in this instance of our game
            if event.type == pygame.MOUSEBUTTONUP:
                # debug(pygame.mouse.get_pos(),10)
                pass
        menu.render(screen)
        menu.handle_events(events)
        menu.update()

        pygame.display.flip()

    pygame.quit()
