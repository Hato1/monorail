import pygame as pg

from monorail import constants
from monorail.utils.vector import Vector2


class BottomBar:
    """Class representing the bottom bar UI element where the player can access quick actions and view important information.

    Attributes:
        position: The top-left position of the bottom bar on the screen.
    """

    border_width = 2
    border_color = "black"

    def __init__(self, position: Vector2):
        self.position = position

    def draw_border(self, surface: pg.Surface):
        """Draw a border around the bottom bar for visual separation from the main game area."""
        border_rect = (*self.position, constants.SCREEN_SIZE[0], constants.BOTTOM_BAR_HEIGHT)
        pg.draw.rect(surface, pg.Color(self.border_color), border_rect, self.border_width)

    def draw(self, surface: pg.Surface):
        self.draw_border(surface)
        _position = self.position + Vector2(10, 10)  # Padding from the border
