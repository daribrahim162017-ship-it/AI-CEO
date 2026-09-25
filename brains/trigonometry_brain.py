import math


def sin_deg(angle):
    return math.sin(math.radians(angle))


def cos_deg(angle):
    return math.cos(math.radians(angle))


def tan_deg(angle):
    return math.tan(math.radians(angle))


def asin_deg(value):
    if value < -1 or value > 1:
        raise ValueError("Value must be between -1 and 1.")
    return math.degrees(math.asin(value))


def acos_deg(value):
    if value < -1 or value > 1:
        raise ValueError("Value must be between -1 and 1.")
    return math.degrees(math.acos(value))


def atan_deg(value):
    return math.degrees(math.atan(value))


def sine_rule_side(a, A, B):
    """
    a/sin(A) = b/sin(B)
    """
    return a * math.sin(math.radians(B)) / math.sin(math.radians(A))


def cosine_rule_side(a, b, C):
    """
    c² = a² + b² - 2ab cos(C)
    """
    value = a*a + b*b - 2*a*b*math.cos(math.radians(C))

    if value < 0:
        raise ValueError("Invalid triangle measurements.")

    return math.sqrt(value)


def cosine_rule_angle(a, b, c):
    """
    cos(C) = (a²+b²-c²)/(2ab)
    """
    value = (a*a + b*b - c*c) / (2*a*b)

    if value < -1 or value > 1:
        raise ValueError("Invalid triangle measurements.")

    return math.degrees(math.acos(value))
