import pygame as pg

from monorail import constants
from monorail.entities.sidebar import Shop
from monorail.entities.tile import Tile, TileGrid
from monorail.utils.vector import Vector2


class Cursor:
    """Class for managing the cursor position and interactions in the game."""

    def __init__(self) -> None:
        self.position = Vector2(0, 0)  # Cursor position in pixels.
        self.selected_tile_type: type[Tile] | None = None  # The currently selected tile type for placement, if any.

    def handle_mouse_click(self, position: Vector2, tile_grid: TileGrid, shop: Shop):
        """Handle mouse click interactions.

        Check if the cursor is clicking on a grid cell and place the selected tile type there.
        """
        if position.x < constants.GRID_WIDTH * constants.TILE_SIZE:
            grid_position = position // constants.TILE_SIZE
            print(f"Clicked on grid cell: ({grid_position})")
            if self.selected_tile_type:
                tile_grid.set_tile(grid_position, self.selected_tile_type)
        else:
            print("Clicked outside the grid, on the sidebar or beyond.")
            for shelf in shop.shelves:
                for item_rect in shelf.item_rects:
                    if item_rect.collidepoint(position):
                        index = shelf.item_rects.index(item_rect)
                        self.selected_tile_type = shelf.items[index]
                        print(f"Selected tile type: {self.selected_tile_type}")
                        return

    def update(self):
        """Update the cursor position based on the current mouse position."""
        mouse_pos = pg.mouse.get_pos()
        self.position = Vector2(*mouse_pos)

    def draw(self, surface: pg.Surface):
        """Draw the cursor on the given surface."""
        if self.position.x < constants.GRID_WIDTH * constants.TILE_SIZE:
            top_left = self.position // constants.TILE_SIZE * constants.TILE_SIZE
            pg.draw.rect(surface, pg.Color("white"), (*top_left, constants.TILE_SIZE, constants.TILE_SIZE), 1)
