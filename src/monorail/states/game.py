from typing import Any

import pygame as pg

from monorail import constants
from monorail.entities import tile
from monorail.entities.cursor import Cursor
from monorail.entities.monorail import Monorail
from monorail.entities.nodes import NodeGraph
from monorail.entities.tile import TileGrid
from monorail.states import main_menu
from monorail.utils.state_manager import State
from monorail.utils.vector import Vector2


class Game(State):
    def __init__(self) -> None:
        super().__init__()
        self.monorail: Monorail
        self.cursor: Cursor = Cursor()

    def startup(self, current_time: float, persistant: dict[str, Any], previous: type[State], surface_rect: pg.Rect):
        super().startup(current_time, persistant, previous, surface_rect)
        self.node_graph = NodeGraph()
        self.node_graph.setup_test_nodes()
        self.monorail = Monorail(node=self.node_graph.nodes[0])
        self.tile_grid = TileGrid(constants.GRID_WIDTH, constants.GRID_HEIGHT)

        self.tile_grid.set_tile(0, 0, tile.TileTypeBank())
        self.tile_grid.set_tile(10, 5, tile.TileTypeRadio())

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
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.cursor.handle_mouse_click(Vector2(*event.pos), self.tile_grid)

    def update(self, surface_rect, keys, current_time, dt):
        self.monorail.update(dt, keys)
        self.cursor.update()

    def draw(self, surface: pg.Surface, keys, current_time: float, dt: float):
        surface.fill(pg.Color("gray"))
        self.tile_grid.draw(surface)
        self.node_graph.draw(surface)
        self.monorail.draw(surface)
        self.cursor.draw(surface)
