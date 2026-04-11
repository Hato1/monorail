import pygame as pg

from monorail import constants
from monorail.utils.vector import Vector2


class Cursor:
    """Class for managing the cursor position and interactions in the game."""

    def __init__(self):
        self.position = Vector2(0, 0)  # Cursor position in pixels.

    def update(self):
        """Update the cursor position based on the current mouse position."""
        mouse_pos = pg.mouse.get_pos()
        self.position = Vector2(*mouse_pos)

    def draw(self, surface: pg.Surface):
        """Draw the cursor on the given surface."""
        top_left = self.position // constants.TILE_SIZE * constants.TILE_SIZE

        pg.draw.rect(surface, pg.Color("white"), (*top_left, constants.TILE_SIZE, constants.TILE_SIZE), 1)
