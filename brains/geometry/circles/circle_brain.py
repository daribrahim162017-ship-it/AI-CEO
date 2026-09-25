"""
AI CEO - Circle Brain

Deterministic circle calculations.
"""

import math


def clean_number(value):
    value = float(value)

    if value.is_integer():
        return int(value)

    return round(value, 10)


def diameter_from_radius(radius):
    radius = float(radius)

    if radius <= 0:
        raise ValueError("Radius must be positive.")

    return clean_number(2 * radius)


def radius_from_diameter(diameter):
    diameter = float(diameter)

    if diameter <= 0:
        raise ValueError("Diameter must be positive.")

    return clean_number(diameter / 2)


def circumference(radius):
    radius = float(radius)

    if radius <= 0:
        raise ValueError("Radius must be positive.")

    return clean_number(2 * math.pi * radius)


def circle_area(radius):
    radius = float(radius)

    if radius <= 0:
        raise ValueError("Radius must be positive.")

    return clean_number(math.pi * radius ** 2)


def semicircle_area(radius):
    return clean_number(circle_area(radius) / 2)


def semicircle_perimeter(radius):
    """
    Perimeter of a semicircle including its diameter.
    """
    radius = float(radius)

    if radius <= 0:
        raise ValueError("Radius must be positive.")

    return clean_number(math.pi * radius + 2 * radius)


def arc_length(radius, angle_degrees):
    """
    Arc length = angle/360 × 2πr
    """
    radius = float(radius)
    angle_degrees = float(angle_degrees)

    if radius <= 0:
        raise ValueError("Radius must be positive.")

    if angle_degrees < 0 or angle_degrees > 360:
        raise ValueError("Angle must be between 0 and 360 degrees.")

    return clean_number(
        (angle_degrees / 360) * 2 * math.pi * radius
    )


def sector_area(radius, angle_degrees):
    """
    Sector area = angle/360 × πr²
    """
    radius = float(radius)
    angle_degrees = float(angle_degrees)

    if radius <= 0:
        raise ValueError("Radius must be positive.")

    if angle_degrees < 0 or angle_degrees > 360:
        raise ValueError("Angle must be between 0 and 360 degrees.")

    return clean_number(
        (angle_degrees / 360) * math.pi * radius ** 2
    )


def chord_length(radius, central_angle_degrees):
    """
    Chord = 2r sin(theta/2)
    """
    radius = float(radius)
    angle = float(central_angle_degrees)

    if radius <= 0:
        raise ValueError("Radius must be positive.")

    if angle < 0 or angle > 360:
        raise ValueError("Angle must be between 0 and 360 degrees.")

    return clean_number(
        2 * radius * math.sin(math.radians(angle / 2))
    )
