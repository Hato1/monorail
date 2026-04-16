"""Tile entity representing a single tile in the game world."""

import pygame as pg

from monorail import constants
from monorail.utils.asset_manager import Image
from monorail.utils.vector import Direction, Vector2


class TileType:
    """Class representing different types of tiles in the game."""

    image = Image.BANK

    def __init__(self, tile_grid: TileGrid, position_gd: Vector2, position_px: Vector2):
        self.tile_grid: TileGrid = tile_grid
        self.position_gd: Vector2 = position_gd
        self.position_px: Vector2 = position_px

    @property
    def name(self) -> str:
        return type(self).__name__

    def get_neighbor(self, direction: Direction):
        return self.tile_grid.get_neighbor(self.position_gd, direction)

    def setup(self):
        """Perform any additional setup for the tile type."""
        pass

    def draw(self, surface):
        """Draw the tile type's image at the given position on the surface."""
        image = self.image.load()
        surface.blit(image, self.position_px)


class TileTypeBank(TileType):
    image = Image.BANK

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TileTypeRadio(TileType):
    image = Image.RADIO

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TileTypeRail(TileType):
    def __init__(self, *args, valid_directions: set[Direction], **kwargs):
        super().__init__(*args, **kwargs)
        self.neighbors: dict[Direction, TileTypeRail | None] = {direction: None for direction in valid_directions}

    def get_connected_rail(self, direction: Direction) -> TileTypeRail | None:
        neighbor = self.get_neighbor(direction)
        if isinstance(neighbor, TileTypeRail):
            if direction in self.neighbors and -direction in neighbor.neighbors:
                return neighbor
        return None


class TileTypeRailNS(TileTypeRail):
    image = Image.RAIL_NS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.UP, Direction.DOWN})


class TileTypeRailEW(TileTypeRail):
    image = Image.RAIL_EW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.LEFT, Direction.RIGHT})


class TileTypeRailNE(TileTypeRail):
    image = Image.RAIL_NE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.UP, Direction.RIGHT})


class TileTypeRailSE(TileTypeRail):
    image = Image.RAIL_SE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.RIGHT, Direction.DOWN})


class TileTypeRailSW(TileTypeRail):
    image = Image.RAIL_SW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.DOWN, Direction.LEFT})


class TileTypeRailNW(TileTypeRail):
    image = Image.RAIL_NW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.LEFT, Direction.UP})


class TileTypeRailNES(TileTypeRail):
    image = Image.RAIL_NES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.UP, Direction.RIGHT, Direction.DOWN})


class TileTypeRailESW(TileTypeRail):
    image = Image.RAIL_ESW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.RIGHT, Direction.DOWN, Direction.LEFT})


class TileTypeRailSWN(TileTypeRail):
    image = Image.RAIL_NSW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.DOWN, Direction.LEFT, Direction.UP})


class TileTypeRailNWE(TileTypeRail):
    image = Image.RAIL_NEW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, valid_directions={Direction.LEFT, Direction.UP, Direction.RIGHT})


class TileTypeRailNESW(TileTypeRail):
    image = Image.RAIL_NESW

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, **kwargs, valid_directions={Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT}
        )


#     def __repr__(self):
#         return f"Tile(position={self.position}, tile_type='{self.tile_type}')"


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
        self.tiles: list[list[TileType | None]] = [[None for _ in range(height)] for _ in range(width)]

        center = Vector2(self.width, self.height) // 2
        center_px = center * constants.TILE_SIZE
        self.start_tile = TileTypeRailNS(self, center, center_px)
        center_asint = center.as_int()
        self.tiles[center_asint[0]][center_asint[1]] = self.start_tile

    def get_neighbor(self, position_gd: Vector2, direction: Direction) -> TileType | None:
        x, y = (position_gd + direction).as_int()
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y]
        return None

    def set_tile(self, position: tuple[int, int], tile_type: type[TileType]):
        """Set a tile at the given grid coordinates."""
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            position_px = Vector2(x * constants.TILE_SIZE, y * constants.TILE_SIZE)
            new_tile = tile_type(self, Vector2(*position), position_px)
            self.tiles[x][y] = new_tile
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
