"""Tile entity representing a single tile in the game world."""

import pygame as pg

from monorail import constants
from monorail.utils.asset_manager import Image
from monorail.utils.vector import Vector2


class TileType:
    """Class representing different types of tiles in the game."""

    def __init__(self, image: Image):
        self.image = image

    @property
    def name(self) -> str:
        return type(self).__name__

    def draw(self, surface, position: Vector2):
        """Draw the tile type's image at the given position on the surface."""
        image = self.image.load()
        surface.blit(image, position)


class TileTypeBank(TileType):
    def __init__(self):
        super().__init__(Image.BANK)


class TileTypeRadio(TileType):
    def __init__(self):
        super().__init__(Image.RADIO)


class Tile:
    def __init__(self, position: Vector2, tile_type: TileType):
        self.position = position
        self.tile_type = tile_type

    def draw(self, surface):
        """Draw the tile on the given surface."""
        self.tile_type.draw(surface, self.position)

    def __repr__(self):
        return f"Tile(position={self.position}, tile_type='{self.tile_type}')"


class TileGrid:
    """Class representing the grid of tiles in the game world."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles: list[list[Tile | None]] = [[None for _ in range(height)] for _ in range(width)]

    def set_tile(self, x: int, y: int, tile_type: TileType):
        """Set a tile at the given grid coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            position = Vector2(x * constants.TILE_SIZE, y * constants.TILE_SIZE)
            self.tiles[x][y] = Tile(position, tile_type)
        else:
            raise IndexError(f"Tile coordinates out of bounds: ({x}, {y})")

    def draw(self, surface):
        """Draw all tiles in the grid on the given surface."""
        for i in range(0, self.width * constants.TILE_SIZE, constants.TILE_SIZE):
            pg.draw.line(surface, pg.Color("darkgray"), (i, 0), (i, self.height * constants.TILE_SIZE))
        for j in range(0, self.height * constants.TILE_SIZE, constants.TILE_SIZE):
            pg.draw.line(surface, pg.Color("darkgray"), (0, j), (self.width * constants.TILE_SIZE, j))

        for column in self.tiles:
            for tile in column:
                if tile:
                    tile.draw(surface)
