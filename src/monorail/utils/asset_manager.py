"""Provides a centralized way to retrieve assets.

Assets are loaded using the importlib.resources module to ensure compatibility
with various packaging methods.

Each asset type (images, sounds, fonts, levels, UI elements) is represented by an Enum.
Each Enum member has a method to load the asset.
Enums were chosen to avoid hardcoding strings throughout the codebase.

Usage:
    from monorail.utils.asset_manager import Images
    image = Images.ZOMBIE.load()  # Returns pygame surface.
"""

from enum import Enum, unique
from functools import cache
from importlib.resources import as_file, files
from pathlib import Path

import pygame as pg

MODULE_PATH = files("monorail")
ASSETS_PATH = MODULE_PATH / "assets"
IMAGES_PATH = ASSETS_PATH / "images"
SOUNDS_PATH = ASSETS_PATH / "sounds"
FONTS_PATH = ASSETS_PATH / "fonts"
LEVELS_PATH = ASSETS_PATH / "levels"
UI_PATH = ASSETS_PATH / "ui"


@unique
class Image(Enum):
    RAIL_NS = "tiles/rail/ns.png"
    RAIL_EW = "tiles/rail/ew.png"

    RAIL_NE = "tiles/rail/ne.png"
    RAIL_SE = "tiles/rail/se.png"
    RAIL_SW = "tiles/rail/sw.png"
    RAIL_NW = "tiles/rail/nw.png"

    RAIL_NES = "tiles/rail/nes.png"
    RAIL_NSW = "tiles/rail/nsw.png"
    RAIL_NEW = "tiles/rail/new.png"
    RAIL_ESW = "tiles/rail/esw.png"

    RAIL_NESW = "tiles/rail/nesw.png"

    BANK = "tiles/bank.png"
    RADIO = "tiles/radio.png"

    @cache
    def load(self) -> pg.Surface:
        with as_file(IMAGES_PATH / self.value) as path:
            assert path.is_file(), f"Image file not found: {path}"
            return pg.image.load(path).convert_alpha()


@unique
class Sound(Enum):
    # Web builds with PygBag only support OGG sounds.
    EXPLOSION = "explosion.wav"
    SHOOT = "shoot.wav"
    BACKGROUND_MUSIC = "background.mp3"

    @cache
    def load(self) -> pg.Sound:
        # TODO: Music should probably be its own Enum that loads with pg.mixer.music.
        with as_file(SOUNDS_PATH / self.value) as path:
            assert path.is_file(), f"Sound file not found: {path}"
            return pg.Sound(path)


@unique
class Font(Enum):
    m_tiny = "m3x6.ttf"
    m_small = "m5x7.ttf"
    m_large = "m6x11.ttf"

    @cache
    def load(self, size: int = 16) -> pg.Font:
        with as_file(FONTS_PATH / self.value) as path:
            assert path.is_file(), f"Font file not found: {path}"
            return pg.font.Font(path, size)


@unique
class Level(Enum):
    LEVEL_1 = "level_1.json"
    LEVEL_2 = "level_2.json"

    @cache
    def load(self) -> Path:
        with as_file(LEVELS_PATH / self.value) as path:
            assert path.is_file(), f"Level file not found: {path}"
            return path


@unique
class UIElement(Enum):
    HEART_FULL = "healthbar/heart_full.png"
    HEART_EMPTY = "healthbar/heart_empty.png"
    NUMBER_0 = "numbers/0.png"
    NUMBER_1 = "numbers/1.png"
    NUMBER_2 = "numbers/2.png"
    NUMBER_3 = "numbers/3.png"
    NUMBER_4 = "numbers/4.png"
    NUMBER_5 = "numbers/5.png"
    NUMBER_6 = "numbers/6.png"
    NUMBER_7 = "numbers/7.png"
    NUMBER_8 = "numbers/8.png"
    NUMBER_9 = "numbers/9.png"

    @cache
    def load(self) -> pg.Surface:
        with as_file(UI_PATH / self.value) as path:
            assert path.is_file(), f"Image file not found: {path}"
            return pg.image.load(path).convert_alpha()
