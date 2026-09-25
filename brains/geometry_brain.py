import math


# -----------------------------
# ANGLES
# -----------------------------

def triangle_missing_angle(a, b):
    return 180 - a - b


def straight_line_missing_angle(a):
    return 180 - a


def angles_around_point_missing(known_angles):
    return 360 - sum(known_angles)


def quadrilateral_missing_angle(known_angles):
    return 360 - sum(known_angles)


def polygon_interior_sum(n):
    if n < 3:
        raise ValueError("A polygon needs at least 3 sides.")
    return (n - 2) * 180


def regular_polygon_angle(n):
    return polygon_interior_sum(n) / n


def exterior_angle_regular_polygon(n):
    if n < 3:
        raise ValueError("A polygon needs at least 3 sides.")
    return 360 / n


def vertically_opposite_angle(angle):
    return angle


def corresponding_angle(angle):
    return angle


def alternate_angle(angle):
    return angle


def cointerior_missing_angle(angle):
    return 180 - angle


# -----------------------------
# TRIANGLES
# -----------------------------

def pythagoras_hypotenuse(a, b):
    return math.sqrt(a * a + b * b)


def pythagoras_missing_side(hypotenuse, side):
    value = hypotenuse * hypotenuse - side * side

    if value < 0:
        raise ValueError("The measurements are impossible.")

    return math.sqrt(value)


def triangle_area(base, height):
    return 0.5 * base * height


# -----------------------------
# CIRCLES
# -----------------------------

def circle_area(radius):
    return math.pi * radius * radius


def circle_circumference(radius):
    return 2 * math.pi * radius


def semicircle_area(radius):
    return 0.5 * math.pi * radius * radius


def semicircle_arc(radius):
    return math.pi * radius


def semicircle_perimeter(radius):
    return math.pi * radius + 2 * radius


# -----------------------------
# RECTANGLES / SQUARES
# -----------------------------

def rectangle_area(length, width):
    return length * width


def rectangle_perimeter(length, width):
    return 2 * (length + width)


def square_area(side):
    return side * side


def square_perimeter(side):
    return 4 * side


# -----------------------------
# GENERAL
# -----------------------------

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def midpoint(x1, y1, x2, y2):
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def round_sf(value, figures=3):
    if value == 0:
        return 0

    places = figures - 1 - math.floor(math.log10(abs(value)))
    return round(value, places)
