"""Class representing the player's monorail."""

import pygame as pg
from pygame import Color

from monorail import constants
from monorail.entities.tile import TileTypeRail
from monorail.utils.vector import Direction, Vector2


def get_directional_input(keys) -> Direction | None:
    """Get directional input from the keyboard and return it as a Direction."""
    direction_map = {
        pg.K_w: Direction.UP,
        pg.K_s: Direction.DOWN,
        pg.K_a: Direction.LEFT,
        pg.K_d: Direction.RIGHT,
        pg.K_UP: Direction.UP,
        pg.K_DOWN: Direction.DOWN,
        pg.K_LEFT: Direction.LEFT,
        pg.K_RIGHT: Direction.RIGHT,
    }
    for key, direction in direction_map.items():
        if keys[key]:
            return direction
    return None


class Monorail:
    """Class representing the player's monorail.

    The monorail moves along a graph of nodes, with each node representing a point on the track.
    The monorail can only move in the four cardinal directions (up, down, left, right) and can
    only move to neighboring nodes in those directions.

    Attributes:
        name: The name of the monorail.
        node: The current node the monorail is on.
        target: The target node the monorail is moving towards.
        position: The current position of the monorail as a Vector2.
        direction: The current direction the monorail is moving in.
        base_speed: The base speed of the monorail in pixels per second.
        speed_multiplier: A multiplier for the monorail's speed, which can be modified by power-ups or other game mechanics.
        color: The color of the monorail, as an RGB tuple.

    Methods:
        update: Update the monorail's position based on its speed and the time since the last frame.
        draw: Draw the monorail to a given surface.
    """

    def __init__(
        self,
        node: TileTypeRail,
        speed_multiplier: float = 1.0,
        name: str = "Manwell",
    ):
        self.name = name
        self.node: TileTypeRail = node
        self.target: TileTypeRail = node
        self.position: Vector2
        self.set_position()
        self.direction = Direction.STOP
        self.base_speed = 100 * constants.TILE_SIZE / 16
        self.speed_multiplier = speed_multiplier
        self.color = Color("blue")

    @property
    def speed(self) -> float:
        """Calculate the current speed of the monorail based on its base speed and speed multiplier."""
        return self.base_speed * self.speed_multiplier

    def set_position(self) -> None:
        """Set the monorail's position to the center of the current node."""
        self.position = self.node.position_px

    def overshot_target(self) -> bool:
        """Check if the monorail has overshot its target node."""
        to_target = self.target.position_px - self.node.position_px
        to_position = self.position - self.node.position_px
        return to_position.length_squared() >= to_target.length_squared()

    def get_new_target(self, direction: Direction) -> TileTypeRail:
        """Calculate the new target node based on the current direction if available."""
        if direction == Direction.STOP:
            return self.node
        return self.node.get_connected_rail(direction) or self.node

    def update(self, dt: float, keys) -> None:
        """Update the monorail's position based on its speed and the time since the last frame."""
        self.position += self.direction.vector * self.speed * dt
        direction = get_directional_input(keys) or self.direction

        if self.overshot_target():
            self.node = self.target
            self.target = self.get_new_target(direction)
            if self.target != self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)
                if self.target == self.node:
                    self.direction = Direction.STOP
            self.set_position()

    def draw(self, surface: pg.Surface) -> None:
        """Draw the monorail to a given surface."""
        # TODO: Replace with sprite when available.
        half_tile = constants.TILE_SIZE // 2, constants.TILE_SIZE // 2
        pg.draw.circle(surface, self.color, self.position + half_tile, constants.TILE_SIZE / 3)
