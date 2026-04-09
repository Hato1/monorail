"""Class representing the player's monorail."""

from enum import Enum

import pygame as pg
from pygame import Color

from monorail import constants
from monorail.utils.vector import Vector2


class Direction(Enum):
    """Enum representing the four cardinal directions."""

    STOP = Vector2(0, 0)
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)

    @property
    def vector(self) -> Vector2:
        """Return the vector representation of the direction."""
        return self.value


def get_directional_input(keys) -> Direction | None:
    """Get directional input from the keyboard and return it as a Direction."""
    if keys[pg.K_w] or keys[pg.K_UP]:
        return Direction.UP
    if keys[pg.K_s] or keys[pg.K_DOWN]:
        return Direction.DOWN
    if keys[pg.K_a] or keys[pg.K_LEFT]:
        return Direction.LEFT
    if keys[pg.K_d] or keys[pg.K_RIGHT]:
        return Direction.RIGHT
    return None


class Monorail:
    """Class representing the player's monorail.

    Attributes:
       x: The x-coordinate of the monorail's position.
       y: The y-coordinate of the monorail's position.
       speed: The speed at which the monorail moves in pixels per second.
       color: The color of the monorail, as an RGB tuple.

    Methods:
       update: Update the monorail's position based on its speed and the time since the last frame.
       draw: Draw the monorail to a given surface.
    """

    def __init__(
        self,
        position: Vector2,
        speed_multiplier: float = 1.0,
        name: str = "Manwell",
    ):
        self.name = name
        self.position = position
        self.direction = Direction.STOP
        self.base_speed = 100 * constants.TILE_SIZE / 16
        self.speed_multiplier = speed_multiplier
        self.color = Color("yellow")

    @property
    def speed(self) -> float:
        """Calculate the current speed of the monorail based on its base speed and speed multiplier."""
        return self.base_speed * self.speed_multiplier

    def update(self, dt: float, keys) -> None:
        """Update the monorail's position based on its speed and the time since the last frame."""
        self.position += self.direction.vector * self.speed * dt
        self.direction = get_directional_input(keys) or self.direction

    def draw(self, surface: pg.Surface) -> None:
        """Draw the monorail to a given surface."""
        # TODO: Replace with sprite when available.
        pg.draw.circle(surface, self.color, self.position, constants.TILE_SIZE / 2)
