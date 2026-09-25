import sympy as sp


x, y, z = sp.symbols("x y z")


def solve_linear(a, b):
    """
    Solve ax + b = 0
    """
    if a == 0:
        raise ValueError("Coefficient of x cannot be zero.")

    return sp.solve(sp.Eq(a * x + b, 0), x)


def solve_quadratic(a, b, c):
    """
    Solve ax² + bx + c = 0
    """
    if a == 0:
        raise ValueError("This is not a quadratic equation.")

    equation = sp.Eq(a * x**2 + b * x + c, 0)

    return sp.solve(equation, x)


def solve_simultaneous(a1, b1, c1, a2, b2, c2):
    """
    Solve:
        a1*x + b1*y = c1
        a2*x + b2*y = c2
    """

    eq1 = sp.Eq(a1 * x + b1 * y, c1)
    eq2 = sp.Eq(a2 * x + b2 * y, c2)

    return sp.solve((eq1, eq2), (x, y))


def factor_expression(expression):
    return sp.factor(expression)


def expand_expression(expression):
    return sp.expand(expression)


def simplify_expression(expression):
    return sp.simplify(expression)
