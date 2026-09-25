from fractions import Fraction


def simplify_ratio(a, b):
    if b == 0:
        raise ValueError("Cannot have zero as the second ratio value.")

    fraction = Fraction(a, b)

    return fraction.numerator, fraction.denominator


def share_from_ratio(total, a, b):
    total_parts = a + b

    if total_parts == 0:
        raise ValueError("Ratio parts cannot both be zero.")

    first = total * a / total_parts
    second = total * b / total_parts

    return first, second


def scale_ratio(a, b, multiplier):
    return a * multiplier, b * multiplier
