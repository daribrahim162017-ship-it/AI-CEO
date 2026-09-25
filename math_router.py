import re
import math

from brains.geometry_brain import (
    triangle_missing_angle,
    straight_line_missing_angle,
    angles_around_point_missing,
    quadrilateral_missing_angle,
    polygon_interior_sum,
    regular_polygon_angle,
    exterior_angle_regular_polygon,
    pythagoras_hypotenuse,
    pythagoras_missing_side,
    triangle_area,
    circle_area,
    circle_circumference,
    semicircle_area,
    semicircle_arc,
    semicircle_perimeter,
    rectangle_area,
    rectangle_perimeter,
    square_area,
    square_perimeter,
)

from brains.arithmetic_brain import (
    percentage_of,
    percentage_change,
    mean,
)

from brains.ratio_brain import (
    simplify_ratio,
    share_from_ratio,
)


def extract_numbers(text):
    return [
        float(x)
        for x in re.findall(
            r"-?\d+(?:\.\d+)?",
            text
        )
    ]


def detect_math_type(question):
    text = question.lower()

    if "pythagoras" in text or "right angled triangle" in text or "right-angled triangle" in text:
        return "pythagoras"

    if "triangle" in text and "angle" in text:
        return "triangle_angle"

    if "straight line" in text or "straight-line" in text:
        return "straight_line"

    if "around a point" in text:
        return "around_point"

    if "quadrilateral" in text:
        return "quadrilateral"

    if "polygon" in text:
        return "polygon"

    if "circle" in text and "circumference" in text:
        return "circle_circumference"

    if "circle" in text and "area" in text:
        return "circle_area"

    if "semicircle" in text and "area" in text:
        return "semicircle_area"

    if "semicircle" in text and "perimeter" in text:
        return "semicircle_perimeter"

    if "triangle" in text and "area" in text:
        return "triangle_area"

    if "rectangle" in text and "area" in text:
        return "rectangle_area"

    if "rectangle" in text and "perimeter" in text:
        return "rectangle_perimeter"

    if "square" in text and "area" in text:
        return "square_area"

    if "square" in text and "perimeter" in text:
        return "square_perimeter"

    if "percentage" in text or "percent" in text:
        return "percentage"

    if "ratio" in text:
        return "ratio"

    if "average" in text or "mean" in text:
        return "mean"

    return None


def solve_math(question):
    problem_type = detect_math_type(question)
    numbers = extract_numbers(question)

    if problem_type == "triangle_angle":
        if len(numbers) >= 2:
            a = numbers[0]
            b = numbers[1]
            answer = triangle_missing_angle(a, b)

            return (
                "Triangle angles add up to 180°.\n\n"
                f"{a:g}° + {b:g}° + x = 180°\n\n"
                f"x = 180° - {a:g}° - {b:g}°\n\n"
                f"Final Answer: {answer:g}°"
            )

    if problem_type == "straight_line":
        if numbers:
            a = numbers[0]
            answer = straight_line_missing_angle(a)

            return (
                "Angles on a straight line add up to 180°.\n\n"
                f"{a:g}° + x = 180°\n\n"
                f"Final Answer: {answer:g}°"
            )

    if problem_type == "around_point":
        if numbers:
            answer = angles_around_point_missing(numbers)

            return (
                "Angles around a point add up to 360°.\n\n"
                f"Known angles total = {sum(numbers):g}°\n\n"
                f"Final Answer: {answer:g}°"
            )

    if problem_type == "quadrilateral":
        if len(numbers) >= 3:
            answer = quadrilateral_missing_angle(numbers[:3])

            return (
                "The angles of a quadrilateral add up to 360°.\n\n"
                f"Known angles total = {sum(numbers[:3]):g}°\n\n"
                f"Final Answer: {answer:g}°"
            )

    if problem_type == "polygon":
        if numbers:
            n = int(numbers[0])
            total = polygon_interior_sum(n)
            each = regular_polygon_angle(n)

            return (
                f"A polygon with {n} sides has interior angle sum:\n\n"
                f"(n - 2) × 180°\n\n"
                f"= {total:g}°\n\n"
                f"If it is regular, each interior angle is:\n\n"
                f"{each:g}°"
            )

    if problem_type == "pythagoras":
        if len(numbers) >= 2:
            a = numbers[0]
            b = numbers[1]
            c = pythagoras_hypotenuse(a, b)

            return (
                "Using Pythagoras' theorem:\n\n"
                "a² + b² = c²\n\n"
                f"{a:g}² + {b:g}² = c²\n\n"
                f"{a*a:g} + {b*b:g} = c²\n\n"
                f"c² = {a*a + b*b:g}\n\n"
                f"c = {c:.3f}\n\n"
                f"Final Answer: {c:.3f}"
            )

    if problem_type == "triangle_area":
        if len(numbers) >= 2:
            base = numbers[0]
            height = numbers[1]
            answer = triangle_area(base, height)

            return (
                "Area of triangle = ½ × base × height\n\n"
                f"= ½ × {base:g} × {height:g}\n\n"
                f"Final Answer: {answer:g}"
            )

    if problem_type == "circle_area":
        if numbers:
            r = numbers[0]
            answer = circle_area(r)

            return (
                "Area of circle = πr²\n\n"
                f"= π × {r:g}²\n\n"
                f"Final Answer: {answer:.3f}"
            )

    if problem_type == "circle_circumference":
        if numbers:
            r = numbers[0]
            answer = circle_circumference(r)

            return (
                "Circumference = 2πr\n\n"
                f"= 2π × {r:g}\n\n"
                f"Final Answer: {answer:.3f}"
            )

    if problem_type == "semicircle_area":
        if numbers:
            r = numbers[0]
            answer = semicircle_area(r)

            return (
                "Area of semicircle = ½πr²\n\n"
                f"= ½π × {r:g}²\n\n"
                f"Final Answer: {answer:.3f}"
            )

    if problem_type == "semicircle_perimeter":
        if numbers:
            r = numbers[0]
            answer = semicircle_perimeter(r)

            return (
                "Semicircle perimeter = πr + 2r\n\n"
                f"= π × {r:g} + 2 × {r:g}\n\n"
                f"Final Answer: {answer:.3f}"
            )

    if problem_type == "rectangle_area":
        if len(numbers) >= 2:
            answer = rectangle_area(numbers[0], numbers[1])

            return f"Rectangle area = {answer:g}"

    if problem_type == "rectangle_perimeter":
        if len(numbers) >= 2:
            answer = rectangle_perimeter(numbers[0], numbers[1])

            return f"Rectangle perimeter = {answer:g}"

    if problem_type == "square_area":
        if numbers:
            answer = square_area(numbers[0])

            return f"Square area = {answer:g}"

    if problem_type == "square_perimeter":
        if numbers:
            answer = square_perimeter(numbers[0])

            return f"Square perimeter = {answer:g}"

    if problem_type == "percentage":
        if len(numbers) >= 2:
            answer = percentage_of(numbers[0], numbers[1])

            return (
                f"{numbers[0]:g}% of {numbers[1]:g}\n\n"
                f"= {answer:g}"
            )

    if problem_type == "ratio":
        if len(numbers) >= 2:
            a, b = simplify_ratio(numbers[0], numbers[1])

            return f"Simplified ratio = {a}:{b}"

    if problem_type == "mean":
        if numbers:
            answer = mean(numbers)

            return f"Mean = {answer:g}"

    return None
