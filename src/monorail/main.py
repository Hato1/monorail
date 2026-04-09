"""Run the program."""

import pygame as pg

import monorail.initialise_pygame  # noqa: F401
from monorail.states.game import Game
from monorail.states.main_menu import MainMenu
from monorail.utils.state_manager import State, StateManager

ORIGINAL_CAPTION = "My Game"
SCREEN_SIZE = (128, 128)


def main():
    """Run the program."""

    # Initialization
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED)
    assert screen is not None, "Pygame display surface not initialized."
    pg.display.set_caption(ORIGINAL_CAPTION)

    # Add states to StateManager here.
    state_dict: dict[type[State], State] = {MainMenu: MainMenu(), Game: Game()}
    state_manager = StateManager(screen, state_dict, MainMenu, ORIGINAL_CAPTION)

    # Run main loop.
    state_manager.main()

    pg.quit()


if __name__ == "__main__":
    main()
