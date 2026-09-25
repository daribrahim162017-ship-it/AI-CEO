import math
from fractions import Fraction


def calculate_fraction(a, b, operation):
    a = Fraction(a)
    b = Fraction(b)

    if operation == "+":
        return a + b
    if operation == "-":
        return a - b
    if operation == "*":
        return a * b
    if operation == "/":
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    raise ValueError("Unknown operation.")


def percentage_of(percent, number):
    return percent / 100 * number


def percentage_change(old, new):
    if old == 0:
        raise ValueError("Old value cannot be zero.")
    return ((new - old) / old) * 100


def mean(values):
    if not values:
        raise ValueError("No values supplied.")
    return sum(values) / len(values)


def round_sf(value, figures=3):
    if value == 0:
        return 0

    places = figures - 1 - math.floor(math.log10(abs(value)))
    return round(value, places)
