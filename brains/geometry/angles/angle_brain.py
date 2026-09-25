"""
AI CEO - Angle Brain

Deterministic angle calculations.
"""

import math


def clean_number(value):
    value = float(value)
    if value.is_integer():
        return int(value)
    return round(value, 10)


def triangle_missing_angle(angle1, angle2):
    """
    Angles in a triangle add to 180 degrees.
    """
    result = 180 - float(angle1) - float(angle2)

    if result <= 0:
        raise ValueError("Triangle angles must leave a positive third angle.")

    return clean_number(result)


def straight_line_missing_angle(angle):
    """
    Angles on a straight line add to 180 degrees.
    """
    result = 180 - float(angle)

    if result < 0:
        raise ValueError("Angle cannot be greater than 180 degrees.")

    return clean_number(result)


def angles_around_point_missing(*angles):
    """
    Angles around a point add to 360 degrees.
    """
    result = 360 - sum(float(a) for a in angles)

    if result < 0:
        raise ValueError("Given angles exceed 360 degrees.")

    return clean_number(result)


def vertically_opposite_angle(angle):
    """
    Vertically opposite angles are equal.
    """
    return clean_number(angle)


def corresponding_angle(angle):
    """
    Corresponding angles between parallel lines are equal.
    """
    return clean_number(angle)


def alternate_angle(angle):
    """
    Alternate angles between parallel lines are equal.
    """
    return clean_number(angle)


def cointerior_missing_angle(angle):
    """
    Co-interior angles between parallel lines add to 180 degrees.
    """
    result = 180 - float(angle)

    if result < 0:
        raise ValueError("Invalid angle.")

    return clean_number(result)


def polygon_interior_sum(sides):
    """
    Sum of interior angles of an n-sided polygon.
    """
    n = int(sides)

    if n < 3:
        raise ValueError("A polygon must have at least 3 sides.")

    return clean_number((n - 2) * 180)


def regular_polygon_interior_angle(sides):
    """
    Each interior angle of a regular polygon.
    """
    n = int(sides)

    if n < 3:
        raise ValueError("A polygon must have at least 3 sides.")

    return clean_number(((n - 2) * 180) / n)


def regular_polygon_exterior_angle(sides):
    """
    Each exterior angle of a regular polygon.
    """
    n = int(sides)

    if n < 3:
        raise ValueError("A polygon must have at least 3 sides.")

    return clean_number(360 / n)


def degrees_to_radians(angle):
    return math.radians(float(angle))


def radians_to_degrees(angle):
    return math.degrees(float(angle))
