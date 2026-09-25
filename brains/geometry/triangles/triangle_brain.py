"""
AI CEO - Triangle Brain

Deterministic triangle calculations.
"""

import math


def clean_number(value):
    value = float(value)

    if value.is_integer():
        return int(value)

    return round(value, 10)


def pythagoras_hypotenuse(a, b):
    """
    c = sqrt(a² + b²)
    """
    a = float(a)
    b = float(b)

    if a <= 0 or b <= 0:
        raise ValueError("Triangle sides must be positive.")

    c = math.sqrt(a * a + b * b)

    return clean_number(c)


def pythagoras_missing_leg(hypotenuse, known_leg):
    """
    a = sqrt(c² - b²)
    """
    c = float(hypotenuse)
    b = float(known_leg)

    if c <= 0 or b <= 0:
        raise ValueError("Lengths must be positive.")

    if b >= c:
        raise ValueError("The hypotenuse must be longer than the known leg.")

    a = math.sqrt(c * c - b * b)

    return clean_number(a)


def triangle_area(base, height):
    """
    Area = 1/2 × base × height
    """
    base = float(base)
    height = float(height)

    if base <= 0 or height <= 0:
        raise ValueError("Base and height must be positive.")

    return clean_number(0.5 * base * height)


def equilateral_triangle_area(side):
    """
    Area = sqrt(3)/4 × side²
    """
    side = float(side)

    if side <= 0:
        raise ValueError("Side must be positive.")

    return clean_number((math.sqrt(3) / 4) * side * side)


def triangle_perimeter(a, b, c):
    """
    Perimeter = a + b + c
    """
    a = float(a)
    b = float(b)
    c = float(c)

    if min(a, b, c) <= 0:
        raise ValueError("Sides must be positive.")

    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("These three lengths cannot form a triangle.")

    return clean_number(a + b + c)


def is_right_triangle(a, b, c):
    """
    Checks whether the three sides form a right triangle.
    """
    sides = sorted([float(a), float(b), float(c)])

    if min(sides) <= 0:
        return False

    return math.isclose(
        sides[0] ** 2 + sides[1] ** 2,
        sides[2] ** 2,
        rel_tol=1e-9,
        abs_tol=1e-9
    )


def similar_length(known_small, known_large, corresponding_large):
    """
    Uses proportional sides.

    known_small / known_large
    =
    unknown / corresponding_large
    """
    known_small = float(known_small)
    known_large = float(known_large)
    corresponding_large = float(corresponding_large)

    if known_small <= 0 or known_large <= 0 or corresponding_large <= 0:
        raise ValueError("Lengths must be positive.")

    scale = corresponding_large / known_large
    result = known_small * scale

    return clean_number(result)
