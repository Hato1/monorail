"""Constants used throughout the game, such as screen size and tile size."""

DEBUG = True

SCREEN_SIZE = (672, 384)  # 16:9 aspect ratio, fits 21x12 tiles at 32x32 pixels each.
TILE_SIZE = 32  # Size of each tile in pixels.
GRID_HEIGHT = SCREEN_SIZE[1] // TILE_SIZE  # Number of rows of tiles on the screen.
GRID_WIDTH = SCREEN_SIZE[0] // TILE_SIZE  # Number of columns of tiles on the screen.

SIDEBAR_WIDTH = TILE_SIZE * 5  # Width of the sidebar on the right side of the screen.
BOTTOM_BAR_HEIGHT = TILE_SIZE * 1  # Height of the bottom bar for UI elements.

GRID_WIDTH -= SIDEBAR_WIDTH // TILE_SIZE  # Leave space on the right side of the screen for UI elements.
GRID_HEIGHT -= BOTTOM_BAR_HEIGHT // TILE_SIZE  # Leave space at the bottom of the screen for UI elements.

DEFAULT_CAPTION = "Monorail"  # Window title.

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

NODE_COLOR = YELLOW
EDGE_COLOR = WHITE
