"""Class representing the player's monorail."""

import pygame as pg
from pygame import Color

from monorail import constants
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
