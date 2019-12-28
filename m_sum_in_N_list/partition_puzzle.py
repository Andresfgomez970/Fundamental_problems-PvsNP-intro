import random


# Test data
numbers = [14175, 15055, 16616, 17495, 18072, 19390, 19731, 22161, 23320,
           23717, 26343, 28725, 29127, 32257, 40020, 41867, 43155, 46298,
           56734, 57176, 58306, 61848, 65825, 66042, 68634, 69189, 72936,
           74287, 74537, 81942, 82027, 82623, 82802, 82988, 90467, 97042,
           97507, 99564]


def gcd(a, b):
    """
    Calculate the gcd of two numbers.

    Parameters
    ----------
    a: int
        One of the numbers used for compute the gcd.
    b: int
        One of the number used for compute the gcd.

    Returns
    -------
    out: int
        The gcd of the two numbers passed as arguments.
    """
    while b != 0:
        # we have that gcd(a, b) = gcd(b, r) where a = b * q + r
        a, b = b, a % b
    return a


def extendedEuclideanAlgorimth(a, b):
    """
    Compute the coefficients of the bezout's identity.

    Bezout's identity: for integer a and b exist integers x and y such that
        a * x + b * y = d, where d = gcd(a, b).

    Parameters
    ----------
    a: int
        One of the numbers used for compute the coefficients of the bezout's
        identity
    b: int
        One of the numbers used for compute the coefficients of the bezout's
        identity

    Returns
    -------
    out: tuple
        The coefficientes of the bezout's identity
    """
    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1

    while r1 != 0:
        quotient = r0 // r1
        r0, r1 = r1, r0 - quotient * r1
        s0, s1 = s1, s0 - quotient * s1
        t0, t1 = t1, t0 - quotient * t1

    return s0, t0


def gcdN(array):
    """
    Calculate the gcd of n numbers.

    Parameters
    ----------
    a: iterable
        iterable object over integers values

    Returns
    -------
    out: int
        The gcd of the n numbers passed as iterable argument.
    """
    # for n numbers a1, a2,..., an wa have that
    # gcd(a1, a2,..., an) = gcd(a1, gcd(a2, a3, .... an)),
    # then we recursively calculate for gcd(a2, a3, .... an)
    result = array[0]

    for i in array:
        result = gcd(result, i)

        # if result is one, then all following values will be 1
        if result == 1:
            return 1

    return result


def isSoluble(c, *numbers):
    """
    Check if the diophantine equation a1 * x1 + a2 * x2 + ... + an * xn = c is
    soluble

    Parameters
    ----------
    c: int
        integer c of the equation a1 * x1 + a2 * x2 + ... + an * xn = c
    a1, a2, a3,..., an: ints
        coefficients a1, a2, ..., an of the equation
        a1 * x1 + a2 * x2 + ... + an * xn = c

    Returns
    -------
    out: bool
        True if the equation a1 * x1 + a2 * x2 + ... + an * xn = c has a
        solution for x1, x2,..., xn False otherwise
    """
    return True if c % gcdN(numbers) == 0 else False


def solve(c, a, b):
    """
    Solve the equation a * x + b * y = c for x and y.

    Parameters
    ----------
    c: int
        integer c of the equation a * x + b * y = c.
    a, b: ints
        coefficients of the equation a * x + b * y = c.
    Returns
    -------
    out: tuple
        Solution of the equation a * x + b * y = c.
    """
    x0, y0 = extendedEuclideanAlgorimth(a, b)

    d = gcd(a, b)

    return x0 * c // d, y0 * c // d


def isMovible(x0, y0, a, b, target=1, first=True):
    d = gcd(a, b)

    if first:
        quotient = b // d

        difference = target - x0

        if difference % quotient == 0:
            return True
    else:
        quotient = a // d

        difference = target - y0

        if difference % quotient == 0:
            return True

    return False


def moveSolution(x0, y0, a, b, target=1, first=True):
    """
    Move the solucion of a diophantine equation to other, conditioning one of
    the solutions.

    A diophantine equation a * x + b * y = c have infinity solutions, if x0 and
    y0 are solution, then x = x0 + (b // d) * t and y = y0 - (a // d) * t is
    a solution too, where t is a integer parameter.

    Parameters
    ----------
    x0, y0: ints
        One of the solutions of the diophantine equation a * x + b * y = c.
    a, b: ints
        Coefficients of the diophantine equations a * x + b * y = c.
    target: int, opcional
        Value of the solution.
    first: bool, optional
        If it's True the value to be conditionated is the solution for x.

    Returns
    -------
        out: tuple
            new solution of the diophantine equation a * x + b * y = c.
    """
    d = gcd(a, b)
    x, y = x0, y0

    if first:
        quotient = b // d

        difference = target - x0

        if difference % quotient == 0:
            t = difference // quotient
            y = y0 - (a // d) * t
            x = target
    else:
        quotient = a // d

        difference = target - y0

        if difference % quotient == 0:
            t = -(difference // quotient)
            x = x0 + (b // d) * t
            y = target

    return x, y


def solveN(c, numbers):
    """
    Solve the equation a1 * x1 + a2 * x2 + ... + an * xn = c for
    x1, x2,..., xn.

    Parameters
    ----------
    c: int
        integer c of the equation a1 * x1 + a2 * x2 + ... + an * xn = c.
    a, b: ints
        coefficients of the equation a1 * x1 + a2 * x2 + ... + an * xn = c.
    Returns
    -------
    out: tuple
        Solution of the equation a1 * x1 + a2 * x2 + ... + an * xn = c.
    """
    values = []

    while len(numbers) > 2:
        copy = numbers[1:]

        gcd = gcdN(copy)
        solution = solve(c, numbers[0], gcd)

        target = random.randint(0, 1)
        solution = moveSolution(*solution, numbers[0], gcd, target=target)

        c = gcd * solution[1]
        numbers = copy

        values.append(solution[0])

    solution = solve(c, numbers[0], numbers[1])

    values.extend(solution)

    return tuple(values)


def test():
    """
    Find the solutions of the partition puzzle problem of the test data.

    1000000 is the total amount tha we need to sum, and numbers is the list of
    numbers that will be used
    """
    sumar = lambda x: sum(map(abs, x))

    for n in range(1000000):
        solution = solveN(1000000, numbers)

        # if the solution only have 1's and 0's
        if sumar(solution) <= 38:
            break

    return solution


def main():
    print(test())


if __name__ == '__main__':
    main()
