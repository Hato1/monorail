import pygame as pg

from monorail import constants
from monorail.entities.tile import TileGrid, TileTypeBank
from monorail.utils.vector import Vector2


class Cursor:
    """Class for managing the cursor position and interactions in the game."""

    def __init__(self):
        self.position = Vector2(0, 0)  # Cursor position in pixels.
        self.selected_tile_type = None  # The currently selected tile type for placement, if any.

        self.selected_tile_type = TileTypeBank()  # Default selected tile type for testing purposes.

    def handle_mouse_click(self, position: Vector2, tile_grid: TileGrid):
        """Handle mouse click interactions.

        Check if the cursor is clicking on a grid cell and place the selected tile type there.
        """
        grid_position = position // constants.TILE_SIZE
        print(f"Clicked on grid cell: ({grid_position})")
        if self.selected_tile_type:
            tile_grid.set_tile(int(grid_position.x), int(grid_position.y), self.selected_tile_type)

    def update(self):
        """Update the cursor position based on the current mouse position."""
        mouse_pos = pg.mouse.get_pos()
        self.position = Vector2(*mouse_pos)

    def draw(self, surface: pg.Surface):
        """Draw the cursor on the given surface."""
        top_left = self.position // constants.TILE_SIZE * constants.TILE_SIZE

        pg.draw.rect(surface, pg.Color("white"), (*top_left, constants.TILE_SIZE, constants.TILE_SIZE), 1)
