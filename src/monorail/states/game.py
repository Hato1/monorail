import random
from typing import Any, Self

import pygame as pg

from monorail import constants
from monorail.entities.monorail import Monorail
from monorail.entities.nodes import NodeGraph
from monorail.states import main_menu
from monorail.utils.asset_manager import Images
from monorail.utils.state_manager import State


def get_random_position_on_rect_perimeter(rect: pg.Rect) -> pg.Vector2:
    """Returns a random position on the perimeter of the given rect."""

    # Decide whether to pick a position on a horizontal or vertical edge.
    # This is weighted by the length of the edges to ensure uniform distribution.
    if random.random() < (rect.width / (rect.width + rect.height)):
        x = random.randrange(rect.left, rect.right)
        y = random.choice([rect.top, rect.bottom])
    else:
        x = random.choice([rect.left, rect.right])
        y = random.randrange(rect.top, rect.bottom)
    return pg.Vector2(x, y)


class Monster:
    """A simple monster class for demonstration purposes.

    Monsters start just outside the screen and move in a straight
    line so that they intersect with their target.

    Monster's never despawn; they just keep going indefinitely.
    That's ok though because they have negligible resource usage.

    """

    SPRITE = (
        Images.MONSTER_FRAME_0.load(),
        Images.MONSTER_FRAME_1.load(),
    )

    def __init__(self, position: pg.Vector2, direction: pg.Vector2, speed: float):
        self.position = position
        self.direction = direction
        self.speed = speed
        self.rect = self.SPRITE[0].get_rect(center=(self.position))

    @classmethod
    def create_monster(cls, screen_rect: pg.Rect, target: pg.Vector2) -> Self:
        """Create a monster with a default position, vector, and speed."""
        half_sprite_dims = cls.SPRITE[0].get_width() / 2, cls.SPRITE[0].get_height() / 2
        # Make sure enemies spawn just outside the screen.
        spawn_area = screen_rect.inflate(half_sprite_dims)
        position = get_random_position_on_rect_perimeter(spawn_area)
        # Aim the monster towards the target position.
        vector = target - position
        speed = random.uniform(0.05, 0.5)
        return cls(position, vector, speed)

    def update(self, dt: float):
        """Update the monster's position based on its speed and direction."""
        self.position += self.direction * self.speed * dt

    def draw(self, surface: pg.Surface, current_time: float):
        # Simple animation based on time and monster speed.
        sprite_index = int((current_time * self.speed * 10) % 2)
        sprite = self.SPRITE[sprite_index]
        self.rect = sprite.get_rect(center=(self.position))
        surface.blit(sprite, self.rect)


class Player:
    """A simple player class for demonstration purposes.

    The directional arrows or WASD keys control the players velocity instead of position.
    This gives the player a smoother, more 'slidey' movement experience.
    """

    SPRITE = Images.MONSTER_FRAME_1.load()
    INITIAL_HEALTH_CAPACITY = 3
    THRUST_SCALAR = 2  # How quickly the player accelerates.
    FRICTION = 0.05  # Percentage of speed lost each second.

    def __init__(self, position: pg.Vector2):
        self.position: pg.Vector2 = position
        self.velocity = pg.Vector2(0, 0)
        self.max_health = self.INITIAL_HEALTH_CAPACITY
        self.health = self.max_health
        self.rect = self.SPRITE.get_rect(center=(self.position))

    def increase_velocity(self, delta: pg.Vector2):
        if not delta:
            return
        delta = pg.Vector2.normalize(delta) * self.THRUST_SCALAR
        self.velocity += delta

    def clamp_position(self, surface_rect: pg.Rect):
        """Keep the player within the bounds of the given rect."""
        half_width = self.rect.width / 2
        half_height = self.rect.height / 2
        self.position.x = pg.math.clamp(
            self.position.x, surface_rect.left + half_width, surface_rect.right - half_width
        )
        self.position.y = pg.math.clamp(
            self.position.y, surface_rect.top + half_height, surface_rect.bottom - half_height
        )

    def update(self, surface_rect: pg.Rect, dt: float):
        self.position += self.velocity * dt
        print(dt)
        # Make friction dt-aware so deceleration is frame-rate independent.
        # Use exponential decay so that FRICTION represents the per-second
        # retention factor when dt is in seconds. For small dt this approximates
        # linear scaling but remains stable for variable frame times.
        self.velocity *= self.FRICTION**dt
        self.clamp_position(surface_rect)
        self.rect = self.SPRITE.get_rect(center=(self.position))

    def draw(self, surface):
        surface.blit(self.SPRITE, self.rect)


class Game(State):
    def __init__(self) -> None:
        super().__init__()
        self.monorail: Monorail

    def startup(self, current_time: float, persistant: dict[str, Any], previous: type[State], surface_rect: pg.Rect):
        super().startup(current_time, persistant, previous, surface_rect)
        self.node_graph = NodeGraph()
        self.node_graph.setup_test_nodes()
        self.monorail = Monorail(node=self.node_graph.nodes[0])

    def get_event(self, event: pg.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.done = True
                # assign the class object from the module alias to avoid
                # circular-import issues that arise from `from ... import ...`
                # and to keep the reference short.
                self.next = main_menu.MainMenu
            if event.key == pg.K_p:
                print(repr(self.node_graph))

    def update(self, surface_rect, keys, current_time, dt):
        self.monorail.update(dt, keys)

    def draw(self, surface: pg.Surface, keys, current_time: float, dt: float):
        surface.fill(pg.Color("gray"))
        for i in range(0, surface.get_width(), constants.TILE_SIZE):
            pg.draw.line(surface, pg.Color("darkgray"), (i, 0), (i, surface.get_height()))
        for j in range(0, surface.get_height(), constants.TILE_SIZE):
            pg.draw.line(surface, pg.Color("darkgray"), (0, j), (surface.get_width(), j))
        self.node_graph.draw(surface)
        self.monorail.draw(surface)
