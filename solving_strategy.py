import logging

from sage.all import RR
from sage.all import ZZ
from sage.all import Zmod

import small_roots


def basic_attack(p, h, xi1, xi2, s=5):
    """
    Recovers the small roots of a bivariate homogeneous equation.
    :param p: the Mersenne prime
    :param h: the given known h
    :param xi1: the exponential parameter for f
    :param xi2: the exponential parameter for g
    :param s: the s value to use for the small roots method (default: 3)
    :return: a tuple containing the roots
    """
    x, y = Zmod(p)["x", "y"].gens()
    f = x - h * y
    X = int(RR(p) ** xi1)
    Y = int(RR(p) ** xi2)
    logging.info(f"Trying s = {s}...")
    for x0, y0 in small_roots.modular_multivariate(f, p, s, s, [X, Y]):
        z = int(f(x0, y0))
        if z % p == 0:
            return x0, y0
    return None, None


def improved_attack(p, h, xi1, xi2, s=5):
    """
    Recovers the small roots of a bivariate homogeneous equation.
    :param p: the Mersenne prime
    :param h: the given known h
    :param xi1: the exponential parameter for f
    :param xi2: the exponential parameter for g
    :param s: the s value to use for the small roots method (default: 5)
    :return: a tuple containing the roots
    """
    x, y = Zmod(p)["x", "y"].gens()
    f = x - h * y
    X = int(RR(p) ** xi1)
    Y = int(RR(p) ** xi2)
    logging.info(f"Trying s = {s}...")
    for x0, y0 in small_roots.modular_bivariate_homogeneous(f, p, s, s, X, Y):
        z = int(f(x0, y0))
        if z % p == 0:
            return x0, y0
    return None, None
    