import math
import sympy as sp


class GeometryEngine:

    # =========================
    # ANGLES
    # =========================

    @staticmethod
    def triangle_angle(a, b):
        return sp.simplify(180 - a - b)

    @staticmethod
    def straight_line_angle(a):
        return sp.simplify(180 - a)

    @staticmethod
    def angles_around_point(known_angles):
        return sp.simplify(360 - sum(known_angles))

    @staticmethod
    def quadrilateral_angle(known_angles):
        return sp.simplify(360 - sum(known_angles))

    @staticmethod
    def polygon_interior_sum(n):
        if n < 3:
            raise ValueError("A polygon must have at least 3 sides.")
        return sp.simplify((n - 2) * 180)

    @staticmethod
    def regular_polygon_interior_angle(n):
        return sp.simplify(((n - 2) * 180) / n)

    @staticmethod
    def regular_polygon_exterior_angle(n):
        if n < 3:
            raise ValueError("A polygon must have at least 3 sides.")
        return sp.simplify(360 / n)

    # =========================
    # TRIANGLES
    # =========================

    @staticmethod
    def pythagoras_hypotenuse(a, b):
        return sp.sqrt(a**2 + b**2)

    @staticmethod
    def pythagoras_missing_side(h, a):
        value = h**2 - a**2

        if value < 0:
            raise ValueError("The hypotenuse must be longer than the other side.")

        return sp.sqrt(value)

    @staticmethod
    def triangle_area(base, height):
        return sp.Rational(1, 2) * base * height

    @staticmethod
    def equilateral_triangle_area(side):
        return sp.sqrt(3) * side**2 / 4

    @staticmethod
    def heron_area(a, b, c):
        s = sp.Rational(1, 2) * (a + b + c)

        if s <= a or s <= b or s <= c:
            raise ValueError("These three sides do not form a triangle.")

        return sp.sqrt(s * (s-a) * (s-b) * (s-c))

    # =========================
    # CIRCLES
    # =========================

    @staticmethod
    def circle_area(radius):
        return sp.pi * radius**2

    @staticmethod
    def circumference(radius):
        return 2 * sp.pi * radius

    @staticmethod
    def diameter_from_radius(radius):
        return 2 * radius

    @staticmethod
    def radius_from_diameter(diameter):
        return diameter / 2

    @staticmethod
    def arc_length(radius, angle_degrees):
        return sp.pi * radius * angle_degrees / 180

    @staticmethod
    def sector_area(radius, angle_degrees):
        return sp.pi * radius**2 * angle_degrees / 360

    @staticmethod
    def semicircle_area(radius):
        return sp.pi * radius**2 / 2

    @staticmethod
    def semicircle_arc(radius):
        return sp.pi * radius

    @staticmethod
    def semicircle_perimeter(radius):
        return sp.pi * radius + 2 * radius

    # =========================
    # RECTANGLES / SQUARES
    # =========================

    @staticmethod
    def rectangle_area(length, width):
        return length * width

    @staticmethod
    def rectangle_perimeter(length, width):
        return 2 * (length + width)

    @staticmethod
    def square_area(side):
        return side**2

    @staticmethod
    def square_perimeter(side):
        return 4 * side

    @staticmethod
    def square_diagonal(side):
        return side * sp.sqrt(2)

    # =========================
    # POLYGONS
    # =========================

    @staticmethod
    def regular_polygon_perimeter(n, side):
        return n * side

    @staticmethod
    def regular_polygon_area(n, side):
        return (
            n * side**2
            / (4 * sp.tan(sp.pi / n))
        )

    # =========================
    # COORDINATE GEOMETRY
    # =========================

    @staticmethod
    def distance(x1, y1, x2, y2):
        return sp.sqrt((x2-x1)**2 + (y2-y1)**2)

    @staticmethod
    def midpoint(x1, y1, x2, y2):
        return (
            sp.Rational(x1+x2, 2),
            sp.Rational(y1+y2, 2)
        )

    @staticmethod
    def gradient(x1, y1, x2, y2):
        if x2 == x1:
            return sp.oo

        return sp.Rational(y2-y1, x2-x1)

    @staticmethod
    def line_equation(m, x, c):
        return sp.expand(m*x + c)

    # =========================
    # 3D GEOMETRY
    # =========================

    @staticmethod
    def cuboid_volume(length, width, height):
        return length * width * height

    @staticmethod
    def cuboid_surface_area(length, width, height):
        return 2 * (
            length*width +
            length*height +
            width*height
        )

    @staticmethod
    def cube_volume(side):
        return side**3

    @staticmethod
    def cube_surface_area(side):
        return 6 * side**2

    @staticmethod
    def cylinder_volume(radius, height):
        return sp.pi * radius**2 * height

    @staticmethod
    def cylinder_surface_area(radius, height):
        return 2 * sp.pi * radius * (radius + height)

    @staticmethod
    def sphere_volume(radius):
        return sp.Rational(4, 3) * sp.pi * radius**3

    @staticmethod
    def sphere_surface_area(radius):
        return 4 * sp.pi * radius**2

    # =========================
    # TRIGONOMETRY
    # =========================

    @staticmethod
    def sine_opposite(hypotenuse, angle):
        return hypotenuse * sp.sin(sp.rad(angle))

    @staticmethod
    def cosine_adjacent(hypotenuse, angle):
        return hypotenuse * sp.cos(sp.rad(angle))

    @staticmethod
    def tangent_opposite(adjacent, angle):
        return adjacent * sp.tan(sp.rad(angle))

    @staticmethod
    def sine_rule_side(a, A, B, b):
        return a * sp.sin(sp.rad(B)) / sp.sin(sp.rad(A))

    @staticmethod
    def cosine_rule_side(a, b, C):
        return sp.sqrt(
            a**2 + b**2 -
            2*a*b*sp.cos(sp.rad(C))
        )

    # =========================
    # UTILITIES
    # =========================

    @staticmethod
    def decimal(value, digits=10):
        value = sp.N(value, digits)

        if abs(float(value) - round(float(value))) < 1e-10:
            return int(round(float(value)))

        return float(value)

    @staticmethod
    def simplify(value):
        return sp.simplify(value)
