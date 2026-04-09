import math
from typing import NamedTuple, Self

THRESHOLD = 1e-6  # Threshold for floating-point comparison in equality check.


class Vector2(NamedTuple):
    """A 2D vector class for basic vector operations.

    Methods:
    - __add__: Adds two Vector2 objects or a Vector2 object and a tuple.
    - __sub__: Subtracts two Vector2 objects or a Vector2 object and a tuple.
    - __mul__: Multiplies the Vector2 object by a scalar.
    - __truediv__: Divides the Vector2 object by a scalar.
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

    TODO: Implement copy or type conversion methods if needed in the future.
    """

    x: float
    y: float

    def __add__(self, other: Self | tuple) -> Self:
        if not isinstance(other, type(self)):
            raise NotImplementedError(f"Addition not supported between instances of 'Vector2' and '{type(other)}'")
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self | tuple) -> Self:
        if not isinstance(other, type(self)):
            raise NotImplementedError(f"Subtraction not supported between instances of 'Vector2' and '{type(other)}'")
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Self:  # type: ignore[override]
        return self.__class__(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Self:
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")
        return self.__class__(self.x / scalar, self.y / scalar)

    def __neg__(self):
        return self.__class__(-self.x, -self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError(f"Cannot compare Vector2 with non-Vector2 type: '{type(other)}'")
        return abs(self.x - other.x) < THRESHOLD and abs(self.y - other.y) < THRESHOLD

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

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
