"""
AI CEO - Geometry Answer Checker

Independently verifies common geometry calculations.
"""

import math


def close(a, b, tolerance=1e-9):
    return math.isclose(
        float(a),
        float(b),
        rel_tol=tolerance,
        abs_tol=tolerance
    )


def check_pythagoras(a, b, c):
    """
    Check:
        a² + b² = c²
    """

    a = float(a)
    b = float(b)
    c = float(c)

    calculated = math.sqrt(a * a + b * b)

    return {
        "correct": close(calculated, c),
        "expected": calculated,
        "given": c,
        "rule": "a² + b² = c²"
    }


def check_triangle_angles(a, b, c):
    """
    Triangle angles must total 180°.
    """

    total = float(a) + float(b) + float(c)

    return {
        "correct": close(total, 180),
        "total": total,
        "expected": 180,
        "rule": "Triangle angles = 180°"
    }


def check_straight_line_angles(a, b):
    """
    Angles on a straight line total 180°.
    """

    total = float(a) + float(b)

    return {
        "correct": close(total, 180),
        "total": total,
        "expected": 180,
        "rule": "Straight line angles = 180°"
    }


def check_angles_around_point(angles):
    """
    Angles around a point total 360°.
    """

    total = sum(float(x) for x in angles)

    return {
        "correct": close(total, 360),
        "total": total,
        "expected": 360,
        "rule": "Angles around a point = 360°"
    }


def check_polygon_interior_sum(sides, answer):
    """
    Check polygon interior angle sum.
    """

    n = int(sides)

    expected = (n - 2) * 180

    return {
        "correct": close(expected, answer),
        "expected": expected,
        "given": float(answer),
        "rule": "(n - 2) × 180°"
    }


def check_regular_polygon_angle(sides, answer):
    """
    Check one interior angle of a regular polygon.
    """

    n = int(sides)

    expected = ((n - 2) * 180) / n

    return {
        "correct": close(expected, answer),
        "expected": expected,
        "given": float(answer),
        "rule": "((n - 2) × 180°) / n"
    }


def check_circle_area(radius, answer):
    """
    Check πr².
    """

    radius = float(radius)

    expected = math.pi * radius ** 2

    return {
        "correct": close(expected, answer),
        "expected": expected,
        "given": float(answer),
        "rule": "πr²"
    }


def check_circumference(radius, answer):
    """
    Check 2πr.
    """

    radius = float(radius)

    expected = 2 * math.pi * radius

    return {
        "correct": close(expected, answer),
        "expected": expected,
        "given": float(answer),
        "rule": "2πr"
    }


def check_coordinate_distance(point1, point2, answer):
    """
    Check distance between two coordinate points.
    """

    x1, y1 = point1
    x2, y2 = point2

    expected = math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

    return {
        "correct": close(expected, answer),
        "expected": expected,
        "given": float(answer),
        "rule": "√((x₂-x₁)² + (y₂-y₁)²)"
    }


def check_gradient(point1, point2, answer):
    """
    Check gradient.
    """

    x1, y1 = point1
    x2, y2 = point2

    if x2 == x1:
        return {
            "correct": answer is None,
            "expected": None,
            "given": answer,
            "rule": "m = (y₂-y₁)/(x₂-x₁)"
        }

    expected = (y2 - y1) / (x2 - x1)

    return {
        "correct": close(expected, answer),
        "expected": expected,
        "given": float(answer),
        "rule": "m = (y₂-y₁)/(x₂-x₁)"
    }


def verification_message(result):
    """
    Convert checker result into a simple message.
    """

    if result["correct"]:
        return "✅ VERIFIED: The calculation is correct."

    return (
        "❌ CHECK FAILED.\n"
        f"Expected: {result.get('expected')}\n"
        f"Given: {result.get('given')}"
    )


if __name__ == "__main__":

    print("================================")
    print("AI CEO GEOMETRY CHECKER")
    print("================================")

    tests = [

        (
            "Pythagoras",
            check_pythagoras(3, 4, 5)
        ),

        (
            "Triangle angles",
            check_triangle_angles(50, 60, 70)
        ),

        (
            "Polygon",
            check_polygon_interior_sum(6, 720)
        ),

        (
            "Regular polygon",
            check_regular_polygon_angle(6, 120)
        ),

        (
            "Circle area",
            check_circle_area(5, math.pi * 25)
        ),

        (
            "Coordinate distance",
            check_coordinate_distance(
                (0, 0),
                (3, 4),
                5
            )
        ),

    ]

    for name, result in tests:

        print("\n" + name)
        print("-" * 30)
        print(verification_message(result))

    print("\n================================")
    print("CHECKER TEST COMPLETE")
    print("================================")
