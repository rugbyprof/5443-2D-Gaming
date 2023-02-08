"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MULTI-INPUT
Shows different inputs (widgets).
"""

__all__ = ["main"]

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from typing import Tuple, Optional

# Constants and global variables
FPS = 60
WINDOW_SIZE = (640, 480)
TITLE = "Messenger"
TEAMLABEL = "Player: Player 1"

sound: Optional["pygame_menu.sound.Sound"] = None
surface: Optional["pygame.Surface"] = None
main_menu: Optional["pygame_menu.Menu"] = None


def main_background() -> None:
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    surface.fill((40, 40, 40))


def check_name_test(value: str) -> None:
    """
    This function tests the text input widget.

    :param value: The widget value
    """
    print(f"User name: {value}")


def update_menu_sound(value: Tuple, enabled: bool) -> None:
    """
    Update menu sound.

    :param value: Value of the selector (Label and index)
    :param enabled: Parameter of the selector, (True/False)
    """
    assert isinstance(value, tuple)
    if enabled:
        main_menu.set_sound(sound, recursive=True)
        print("Menu sounds were enabled")
    else:
        main_menu.set_sound(None, recursive=True)
        print("Menu sounds were disabled")


def add_dynamic_text(menu) -> "pygame_menu.widgets.Label":
    """
    Append a button to the menu on demand.
    :return: Appended button
    """
    print(f"Adding a button dynamically, total: {len(menu.get_widgets()) - 2}")
    txt = menu.add.label()

    # def _update_button() -> None:
    #     count = btn.get_counter_attribute("count", 1, btn.get_title())
    #     btn.set_title(str(count))

    # btn.update_callback(_update_button)
    # return btn


def handleSubmit():
    print("submitted!")


def main(test: bool = False) -> None:
    """
    Main program.

    :param test: Indicate function is being tested
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface

    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface = create_example_window("Message Example", WINDOW_SIZE)
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Set sounds
    # -------------------------------------------------------------------------
    sound = pygame_menu.sound.Sound()

    # Load example sounds
    sound.load_example_sounds()

    # Disable a sound
    sound.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, None)

    # -------------------------------------------------------------------------
    # Create menus: Settings
    # -------------------------------------------------------------------------
    settings_menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
    settings_menu_theme.title_offset = (5, -2)
    settings_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    settings_menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
    settings_menu_theme.widget_font_size = 20

    settings_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.85,
        theme=settings_menu_theme,
        title=f"{TITLE}",
        width=WINDOW_SIZE[0] * 0.9,
    )

    settings_menu.add.label(
        f"{TEAMLABEL}", align=pygame_menu.locals.ALIGN_LEFT, font_size=20
    )

    # Selectable items
    commands = [("Message", "MESSAGE"), ("Broadcast", "BROADCAST"), ("Fire", "FIRE")]

    settings_menu.add.dropselect(
        "Select Command:", commands, default=1, dropselect_id="command_drop"
    )

    targets = [
        ("Player-1", "Player-1"),
        ("Player-2", "Player-2"),
        ("Player-3", "Player-3"),
    ]

    settings_menu.add.dropselect(
        "Select Target:", targets, default=1, dropselect_id="target_drop"
    )

    # {"lon":-37.234,"lat":97.2234}
    settings_menu.add.text_input(
        "Command Body: ",
        maxwidth=19,
        textinput_id="cmd_text",
        input_underline="_",
        copy_paste_enable=True,
        # cursor_color=(0, 255, 0),
        cursor_selection_enable=True,
    )

    settings_menu.add.label(
        f"hello",
        align=pygame_menu.locals.ALIGN_LEFT,
        font_size=12,
        font_color=(0, 255, 0),
        label_id="message",
    )

    settings_menu.add.button(
        "Submit",
        handleSubmit,
        button_id="handleSubmit",
        cursor=pygame_menu.locals.CURSOR_HAND,
        font_size=20,
        margin=(0, 75),
        shadow_width=10,
    )
    settings_menu.add.button("Quit", pygame_menu.events.EXIT)

    font = pygame.font.Font("Roboto-Bold.ttf", 20)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Main menu
        settings_menu.mainloop(
            surface, main_background, disable_loop=test, fps_limit=FPS
        )

        # text = font.render("XXXXXXXXX", True, (0, 0, 0))
        # textRect = text.get_rect()
        # textRect.right = 500
        # textRect.bottom = 300
        # surface.blit(text, textRect)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == "__main__":
    main()
