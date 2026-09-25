"""
AI CEO - Coordinate Geometry Brain

Deterministic coordinate calculations.
"""

import math


def clean_number(value):
    value = float(value)

    if value.is_integer():
        return int(value)

    return round(value, 10)


def distance(point1, point2):
    """
    Distance between two 2D points.
    """
    x1, y1 = map(float, point1)
    x2, y2 = map(float, point2)

    return clean_number(
        math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    )


def midpoint(point1, point2):
    """
    Midpoint of two points.
    """
    x1, y1 = map(float, point1)
    x2, y2 = map(float, point2)

    return (
        clean_number((x1 + x2) / 2),
        clean_number((y1 + y2) / 2)
    )


def gradient(point1, point2):
    """
    Gradient = change in y / change in x
    """
    x1, y1 = map(float, point1)
    x2, y2 = map(float, point2)

    if math.isclose(x1, x2):
        return None

    return clean_number((y2 - y1) / (x2 - x1))


def section_point(point1, point2, ratio):
    """
    Internal division.

    ratio = m/n

    Returns the point dividing AB in the given ratio.
    """
    x1, y1 = map(float, point1)
    x2, y2 = map(float, point2)

    m, n = map(float, ratio)

    if m <= 0 or n <= 0:
        raise ValueError("Ratio values must be positive.")

    x = (n * x1 + m * x2) / (m + n)
    y = (n * y1 + m * y2) / (m + n)

    return clean_number(x), clean_number(y)


def polygon_area(points):
    """
    Shoelace formula for a polygon.
    """
    points = [(float(x), float(y)) for x, y in points]

    if len(points) < 3:
        raise ValueError("At least three points are required.")

    total = 0

    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]

        total += x1 * y2 - y1 * x2

    return clean_number(abs(total) / 2)
