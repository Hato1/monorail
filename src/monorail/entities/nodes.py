import pygame as pg

from monorail import constants
from monorail.utils.asset_manager import Image
from monorail.utils.vector import Direction, Vector2

# Convertions from sets of valid directions to the appropriate image and rotation for a node.
# The angles may seem reversed from what you would expect because Pygame rotations are counterclockwise.
IMAGE_LOOKUP: dict[frozenset[Direction], Image] = {
    # Straight
    frozenset({Direction.UP, Direction.DOWN}): Image.RAIL_NS,
    frozenset({Direction.LEFT, Direction.RIGHT}): Image.RAIL_EW,
    # Corner
    frozenset({Direction.UP, Direction.RIGHT}): Image.RAIL_NE,
    frozenset({Direction.RIGHT, Direction.DOWN}): Image.RAIL_SE,
    frozenset({Direction.DOWN, Direction.LEFT}): Image.RAIL_SW,
    frozenset({Direction.LEFT, Direction.UP}): Image.RAIL_NW,
    # 3-way
    frozenset({Direction.UP, Direction.RIGHT, Direction.DOWN}): Image.RAIL_NES,
    frozenset({Direction.RIGHT, Direction.DOWN, Direction.LEFT}): Image.RAIL_NSW,
    frozenset({Direction.DOWN, Direction.LEFT, Direction.UP}): Image.RAIL_NEW,
    frozenset({Direction.LEFT, Direction.UP, Direction.RIGHT}): Image.RAIL_ESW,
    # 4-way
    frozenset({Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN}): Image.RAIL_NESW,
}


def get_image(valid_directions: set[Direction]) -> pg.Surface:
    """Get the appropriate image for a node based on its valid directions.

    nb. Pygame rotations are counterclockwise, so the angles may seem reversed from what you would expect.
    """
    try:
        image = IMAGE_LOOKUP[frozenset(valid_directions)]
    except KeyError as err:
        raise ValueError(f"Invalid combination of valid directions: {valid_directions}") from err

    return image.load()


class RoadNode:
    """Class representing a node in the monorail track graph.

    Each node represents a point on the track where cars can be, and edges between nodes represent possible paths for cars to take.

    Attributes:
        position: The position of the node as a Vector2.
        neighbors: A dictionary mapping directions to neighboring nodes that can be reached from this node.
    """

    def __init__(self, position: Vector2, valid_directions: set[Direction]):
        self.position: Vector2 = position
        self.neighbors: dict[Direction, RoadNode | None] = {direction: None for direction in valid_directions}
        self.image = get_image(valid_directions)

    def add_neighbor(self, direction: Direction, neighbor: RoadNode):
        """Add a neighbor in the given direction."""
        assert direction in self.neighbors, (
            f"Invalid direction {direction}. Must be one of {list(self.neighbors.keys())}."
        )
        self.neighbors[direction] = neighbor
        neighbor.neighbors[-direction] = self

    def remove_neighbor(self, direction: Direction):
        """Remove the neighbor in the given direction."""
        neighbor = self.neighbors[direction]
        if neighbor:
            self.neighbors[direction] = None
            neighbor.neighbors[-direction] = None
        else:
            print(f"Warning: No neighbor to remove in direction {direction} from node at {self.position}")

    def remove_all_neighbors(self):
        """Remove all neighbors from this node.

        Useful for when a node is being deleted and we want to clean up all references to it from its neighbors.
        """
        for direction in self.neighbors:
            self.remove_neighbor(direction)

    def draw_node(self, surface: pg.Surface):
        """Draw the node as a small circle on the given surface for debug purposes."""
        surface.blit(self.image, self.position)
        pg.draw.circle(surface, constants.NODE_COLOR, self.position, constants.TILE_SIZE // 3)

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
        self.nodes: list[RoadNode] = []

    def draw(self, surface: pg.Surface):
        """Render all nodes and edges in the graph."""
        if constants.DEBUG:
            for node in self.nodes:
                node.draw_edges(surface)
            for node in self.nodes:
                node.draw_node(surface)

    def setup_test_nodes(self):
        node_i = RoadNode(Vector2(11, 3) * constants.TILE_SIZE, {Direction.LEFT, Direction.UP})  # Bottom Right
        node_j = RoadNode(Vector2(10, 3) * constants.TILE_SIZE, {Direction.LEFT, Direction.RIGHT})  # Bottom
        node_k = RoadNode(Vector2(9, 3) * constants.TILE_SIZE, {Direction.UP, Direction.RIGHT})  # Bottom Left
        node_l = RoadNode(Vector2(9, 2) * constants.TILE_SIZE, {Direction.UP, Direction.DOWN})  # Left
        node_m = RoadNode(Vector2(9, 1) * constants.TILE_SIZE, {Direction.RIGHT, Direction.DOWN})  # Top Left
        node_n = RoadNode(Vector2(10, 1) * constants.TILE_SIZE, {Direction.RIGHT, Direction.LEFT})  # Top
        node_o = RoadNode(Vector2(11, 1) * constants.TILE_SIZE, {Direction.DOWN, Direction.LEFT})  # Top Right
        node_p = RoadNode(Vector2(11, 2) * constants.TILE_SIZE, {Direction.UP, Direction.DOWN})  # Right

        node_a = RoadNode(Vector2(2, 2) * constants.TILE_SIZE, {Direction.RIGHT, Direction.DOWN})
        node_b = RoadNode(Vector2(3, 2) * constants.TILE_SIZE, {Direction.LEFT, Direction.DOWN})
        node_c = RoadNode(Vector2(2, 3) * constants.TILE_SIZE, {Direction.UP, Direction.RIGHT, Direction.DOWN})
        node_d = RoadNode(Vector2(3, 3) * constants.TILE_SIZE, {Direction.UP, Direction.LEFT, Direction.RIGHT})
        node_e = RoadNode(Vector2(5, 3) * constants.TILE_SIZE, {Direction.LEFT, Direction.DOWN})
        node_f = RoadNode(Vector2(2, 8) * constants.TILE_SIZE, {Direction.UP, Direction.RIGHT})
        node_g = RoadNode(Vector2(5, 8) * constants.TILE_SIZE, {Direction.UP, Direction.LEFT})

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
        self.nodes = [
            node_a,
            node_b,
            node_c,
            node_d,
            node_e,
            node_f,
            node_g,
            node_i,
            node_j,
            node_k,
            node_l,
            node_m,
            node_n,
            node_o,
            node_p,
        ]
