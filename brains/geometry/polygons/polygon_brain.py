"""
AI CEO - Polygon Brain

Deterministic polygon calculations.
"""

import math


def clean_number(value):
    value = float(value)

    if value.is_integer():
        return int(value)

    return round(value, 10)


def interior_angle_sum(sides):
    n = int(sides)

    if n < 3:
        raise ValueError("A polygon must have at least 3 sides.")

    return clean_number((n - 2) * 180)


def regular_interior_angle(sides):
    n = int(sides)

    if n < 3:
        raise ValueError("A polygon must have at least 3 sides.")

    return clean_number((n - 2) * 180 / n)


def regular_exterior_angle(sides):
    n = int(sides)

    if n < 3:
        raise ValueError("A polygon must have at least 3 sides.")

    return clean_number(360 / n)


def sides_from_exterior_angle(angle):
    angle = float(angle)

    if angle <= 0:
        raise ValueError("Exterior angle must be positive.")

    sides = 360 / angle

    if not math.isclose(sides, round(sides), rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError("The angle does not produce a regular polygon with a whole number of sides.")

    return int(round(sides))


def regular_polygon_perimeter(sides, side_length):
    n = int(sides)
    side_length = float(side_length)

    if n < 3:
        raise ValueError("A polygon must have at least 3 sides.")

    if side_length <= 0:
        raise ValueError("Side length must be positive.")

    return clean_number(n * side_length)


def regular_polygon_area(sides, side_length):
    """
    Area = n*s² / (4*tan(pi/n))
    """
    n = int(sides)
    side_length = float(side_length)

    if n < 3:
        raise ValueError("A polygon must have at least 3 sides.")

    if side_length <= 0:
        raise ValueError("Side length must be positive.")

    area = (
        n * side_length ** 2
        / (4 * math.tan(math.pi / n))
    )

    return clean_number(area)
