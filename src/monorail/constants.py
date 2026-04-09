"""Constants used throughout the game, such as screen size and tile size."""

SCREEN_SIZE = (672, 384)  # 16:9 aspect ratio, fits 21x12 tiles at 32x32 pixels each.
TILE_SIZE = 32  # Size of each tile in pixels.
NROWS = SCREEN_SIZE[1] // TILE_SIZE  # Number of rows of tiles on the screen.
NCOLS = SCREEN_SIZE[0] // TILE_SIZE  # Number of columns of tiles on the screen.

DEFAULT_CAPTION = "Monorail"  # Window title.

# Colors
BLACK = (0, 0, 0)
