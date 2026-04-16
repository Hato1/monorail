"""Tile entity representing a single tile in the game world."""

import pygame as pg

from monorail import constants
from monorail.utils.asset_manager import Image
from monorail.utils.vector import Direction, Vector2


class TileType:
    """Class representing different types of tiles in the game."""

    def __init__(self, image: Image = Image.BANK):
        self.image = image

    @property
    def name(self) -> str:
        return type(self).__name__

    def setup(self, tile_grid: TileGrid, grid_position: tuple[int, int]):
        """Perform any additional setup for the tile type."""
        pass

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


class TileTypeRail(TileType):
    def __init__(self, image: Image, valid_directions: set[Direction]):
        super().__init__(image)
        self.neighbors: dict[Direction, TileTypeRail | None] = {direction: None for direction in valid_directions}

    def setup(self, tile_grid: TileGrid, grid_position: tuple[int, int]):
        """Connect the tile to neighboring rail tiles in the grid."""
        x, y = grid_position
        for direction in self.neighbors:
            neighbor_pos = Vector2(x, y) + direction.value
            if 0 <= neighbor_pos.x < tile_grid.width and 0 <= neighbor_pos.y < tile_grid.height:
                neighbor_tile = tile_grid.tiles[int(neighbor_pos.x)][int(neighbor_pos.y)]
                if isinstance(neighbor_tile, Tile) and isinstance(neighbor_tile.tile_type, TileTypeRail):
                    neighbor_rail: TileTypeRail = neighbor_tile.tile_type
                    if -direction in neighbor_rail.neighbors:
                        self.neighbors[direction] = neighbor_rail
                        neighbor_rail.neighbors[-direction] = self


class TileTypeRailNS(TileTypeRail):
    def __init__(self):
        super().__init__(Image.RAIL_NS, {Direction.UP, Direction.DOWN})


class TileTypeRailEW(TileTypeRail):
    def __init__(self):
        super().__init__(Image.RAIL_EW, {Direction.LEFT, Direction.RIGHT})


class TileTypeRailNE(TileTypeRail):
    def __init__(self):
        super().__init__(Image.RAIL_NE, {Direction.UP, Direction.RIGHT})


class TileTypeRailSE(TileTypeRail):
    def __init__(self):
        super().__init__(Image.RAIL_SE, {Direction.RIGHT, Direction.DOWN})


class TileTypeRailSW(TileTypeRail):
    def __init__(self):
        super().__init__(Image.RAIL_SW, {Direction.DOWN, Direction.LEFT})


class TileTypeRailNW(TileTypeRail):
    def __init__(self):
        super().__init__(Image.RAIL_NW, {Direction.LEFT, Direction.UP})


class TileTypeRailNES(TileTypeRail):
    def __init__(self):
        super().__init__(Image.RAIL_NES, {Direction.UP, Direction.RIGHT, Direction.DOWN})


class TileTypeRailESW(TileTypeRail):
    def __init__(self):
        super().__init__(Image.RAIL_ESW, {Direction.RIGHT, Direction.DOWN, Direction.LEFT})


class TileTypeRailSWN(TileTypeRail):
    def __init__(self):
        super().__init__(Image.RAIL_NSW, {Direction.DOWN, Direction.LEFT, Direction.UP})


class TileTypeRailNWE(TileTypeRail):
    def __init__(self):
        super().__init__(Image.RAIL_NEW, {Direction.LEFT, Direction.UP, Direction.RIGHT})


class TileTypeRailNESW(TileTypeRail):
    def __init__(self):
        super().__init__(Image.RAIL_NESW, {Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT})


class Tile:
    def __init__(self, position: Vector2, tile_type: TileType):
        self.position = position
        self.tile_type = tile_type

    def setup(self):
        """Perform any additional setup for the tile based on its type."""
        if isinstance(self.tile_type, TileTypeRail):
            # For road tiles, we might want to initialize additional properties or connections here.
            pass

    def draw(self, surface):
        """Draw the tile on the given surface."""
        self.tile_type.draw(surface, self.position)

    def __repr__(self):
        return f"Tile(position={self.position}, tile_type='{self.tile_type}')"


class TileGrid:
    """Class representing the grid of tiles in the game world."""

    def __init__(self, width: int, height: int):
        """Init a grid of the given width and height, filled with None (no tile).

        Args:
            width (int): Number of tiles in the horizontal direction.
            height (int): Number of tiles in the vertical direction.
        """
        self.width = width
        self.height = height
        self.tiles: list[list[Tile | None]] = [[None for _ in range(height)] for _ in range(width)]

    def set_tile(self, position: tuple[int, int], tile_type: TileType):
        """Set a tile at the given grid coordinates."""
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            position_px = Vector2(x * constants.TILE_SIZE, y * constants.TILE_SIZE)
            new_tile = Tile(position_px, tile_type)
            self.tiles[x][y] = new_tile
            new_tile.setup()  # Call setup to initialize any additional properties based on the tile type
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
