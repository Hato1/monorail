import pygame as pg

from monorail import constants
from monorail.entities import tile
from monorail.utils.asset_manager import Font
from monorail.utils.vector import Vector2


class Shelf:
    font: pg.Font = Font.m_small.load()
    gap_between_items = 3
    padding_between_title_and_items = 2

    def __init__(self, price: int, message: str, items: tuple[tile.TileTypeRail, ...]):
        self.price = price
        self.message = message
        self.items: tuple[tile.TileTypeRail, ...] = items
        self.item_rects: list[pg.Rect] = []  # List of rects for each item, used for click detection

    def draw_title(self, surface: pg.Surface, position: Vector2) -> int:
        message = f"${self.price} - {self.message}"
        text_surface = self.font.render(message, antialias=False, color=pg.Color("black"))
        surface.blit(text_surface, position)
        # Return the height of the title for layout purposes
        return text_surface.get_height() + self.padding_between_title_and_items

    def draw_items(self, surface: pg.Surface, position: Vector2):
        self.item_rects.clear()  # Clear the list before drawing new items
        for item in self.items:
            # Draw a light gray background for the item to make it stand out against the sidebar background
            item_rect = pg.Rect((*position, constants.TILE_SIZE, constants.TILE_SIZE))
            pg.draw.rect(surface, pg.Color("lightgray"), item_rect)
            item.draw(surface, position)
            self.item_rects.append(item_rect)  # Store the rect for click detection
            position += (constants.TILE_SIZE + self.gap_between_items, 0)  # Move right for the next item

    def draw(self, surface: pg.Surface, position: Vector2) -> int:
        """Draw the shelf's items at the given position on the surface. Returns the height of the shelf for layout purposes."""
        title_height = self.draw_title(surface, position)
        position += (0, title_height)
        self.draw_items(surface, position)

        return constants.TILE_SIZE + title_height + 5  # Total height of the shelf for layout purposes


class ShelfStraight(Shelf):
    def __init__(self):
        items = (tile.TileTypeRailNS(), tile.TileTypeRailEW())
        super().__init__(1, "Straight Rail", items)


class ShelfCurve(Shelf):
    def __init__(self):
        items = (tile.TileTypeRailNE(), tile.TileTypeRailSE(), tile.TileTypeRailSW(), tile.TileTypeRailNW())
        super().__init__(2, "Curved Rail", items)


class ShelfIntersection(Shelf):
    def __init__(self):
        items = (tile.TileTypeRailNES(), tile.TileTypeRailESW(), tile.TileTypeRailSWN(), tile.TileTypeRailNWE())
        super().__init__(5, "Intersections", items)


class ShelfStation(Shelf):
    def __init__(self):
        items = (tile.TileTypeRailNESW(),)
        super().__init__(9, "Stations", items)


class Shop:
    def __init__(self):
        self.shelves: list[Shelf] = []
        self.shelves.append(ShelfStraight())
        self.shelves.append(ShelfCurve())
        self.shelves.append(ShelfIntersection())
        self.shelves.append(ShelfStation())

    def draw(self, surface: pg.Surface, position: Vector2):
        for shelf in self.shelves:
            position += (0, shelf.draw(surface, position))


class Sidebar:
    """Class representing the sidebar UI element where the player can purchase items and manage their inventory.

    Attributes:
        shop: The shop containing shelves of items for sale.
        infobox: A UI element for displaying information about game elements when the player hovers over them.
    """

    border_width = 2
    border_color = "black"

    def __init__(self, position: Vector2):
        self.position = position
        self.shop = Shop()

    def draw_border(self, surface: pg.Surface):
        """Draw a border around the sidebar for visual separation from the main game area."""
        border_rect = (*self.position, constants.SIDEBAR_WIDTH, constants.SCREEN_SIZE[1])
        pg.draw.rect(surface, pg.Color(self.border_color), border_rect, self.border_width)

    def draw(self, surface: pg.Surface):
        self.draw_border(surface)
        position = self.position + Vector2(10, 10)  # Padding from the border
        self.shop.draw(surface, position)
