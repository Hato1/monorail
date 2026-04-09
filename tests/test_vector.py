"""Tests for Vector2 class."""

import pytest

from monorail.utils.vector import Vector2


def test_vector_add():
    v1 = Vector2(1, 2)
    v2 = Vector2(3, 4)
    result = v1 + v2
    assert result.x == 4
    assert result.y == 6


def test_vector_sub():
    v1 = Vector2(5, 6)
    v2 = Vector2(2, 3)
    result = v1 - v2
    assert result.x == 3
    assert result.y == 3


def test_vector_neg():
    v1 = Vector2(1, -2)
    result = -v1
    assert result.x == -1
    assert result.y == 2


def test_vector_mul():
    v1 = Vector2(2, 3)
    scalar = 2
    result = v1 * scalar
    assert result.x == 4
    assert result.y == 6


def test_vector_div():
    v1 = Vector2(4, 6)
    scalar = 2
    result = v1 / scalar
    assert result.x == 2
    assert result.y == 3


def test_vector_division_by_zero():
    v1 = Vector2(1, 2)
    with pytest.raises(AssertionError):
        _ = v1 / 0


def test_vector_len():
    v1 = Vector2(3, 4)
    assert v1.length() == 5


def test_vector_normalize():
    v1 = Vector2(3, 4)
    normalized = v1.normalize()
    assert normalized.x == 0.6
    assert normalized.y == 0.8


def test_vector_equality():
    v1 = Vector2(1, 2)
    v2 = Vector2(1, 2)
    v3 = Vector2(1.000000001, 2.000000001)
    assert v1 == v2
    assert v1 == v3


def test_vector_inequality():
    v1 = Vector2(1, 2)
    v2 = Vector2(1, 3)
    assert v1 != v2


def test_vector_zero_length_normalize():
    v1 = Vector2(0, 0)
    normalized = v1.normalize()
    assert normalized.x == 0
    assert normalized.y == 0


def test_vector_str():
    v1 = Vector2(1, 2)
    assert str(v1) == "Vector2(1, 2)"
