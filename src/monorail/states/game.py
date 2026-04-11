from typing import Any

import pygame as pg

from monorail import constants
from monorail.entities.cursor import Cursor
from monorail.entities.monorail import Monorail
from monorail.entities.nodes import NodeGraph
from monorail.states import main_menu
from monorail.utils.state_manager import State


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
        self.cursor.update()

    def draw(self, surface: pg.Surface, keys, current_time: float, dt: float):
        surface.fill(pg.Color("gray"))
        for i in range(0, surface.get_width(), constants.TILE_SIZE):
            pg.draw.line(surface, pg.Color("darkgray"), (i, 0), (i, surface.get_height()))
        for j in range(0, surface.get_height(), constants.TILE_SIZE):
            pg.draw.line(surface, pg.Color("darkgray"), (0, j), (surface.get_width(), j))
        self.node_graph.draw(surface)
        self.monorail.draw(surface)
        self.cursor.draw(surface)
