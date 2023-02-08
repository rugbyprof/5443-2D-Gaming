"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MAZE
Maze solver app, an improved version from https://github.com/ChrisKneller/pygame-pathfinder.
License: GNU General Public License v3.0
"""

__all__ = ["MessageApp"]

import heapq
import pygame
import pygame_menu
import pygame_menu.utils as ut
import random
import time

from collections import deque
from math import inf
from typing import List, Union, Optional, Tuple, Any, Generator

from pygame_menu.examples import create_example_window

# Define some colors
BACKGROUND = (34, 40, 44)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (186, 127, 50)
DARK_BLUE = (0, 0, 128)
DARK_GREEN = (0, 128, 0)
GREEN = (0, 255, 0)
GREY = (143, 143, 143)
LIGHT_BLUE = (0, 111, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


class MessageApp(object):
    """
    Maze class.
    """

    _height: int
    _margin: int
    _menu: "pygame_menu.Menu"
    _height: int
    _width: int

    def __init__(self, width: int = 900, height: int = 650, margin: int = 0) -> None:
        """
        Creates the maze.

        :param width: Width of each cell
        :param rows: Number of rows
        :param margin: Margin between cells
        """
        # Create the maze
        self._height = height  # so they are squares
        self._margin = margin
        self._offset = (25, 25)  # Maze offset within window
        self._width = width

        # Create the window
        self._clock = pygame.time.Clock()
        self._fps = 60
        self._surface = create_example_window("Message Sender", (width, height))

        # Setups the menu
        self._setup_menu()

    def send_message(self):
        pass

    def _setup_menu(self) -> None:
        """
        Setups the menu.
        """

        # Creates the events
        # noinspection PyUnusedLocal
        def onchange_dropselect(*args) -> None:
            """
            Called if the select is changed.
            """
            b = self._menu.get_widget("run_generator")
            b.readonly = False
            b.is_selectable = True
            b.set_cursor(pygame_menu.locals.CURSOR_HAND)

        def button_onmouseover(w: "pygame_menu.widgets.Widget", _) -> None:
            """
            Set the background color of buttons if entered.
            """
            if w.readonly:
                return
            w.set_background_color((98, 103, 106))

        def button_onmouseleave(w: "pygame_menu.widgets.Widget", _) -> None:
            """
            Set the background color of buttons if leaved.
            """
            w.set_background_color((75, 79, 81))

        def button_onmouseover_clear(w: "pygame_menu.widgets.Widget", _) -> None:
            """
            Set the background color of buttons if entered.
            """
            if w.readonly:
                return
            w.set_background_color((139, 0, 0))

        def button_onmouseleave_clear(w: "pygame_menu.widgets.Widget", _) -> None:
            """
            Set the background color of buttons if leaved.
            """
            w.set_background_color((205, 92, 92))

        def _visualize(value: bool) -> None:
            """
            Changes visualize.
            """
            self._visualize = value

        theme = pygame_menu.Theme(
            background_color=pygame_menu.themes.TRANSPARENT_COLOR,
            title=False,
            widget_font=pygame_menu.font.FONT_FIRACODE,
            widget_font_color=(255, 255, 255),
            widget_margin=(0, 15),
            widget_selection_effect=pygame_menu.widgets.NoneSelection(),
        )
        self._menu = pygame_menu.Menu(
            height=self._height,
            mouse_motion_selection=True,
            position=(645, 25, False),
            theme=theme,
            title="",
            width=self._width,
        )

        self._menu.add.label(
            "Command",
            font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
            font_size=22,
            margin=(0, 5),
        ).translate(-12, 0)
        self._menu.add.dropselect(
            title="",
            items=[
                ("Message", "MESSAGE"),
                ("Broadcast", "BROADCAST"),
                ("Fire", "FIRE"),
            ],
            dropselect_id="command",
            font_size=16,
            onchange=onchange_dropselect,
            padding=0,
            placeholder="Select one",
            selection_box_height=5,
            selection_box_inflate=(0, 20),
            selection_box_margin=0,
            selection_box_text_margin=10,
            selection_box_width=200,
            selection_option_font_size=20,
            shadow_width=20,
        )
        # self._menu.add.vertical_margin(10)
        # btn = self._menu.add.button(
        #     "Run Generator",
        #     self._run_generator,
        #     button_id="run_generator",
        #     font_size=20,
        #     margin=(0, 30),
        #     shadow_width=10,
        # )
        # btn.readonly = True
        # btn.is_selectable = False

        self._menu.add.label(
            "Target",
            font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
            font_size=22,
            margin=(0, 5),
        ).translate(-30, 0)
        self._menu.add.dropselect(
            title="",
            items=[
                ("Player-1", "Player-1"),
                ("Player-2", "Player-2"),
                ("Player-3", "Player-3"),
            ],
            default=0,
            dropselect_id="target",
            font_size=16,
            padding=0,
            placeholder="Select one",
            selection_box_height=5,
            selection_box_inflate=(0, 20),
            selection_box_margin=0,
            selection_box_text_margin=10,
            selection_box_width=200,
            selection_option_font_size=20,
            shadow_width=20,
        )
        self._menu.add.vertical_margin(10)
        # self._menu.add.button(
        #     "Run Solver",
        #     self._run_solver,
        #     button_id="run_solver",
        #     cursor=pygame_menu.locals.CURSOR_HAND,
        #     font_size=20,
        #     margin=(0, 75),
        #     shadow_width=10,
        # )

        # Clears
        btn = self._menu.add.button(
            "Send",
            self.send_message,
            background_color=(205, 92, 92),
            button_id="send",
            cursor=pygame_menu.locals.CURSOR_HAND,
            font_size=20,
            margin=(0, 30),
            shadow_width=10,
        )
        btn.set_onmouseover(button_onmouseover_clear)
        btn.set_onmouseleave(button_onmouseleave_clear)
        btn.translate(-50, 0)

        # Create about menu
        menu_about = pygame_menu.Menu(
            height=self._height - 20,
            mouse_motion_selection=True,
            position=(645, 8, False),
            theme=theme,
            title="",
            width=self._width // 4,
        )
        menu_about.add.label(
            "pygame-menu\nMaze",
            font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
            font_size=25,
            margin=(0, 5),
        )
        menu_about.add.vertical_margin(10)
        text = (
            "Left click to create a wall or move the start and end points.\n"
            "Hold left CTRL and left click to create a sticky mud patch (whi"
            "ch reduces movement speed to 1/3).\n"
        )
        text += (
            "The point of these mud patches is to showcase Dijkstra's algor"
            'ithm (first) and A* (second) by adjusting the "distances" betwe'
            "en the nodes.\n\n"
        )
        text += (
            "After a pathfinding algorithm has been run you can drag the sta"
            "rt/end points around and see the visualisation update instantly"
            " for the new path using the algorithm that was last run.\n"
        )
        menu_about.add.label(
            text,
            font_name=pygame_menu.font.FONT_FIRACODE,
            font_size=12,
            margin=(0, 5),
            max_char=-1,
            padding=0,
        )
        menu_about.add.label(
            "License: GNU GPL v3.0",
            margin=(0, 5),
            font_name=pygame_menu.font.FONT_FIRACODE,
            font_size=12,
        )
        menu_about.add.url(
            "https://github.com/ChrisKneller/pygame-pathfinder",
            "ChrisKneller/pygame-pathfinder",
            font_name=pygame_menu.font.FONT_FIRACODE,
            font_size=12,
            font_color="#00bfff",
        )
        menu_about.add.vertical_margin(20)
        menu_about.add.button(
            "Back",
            pygame_menu.events.BACK,
            button_id="about_back",
            cursor=pygame_menu.locals.CURSOR_HAND,
            font_size=20,
            shadow_width=10,
        )

        btn = self._menu.add.button(
            "About",
            menu_about,
            button_id="about",
            float=True,
            font_size=20,
            margin=(0, 75),
            shadow_width=10,
        )
        btn.translate(50, 0)

        # Configure buttons
        for btn in self._menu.get_widgets(["send", "target", "about", "about_back"]):
            btn.set_onmouseover(button_onmouseover)
            btn.set_onmouseleave(button_onmouseleave)
            if not btn.readonly:
                btn.set_cursor(pygame_menu.locals.CURSOR_HAND)
            btn.set_background_color((75, 79, 81))

    def _check_esc(self) -> None:
        """
        Check if ESC button was pressed.
        """
        if self._visualize:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._visualize = False

    @staticmethod
    def _sleep(ms: float) -> None:
        """
        Sleep time.

        :param ms: Sleep time in milliseconds
        """
        time.sleep(ms)

    @staticmethod
    def _quit() -> None:
        """
        Quit app.
        """
        pygame.quit()
        exit()

    def mainloop(self, test: bool) -> None:
        """
        Executes the main loop of the app.

        :param test: If True, runs only 1 frame
        """
        print("Press [ESC] to skip process if Visualize is On")
        while True:

            # Application events
            events = pygame.event.get()

            # Update the menu
            self._menu.update(events)

            self._menu.draw(self._surface)

            # If a menu widget disable its active state, disable the events, this is due to
            # user can click outside a dropselection box, and that triggers to disable active
            # state. If so, the event is destroyed, thus avoiding clicking the canvas
            if (
                pygame_menu.events.MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE
                in self._menu.get_last_update_mode()[0]
            ):
                events = []

            for event in events:
                # User closes
                if event.type == pygame.QUIT:
                    self._quit()

                # Write in the board
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # Find out which keys have been pressed
                    pressed = pygame.key.get_pressed()

            # Update the app
            self._surface.fill(BACKGROUND)

            # Flip surface
            pygame.display.flip()

            # Update clock
            self._clock.tick(self._fps)

            # At first loop returns
            if test:
                break


def main(test: bool = False) -> "MessageApp":
    """
    Main function.

    :param test: Indicate function is being tested
    :return: App
    """
    app = MessageApp()
    app.mainloop(test)
    return app


if __name__ == "__main__":
    main()
