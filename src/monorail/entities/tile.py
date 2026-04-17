"""Tile entity representing a single tile in the game world."""

import pygame as pg

from monorail import constants
from monorail.utils.asset_manager import Image
from monorail.utils.vector import Direction, Vector2


class Tile:
    """Class representing different types of tiles in the game."""

    image = Image.BANK

    def __init__(self, tile_grid: TileGrid, position_gd: Vector2):
        self.tile_grid: TileGrid = tile_grid
        self.position_gd: Vector2 = position_gd

    @property
    def name(self) -> str:
        return type(self).__name__

    @property
    def position_px(self):
        return self.position_gd * constants.TILE_SIZE

    def get_neighbor(self, direction: Direction):
        return self.tile_grid.get_neighbor(self.position_gd, direction)

    def setup(self):
        """Perform any additional setup for the tile type."""
        pass

    def draw(self, surface):
        """Draw the tile type's image at the given position on the surface."""
        image = self.image.load()
        surface.blit(image, self.position_px)

    def __repr__(self):
        return f"Tile(position={self.position_gd}, name='{self.name}')"


class TileBank(Tile):
    image = Image.BANK

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TileRadio(Tile):
    image = Image.RADIO

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TileRail(Tile):
    def __init__(self, *args, valid_directions: set[Direction], **kwargs):
        super().__init__(*args, **kwargs)
        self.neighbors: dict[Direction, TileRail | None] = {direction: None for direction in valid_directions}

    def get_connected_rail(self, direction: Direction) -> TileRail | None:
        neighbor = self.get_neighbor(direction)
        if isinstance(neighbor, TileRail):
            if direction in self.neighbors and -direction in neighbor.neighbors:
                return neighbor
        return None


class TileRailNS(TileRail):
    image = Image.RAIL_NS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.UP, Direction.DOWN})


class TileRailEW(TileRail):
    image = Image.RAIL_EW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.LEFT, Direction.RIGHT})


class TileRailNE(TileRail):
    image = Image.RAIL_NE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.UP, Direction.RIGHT})


class TileRailSE(TileRail):
    image = Image.RAIL_SE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.RIGHT, Direction.DOWN})


class TileRailSW(TileRail):
    image = Image.RAIL_SW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.DOWN, Direction.LEFT})


class TileRailNW(TileRail):
    image = Image.RAIL_NW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.LEFT, Direction.UP})


class TileRailNES(TileRail):
    image = Image.RAIL_NES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.UP, Direction.RIGHT, Direction.DOWN})


class TileRailESW(TileRail):
    image = Image.RAIL_ESW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.RIGHT, Direction.DOWN, Direction.LEFT})


class TileRailSWN(TileRail):
    image = Image.RAIL_NSW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.DOWN, Direction.LEFT, Direction.UP})


class TileRailNWE(TileRail):
    image = Image.RAIL_NEW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.LEFT, Direction.UP, Direction.RIGHT})


class TileRailNESW(TileRail):
    image = Image.RAIL_NESW

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, **kwargs, valid_directions={Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT}
        )


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

        center = Vector2(self.width, self.height) // 2
        self.start_tile = TileRailNS(self, center)
        self.tiles[center.x][center.y] = self.start_tile

    def is_in_grid(self, position: Vector2) -> bool:
        rect = pg.Rect(0, 0, self.width, self.height)
        return rect.collidepoint(position)

    def get_neighbor(self, position_gd: Vector2, direction: Direction) -> Tile | None:
        position = position_gd + direction
        if self.is_in_grid(position):
            return self.tiles[position.x][position.y]
        return None

    def set_tile(self, position: Vector2, tile_type: type[Tile]):
        """Set a tile at the given grid coordinates."""
        if self.is_in_grid(position):
            self.tiles[position.x][position.y] = tile_type(self, position)
        else:
            raise IndexError(f"Tile coordinates out of bounds: ({position})")

    def draw(self, surface):
        """Draw all tiles in the grid on the given surface."""

        # Draw grid
        for i in range(0, self.width * constants.TILE_SIZE, constants.TILE_SIZE):
            pg.draw.line(surface, pg.Color("darkgray"), (i, 0), (i, self.height * constants.TILE_SIZE))
        for j in range(0, self.height * constants.TILE_SIZE, constants.TILE_SIZE):
            pg.draw.line(surface, pg.Color("darkgray"), (0, j), (self.width * constants.TILE_SIZE, j))

        # Draw tiles
        for column in self.tiles:
            for tile in column:
                if tile:
                    tile.draw(surface)
