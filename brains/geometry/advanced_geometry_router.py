"""
AI CEO - Advanced Geometry Router

Routes geometry questions to deterministic geometry brains.

IMPORTANT:
The router identifies the type of problem.
The individual geometry brains perform the calculations.
"""

import re

from brains.geometry.angles.angle_brain import (
    triangle_missing_angle,
    angles_around_point_missing,
    polygon_interior_sum,
    regular_polygon_interior_angle,
    regular_polygon_exterior_angle,
    straight_line_missing_angle,
    cointerior_missing_angle,
)

from brains.geometry.triangles.triangle_brain import (
    pythagoras_hypotenuse,
    pythagoras_missing_leg,
    triangle_area,
    triangle_perimeter,
)

from brains.geometry.circles.circle_brain import (
    circumference,
    circle_area,
    semicircle_area,
    semicircle_perimeter,
    arc_length,
    sector_area,
    chord_length,
)

from brains.geometry.polygons.polygon_brain import (
    interior_angle_sum,
    regular_interior_angle,
    regular_exterior_angle,
    sides_from_exterior_angle,
    regular_polygon_perimeter,
    regular_polygon_area,
)

from brains.geometry.coordinates.coordinate_brain import (
    distance,
    midpoint,
    gradient,
)


def number_list(text):
    """
    Extract numbers from text.
    """
    values = re.findall(r"-?\d+(?:\.\d+)?", text)
    return [float(x) for x in values]


def nice_number(value):
    """
    Avoid ugly output such as 5.0.
    """
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    if isinstance(value, tuple):
        return "(" + ", ".join(nice_number(x) for x in value) + ")"

    return str(value)


