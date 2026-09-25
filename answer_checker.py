import math


def numbers_close(a, b, tolerance=1e-9):
    return math.isclose(
        float(a),
        float(b),
        rel_tol=tolerance,
        abs_tol=tolerance
    )


def verify_positive(value):
    return value >= 0


def verify_angle(value):
    return 0 <= value <= 360


def verify_triangle_angles(a, b, c):
    return numbers_close(a + b + c, 180)


def verify_quadrilateral_angles(angles):
    return numbers_close(sum(angles), 360)


def verify_pythagoras(a, b, c):
    return numbers_close(
        a*a + b*b,
        c*c
    )


def verify_circle_area(area, radius):
    expected = math.pi * radius * radius
    return numbers_close(area, expected)


def verify_circle_circumference(circumference, radius):
    expected = 2 * math.pi * radius
    return numbers_close(circumference, expected)
