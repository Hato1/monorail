import math
from enum import Enum
from typing import NamedTuple, Self

THRESHOLD = 1e-6  # Threshold for floating-point comparison in equality check.


class Vector2(NamedTuple):
    """A 2D vector class for basic vector operations.

    Methods:
    - __add__: Adds two Vector2 objects or a Vector2 object and a tuple.
    - __sub__: Subtracts two Vector2 objects or a Vector2 object and a tuple.
    - __mul__: Multiplies the Vector2 object by a scalar.
    - __truediv__: Divides the Vector2 object by a scalar.
    - __floordiv__: Performs floor division of the Vector2 object by a scalar.
    - __neg__: Negates the Vector2 object.
    - __eq__: Checks if two Vector2 objects are approximately equal, accounting for floating-point precision issues.
    - length_squared: Returns the square of the length of the vector.
    - length: Returns the length of the vector.
    - normalize: Returns a new Vector2 object that is the normalized version of the original vector.

    Attributes:
    - x: The x-coordinate of the vector.
    - y: The y-coordinate of the vector.

    Examples:
        Vector2(1, 2) + Vector2(3, 4)
        > Vector2(4, 6)
        Vector2(1, 2) * 5
        > Vector2(5, 10)
        Vector2(3, 4) == (3.0000001, 4.0000001)
        > True

    TODO: Implement copy or type conversion methods if needed in the future.
    """

    x: int
    y: int

    def check_compatibility(self, other: object):
        if isinstance(other, tuple):
            if len(other) != len(self):
                raise ValueError(f"Tuple must have exactly {len(self)} elements to be compatible with Vector2.")
            if not all(isinstance(coord, int) for coord in other):
                raise TypeError("All elements of the tuple must be int to be compatible with Vector2.")
        else:
            raise TypeError(f"Unsupported type for operation with Vector2: {type(other)}")

    def __add__(self, other: Self | tuple) -> Self:
        self.check_compatibility(other)
        return self.__class__(self.x + other[0], self.y + other[1])

    def __sub__(self, other: Self | tuple) -> Self:
        self.check_compatibility(other)
        return self.__class__(self.x - other[0], self.y - other[1])

    def __mul__(self, scalar: int) -> Self:  # type: ignore[override]
        return self.__class__(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Self:
        raise NotImplementedError("Cannot divide Vector2[int, int]. Use FloatVector2 instead.")

    def __floordiv__(self, scalar: int) -> Self:
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")
        return self.__class__(self.x // scalar, self.y // scalar)

    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self) | tuple):
            return False
        if len(other) != len(self):
            return False
        return abs(self.x - other[0]) < THRESHOLD and abs(self.y - other[1]) < THRESHOLD

    def length_squared(self) -> float:
        """Returns the square of the length of the vector.

        This is more efficient than calculating the actual length when you only need to compare lengths.

        Returns:
            float: The square of the length of the vector.
        """
        return self.x**2 + self.y**2

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"


class FloatVector2(NamedTuple):
    """A 2D vector class for basic vector operations.

    Methods:
    - __add__: Adds two Vector2 objects or a Vector2 object and a tuple.
    - __sub__: Subtracts two Vector2 objects or a Vector2 object and a tuple.
    - __mul__: Multiplies the Vector2 object by a scalar.
    - __truediv__: Divides the Vector2 object by a scalar.
    - __floordiv__: Performs floor division of the Vector2 object by a scalar.
    - __neg__: Negates the Vector2 object.
    - __eq__: Checks if two Vector2 objects are approximately equal, accounting for floating-point precision issues.
    - length_squared: Returns the square of the length of the vector.
    - length: Returns the length of the vector.
    - normalize: Returns a new Vector2 object that is the normalized version of the original vector.

    Attributes:
    - x: The x-coordinate of the vector.
    - y: The y-coordinate of the vector.

    Examples:
        Vector2(1, 2) + Vector2(3, 4)
        > Vector2(4, 6)
        Vector2(1, 2) * 5
        > Vector2(5, 10)
        Vector2(3, 4) == (3.0000001, 4.0000001)
        > True

    TODO: Implement copy or type conversion methods if needed in the future.
    """

    x: float
    y: float

    def check_compatibility(self, other: object):
        if isinstance(other, tuple):
            if len(other) != len(self):
                raise ValueError(f"Tuple must have exactly {len(self)} elements to be compatible with Vector2.")
            if not all(isinstance(coord, (int, float)) for coord in other):
                raise TypeError("All elements of the tuple must be int or float to be compatible with Vector2.")
        else:
            raise TypeError(f"Unsupported type for operation with Vector2: {type(other)}")

    def __add__(self, other: Self | tuple) -> Self:
        self.check_compatibility(other)
        return self.__class__(self.x + other[0], self.y + other[1])

    def __sub__(self, other: Self | tuple) -> Self:
        self.check_compatibility(other)
        return self.__class__(self.x - other[0], self.y - other[1])

    def __mul__(self, scalar: float) -> Self:  # type: ignore[override]
        return self.__class__(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Self:
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")
        return self.__class__(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar: float) -> Self:
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")
        return self.__class__(self.x // scalar, self.y // scalar)

    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self) | tuple):
            return False
        if len(other) != len(self):
            return False
        return abs(self.x - other[0]) < THRESHOLD and abs(self.y - other[1]) < THRESHOLD

    def length_squared(self) -> float:
        """Returns the square of the length of the vector.

        This is more efficient than calculating the actual length when you only need to compare lengths.

        Returns:
            float: The square of the length of the vector.
        """
        return self.x**2 + self.y**2

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def normalize(self) -> Self:
        length = self.length()
        if length == 0:
            return type(self)(0, 0)
        return self / length

    def as_int(self) -> tuple:
        """Return the vector as a tuple of integers, rounding the components to the nearest integer."""
        return int(self.x), int(self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"


class Direction(Vector2, Enum):
    """Enum representing the four cardinal directions."""

    STOP = 0, 0
    UP = 0, -1
    DOWN = 0, 1
    LEFT = -1, 0
    RIGHT = 1, 0

    @property
    def vector(self) -> Vector2:
        """Return the vector representation of the direction."""
        return self.value