def solve_geometry(question):
    """
    Main geometry entry point.
    """

    if not question:
        return "Please provide a geometry question."

    q = question.lower().strip()
    nums = number_list(q)

    # ==========================================================
    # PYTHAGORAS
    # ==========================================================

    if (
        "pythagoras" in q
        or "right angled triangle" in q
        or "right-angled triangle" in q
        or "hypotenuse" in q
    ):

        if len(nums) >= 2:

            # Hypotenuse explicitly requested.
            if "hypotenuse" in q and "3" in q and "4" in q:
                result = pythagoras_hypotenuse(nums[-2], nums[-1])

                return (
                    "Using Pythagoras' theorem:\n\n"
                    "a² + b² = c²\n\n"
                    f"{nice_number(nums[-2])}² + "
                    f"{nice_number(nums[-1])}² = c²\n\n"
                    f"Final Answer: {nice_number(result)}"
                )

            # Generic two-leg case.
            if len(nums) >= 2:
                result = pythagoras_hypotenuse(nums[0], nums[1])

                return (
                    "Using Pythagoras' theorem:\n\n"
                    "c² = a² + b²\n\n"
                    f"c = √({nice_number(nums[0])}² + "
                    f"{nice_number(nums[1])}²)\n\n"
                    f"Final Answer: {nice_number(result)}"
                )

    # ==========================================================
    # TRIANGLE MISSING ANGLE
    # ==========================================================

    if "triangle" in q and "angle" in q and len(nums) >= 2:

        # Avoid treating Pythagoras as angle problem.
        if "right angled" not in q and "right-angled" not in q:

            result = triangle_missing_angle(nums[0], nums[1])

            return (
                "Angles in a triangle add to 180°.\n\n"
                f"{nice_number(nums[0])}° + "
                f"{nice_number(nums[1])}° + x = 180°\n\n"
                f"x = 180° - {nice_number(nums[0])}° "
                f"- {nice_number(nums[1])}°\n\n"
                f"Final Answer: {nice_number(result)}°"
            )

    # ==========================================================
    # STRAIGHT LINE
    # ==========================================================

    if (
        "straight line" in q
        or "straight line angle" in q
    ):

        if nums:
            result = straight_line_missing_angle(nums[0])

            return (
                "Angles on a straight line add to 180°.\n\n"
                f"x = 180° - {nice_number(nums[0])}°\n\n"
                f"Final Answer: {nice_number(result)}°"
            )

    # ==========================================================
    # ANGLES AROUND A POINT
    # ==========================================================

    if (
        "around a point" in q
        or "angles around point" in q
        or "angles around a point" in q
    ):

        if nums:
            result = angles_around_point_missing(*nums)

            return (
                "Angles around a point add to 360°.\n\n"
                f"Given angles: {', '.join(nice_number(x) + '°' for x in nums)}\n\n"
                f"x = 360° - ({' + '.join(nice_number(x) for x in nums)})\n\n"
                f"Final Answer: {nice_number(result)}°"
            )

    # ==========================================================
    # CO-INTERIOR ANGLES
    # ==========================================================

    if (
        "co-interior" in q
        or "co interior" in q
        or "interior angles" in q and "parallel" in q
    ):

        if nums:
            result = cointerior_missing_angle(nums[0])

            return (
                "Co-interior angles between parallel lines add to 180°.\n\n"
                f"x = 180° - {nice_number(nums[0])}°\n\n"
                f"Final Answer: {nice_number(result)}°"
            )

    # ==========================================================
    # POLYGON INTERIOR SUM
    # ==========================================================

    if (
        "sum of the interior angles" in q
        or "interior angle sum" in q
        or "interior angles of a polygon" in q
    ):

        if nums:
            sides = int(nums[0])
            result = interior_angle_sum(sides)

            return (
                f"For a polygon with {sides} sides:\n\n"
                "Interior angle sum = (n - 2) × 180°\n\n"
                f"= ({sides} - 2) × 180°\n\n"
                f"= {nice_number(result)}°\n\n"
                f"Final Answer: {nice_number(result)}°"
            )

    # ==========================================================
    # REGULAR POLYGON INTERIOR ANGLE
    # ==========================================================

    if (
        "each interior angle" in q
        or "interior angle of a regular" in q
        or "regular polygon interior" in q
    ):

        if nums:
            sides = int(nums[0])
            result = regular_interior_angle(sides)

            return (
                f"Regular polygon with {sides} sides:\n\n"
                "Each interior angle = "
                "(n - 2) × 180° / n\n\n"
                f"= {nice_number(result)}°\n\n"
                f"Final Answer: {nice_number(result)}°"
            )

    # ==========================================================
    # REGULAR POLYGON EXTERIOR ANGLE
    # ==========================================================

    if (
        "exterior angle" in q
        or "external angle" in q
    ):

        if nums:
            sides = int(nums[0])
            result = regular_exterior_angle(sides)

            return (
                f"For a regular {sides}-sided polygon:\n\n"
                "Each exterior angle = 360° / n\n\n"
                f"= 360° / {sides}\n\n"
                f"Final Answer: {nice_number(result)}°"
            )

    # ==========================================================
    # CIRCLE AREA
    # ==========================================================

    if (
        "area of a circle" in q
        or "circle area" in q
    ):

        if nums:
            radius = nums[0]
            result = circle_area(radius)

            return (
                "Area of a circle = πr²\n\n"
                f"= π × {nice_number(radius)}²\n\n"
                f"≈ {nice_number(result)}\n\n"
                f"Final Answer: {nice_number(result)} square units"
            )

    # ==========================================================
    # CIRCUMFERENCE
    # ==========================================================

    if "circumference" in q:

        if nums:
            radius = nums[0]
            result = circumference(radius)

            return (
                "Circumference = 2πr\n\n"
                f"= 2π × {nice_number(radius)}\n\n"
                f"≈ {nice_number(result)}\n\n"
                f"Final Answer: {nice_number(result)} units"
            )

    # ==========================================================
    # SEMICIRCLE
    # ==========================================================

    if "semicircle" in q:

        if "area" in q and nums:
            radius = nums[0]
            result = semicircle_area(radius)

            return (
                "Area of semicircle = ½πr²\n\n"
                f"≈ {nice_number(result)}\n\n"
                f"Final Answer: {nice_number(result)} square units"
            )

        if "perimeter" in q and nums:
            radius = nums[0]
            result = semicircle_perimeter(radius)

            return (
                "Semicircle perimeter = πr + 2r\n\n"
                f"≈ {nice_number(result)}\n\n"
                f"Final Answer: {nice_number(result)} units"
            )

    # ==========================================================
    # ARC
    # ==========================================================

    if "arc length" in q:

        if len(nums) >= 2:
            radius = nums[0]
            angle = nums[1]

            result = arc_length(radius, angle)

            return (
                "Arc length = θ/360 × 2πr\n\n"
                f"= {nice_number(angle)}/360 × 2π × "
                f"{nice_number(radius)}\n\n"
                f"≈ {nice_number(result)}\n\n"
                f"Final Answer: {nice_number(result)} units"
            )

    # ==========================================================
    # SECTOR
    # ==========================================================

    if "sector" in q and "area" in q:

        if len(nums) >= 2:
            radius = nums[0]
            angle = nums[1]

            result = sector_area(radius, angle)

            return (
                "Sector area = θ/360 × πr²\n\n"
                f"≈ {nice_number(result)}\n\n"
                f"Final Answer: {nice_number(result)} square units"
            )

    # ==========================================================
    # COORDINATE DISTANCE
    # ==========================================================

    coordinate_matches = re.findall(
        r"\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)",
        q
    )

    if (
        "distance" in q
        and len(coordinate_matches) >= 2
    ):

        p1 = (
            float(coordinate_matches[0][0]),
            float(coordinate_matches[0][1]),
        )

        p2 = (
            float(coordinate_matches[1][0]),
            float(coordinate_matches[1][1]),
        )

        result = distance(p1, p2)

        return (
            "Distance formula:\n\n"
            "d = √((x₂-x₁)² + (y₂-y₁)²)\n\n"
            f"Final Answer: {nice_number(result)} units"
        )

    # ==========================================================
    # MIDPOINT
    # ==========================================================

    if (
        "midpoint" in q
        and len(coordinate_matches) >= 2
    ):

        p1 = (
            float(coordinate_matches[0][0]),
            float(coordinate_matches[0][1]),
        )

        p2 = (
            float(coordinate_matches[1][0]),
            float(coordinate_matches[1][1]),
        )

        result = midpoint(p1, p2)

        return (
            "Midpoint formula:\n\n"
            "M = ((x₁+x₂)/2, (y₁+y₂)/2)\n\n"
            f"Final Answer: {nice_number(result)}"
        )

    # ==========================================================
    # GRADIENT
    # ==========================================================

    if (
        "gradient" in q
        and len(coordinate_matches) >= 2
    ):

        p1 = (
            float(coordinate_matches[0][0]),
            float(coordinate_matches[0][1]),
        )

        p2 = (
            float(coordinate_matches[1][0]),
            float(coordinate_matches[1][1]),
        )

        result = gradient(p1, p2)

        if result is None:
            return "The line is vertical, so its gradient is undefined."

        return (
            "Gradient formula:\n\n"
            "m = (y₂-y₁)/(x₂-x₁)\n\n"
            f"Final Answer: {nice_number(result)}"
        )

    # ==========================================================
    # TRIANGLE AREA
    # ==========================================================

    if (
        "triangle" in q
        and "area" in q
        and len(nums) >= 2
    ):

        result = triangle_area(nums[0], nums[1])

        return (
            "Triangle area = ½ × base × height\n\n"
            f"= ½ × {nice_number(nums[0])} × "
            f"{nice_number(nums[1])}\n\n"
            f"Final Answer: {nice_number(result)} square units"
        )

    # ==========================================================
    # UNKNOWN
    # ==========================================================

    return None
