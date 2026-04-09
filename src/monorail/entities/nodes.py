from enum import Enum

import pygame as pg

from monorail import constants
from monorail.utils.vector import Vector2


class Direction(Vector2, Enum):
    """Enum representing the four cardinal directions."""

    UP = 0, -1
    DOWN = 0, 1
    LEFT = -1, 0
    RIGHT = 1, 0


class Node:
    """Class representing a node in the pathfinding graph.

    Attributes:
        position: The position of the node as a Vector2.
        neighbors: A dictionary mapping directions to neighboring nodes that can be reached from this node.
    """

    def __init__(self, position: Vector2):
        self.position: Vector2 = position
        self.neighbors: dict[Direction, Node | None] = {
            Direction.UP: None,
            Direction.DOWN: None,
            Direction.LEFT: None,
            Direction.RIGHT: None,
        }

    def add_neighbor(self, direction: Direction, neighbor: Node):
        """Add a neighbor in the given direction."""
        self.neighbors[direction] = neighbor
        neighbor.neighbors[-direction] = self

    def draw_node(self, surface: pg.Surface):
        """Draw the node as a small circle on the given surface for debug purposes."""
        pg.draw.circle(surface, constants.NODE_COLOR, self.position, constants.TILE_SIZE // 2)

    def draw_edges(self, surface: pg.Surface):
        """Draw edges from this node to its neighbors for debug purposes."""
        for neighbor in self.neighbors.values():
            if neighbor:
                pg.draw.line(surface, constants.EDGE_COLOR, self.position, neighbor.position, constants.TILE_SIZE // 8)


class NodeGraph:
    """Class representing the entire graph of nodes.

    Attributes:
        nodes: A list of all nodes in the graph.
    """

    def __init__(self):
        self.nodes: list[Node] = []

    def draw(self, surface: pg.Surface):
        """Render all nodes and edges in the graph."""
        if constants.DEBUG:
            for node in self.nodes:
                node.draw_edges(surface)
            for node in self.nodes:
                node.draw_node(surface)

    def setup_test_nodes(self):
        node_a = Node(Vector2(80, 80))
        node_b = Node(Vector2(160, 80))
        node_c = Node(Vector2(80, 160))
        node_d = Node(Vector2(160, 160))
        node_e = Node(Vector2(208, 160))
        node_f = Node(Vector2(80, 320))
        node_g = Node(Vector2(208, 320))
        node_a.add_neighbor(Direction.RIGHT, node_b)
        node_a.add_neighbor(Direction.DOWN, node_c)
        node_b.add_neighbor(Direction.LEFT, node_a)
        node_b.add_neighbor(Direction.DOWN, node_d)
        node_c.add_neighbor(Direction.UP, node_a)
        node_c.add_neighbor(Direction.RIGHT, node_d)
        node_c.add_neighbor(Direction.DOWN, node_f)
        node_d.add_neighbor(Direction.UP, node_b)
        node_d.add_neighbor(Direction.LEFT, node_c)
        node_d.add_neighbor(Direction.RIGHT, node_e)
        node_e.add_neighbor(Direction.LEFT, node_d)
        node_e.add_neighbor(Direction.DOWN, node_g)
        node_f.add_neighbor(Direction.UP, node_c)
        node_f.add_neighbor(Direction.RIGHT, node_g)
        node_g.add_neighbor(Direction.UP, node_e)
        node_g.add_neighbor(Direction.LEFT, node_f)
        self.nodes = [node_a, node_b, node_c, node_d, node_e, node_f, node_g]
