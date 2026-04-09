import math
from typing import Self


class Vector2:
    """A simple 2D vector class for basic vector operations.

    TODO: Implement copy or type conversion methods if needed in the future.
    """

    THRESHOLD = 1e-6  # Threshold for floating-point comparison in equality check.

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return type(self)(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    def __mul__(self, scalar: float) -> Self:
        return type(self)(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Self:
        assert scalar != 0, "Cannot divide by zero."
        return type(self)(self.x / scalar, self.y / scalar)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError(f"Cannot compare Vector2 with non-Vector2 type: '{type(other)}'")
        return abs(self.x - other.x) < self.THRESHOLD and abs(self.y - other.y) < self.THRESHOLD

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

    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
