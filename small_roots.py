import logging
import time

from sage.all import *

DEBUG_ROOTS = None
Bound_Check = False
USE_FLATTER = True


def create_lattice(pr, shifts, bounds, order="invlex", sort_shifts_reverse=False, sort_monomials_reverse=False):
    """
    Creates a lattice from a list of shift polynomials.
    :param pr: the polynomial ring
    :param shifts: the shifts
    :param bounds: the bounds
    :param order: the order to sort the shifts/monomials by
    :param sort_shifts_reverse: set to true to sort the shifts in reverse order
    :param sort_monomials_reverse: set to true to sort the monomials in reverse order
    :return: a tuple of lattice and list of monomials
    """
    logging.debug(f"Creating a lattice with {len(shifts)} shifts (order = {order}, sort_shifts_reverse = {sort_shifts_reverse}, sort_monomials_reverse = {sort_monomials_reverse})...")
    if pr.ngens() > 1:
        pr_ = pr.change_ring(ZZ, order=order)
        shifts = [pr_(shift) for shift in shifts]

    monomials = set()
    for shift in shifts:
        monomials.update(shift.monomials())

    shifts.sort(reverse=sort_shifts_reverse)
    monomials = sorted(monomials, reverse=sort_monomials_reverse)
    L = matrix(ZZ, len(shifts), len(monomials))
    for row, shift in enumerate(shifts):
        for col, monomial in enumerate(monomials):
            L[row, col] = shift.monomial_coefficient(monomial) * monomial(*bounds)

    monomials = [pr(monomial) for monomial in monomials]
    return L, monomials


def reduce_lattice(L, delta=0.8):
    """
    Reduces a lattice basis using a lattice reduction algorithm (currently LLL).
    :param L: the lattice basis
    :param delta: the delta parameter for LLL (default: 0.8)
    :return: the reduced basis
    """
    # logging.debug(f"Reducing a {L.nrows()} x {L.ncols()} lattice...")
    # logging.info(f"Reducing a {L.nrows()} x {L.ncols()} lattice...")
    start_time = time.perf_counter()
    if USE_FLATTER:
        from subprocess import check_output
        from re import findall
        LL = "[[" + "]\n[".join(" ".join(map(str, row)) for row in L) + "]]"
        ret = check_output(["flatter"], input = LL.encode())
        L_reduced = matrix(L.nrows(), L.ncols(), map(int, findall(rb"-?\d+", ret)))
    else:
        L_reduced = L.LLL(delta)
    end_time = time.perf_counter()
    reduced_time = end_time - start_time
    logging.info(f"Reducing a {L.nrows()} x {L.ncols()} lattice within {reduced_time:.3f} seconds...")
    return L_reduced


def reconstruct_polynomials(B, f, modulus, monomials, bounds, preprocess_polynomial=lambda x: x, divide_gcd=True):
    """
    Reconstructs polynomials from the lattice basis in the monomials.
    :param B: the lattice basis
    :param f: the original polynomial (if set to None, polynomials will not be divided by f if possible)
    :param modulus: the original modulus
    :param monomials: the monomials
    :param bounds: the bounds
    :param preprocess_polynomial: a function which preprocesses a polynomial before it is added to the list (default: identity function)
    :param divide_gcd: if set to True, polynomials will be pairwise divided by their gcd if possible (default: True)
    :return: a list of polynomials
    """
    logging.debug(f"Reconstructing polynomials (divide_original = {f is not None}, modulus_bound = {modulus is not None}, divide_gcd = {divide_gcd})...")
    polynomials = []
    for row in range(B.nrows()):
        norm_squared = 0
        w = 0
        polynomial = 0
        for col, monomial in enumerate(monomials):
            if B[row, col] == 0:
                continue
            norm_squared += B[row, col] ** 2
            w += 1
            assert B[row, col] % monomial(*bounds) == 0
            polynomial += B[row, col] * monomial // monomial(*bounds)

        # Equivalent to norm >= modulus / sqrt(w)
        if Bound_Check and modulus is not None and norm_squared * w >= modulus ** 2:
            logging.debug(f"Row {row} is too large, ignoring...")
            continue

        polynomial = preprocess_polynomial(polynomial)

        if f is not None and polynomial % f == 0:
            logging.debug(f"Original polynomial divides reconstructed polynomial at row {row}, dividing...")
            polynomial //= f

        if divide_gcd:
            for i in range(len(polynomials)):
                g = gcd(polynomial, polynomials[i])
                # TODO: why are we only allowed to divide out g if it is constant?
                if g != 1 and g.is_constant():
                    logging.debug(f"Reconstructed polynomial has gcd @#$ with polynomial at {i}, dividing...")
                    polynomial //= g
                    polynomials[i] //= g

        if polynomial.is_constant():
            logging.debug(f"Polynomial at row {row} is constant, ignoring...")
            continue

        if DEBUG_ROOTS is not None:
            logging.debug(f"Polynomial at row {row} roots check: {polynomial(*DEBUG_ROOTS)}")

        polynomials.append(polynomial)

    logging.debug(f"Reconstructed {len(polynomials)} polynomials")
    return polynomials


def find_roots_univariate(x, polynomial):
    """
    Returns a generator generating all roots of a univariate polynomial in an unknown.
    :param x: the unknown
    :param polynomial: the polynomial
    :return: a generator generating dicts of (x: root) entries
    """
    if polynomial.is_constant():
        return

    for root in polynomial.roots(multiplicities=False):
        if root != 0:
            yield {x: int(root)}


def find_roots_gcd(pr, polynomials):
    """
    Returns a generator generating all roots of a polynomial in some unknowns.
    Uses pairwise gcds to find trivial roots.
    :param pr: the polynomial ring
    :param polynomials: the reconstructed polynomials
    :return: a generator generating dicts of (x0: x0root, x1: x1root, ...) entries
    """
    if pr.ngens() != 2:
        return

    logging.debug("Computing pairwise gcds to find trivial roots...")
    x, y = pr.gens()
    for i in range(len(polynomials)):
        for j in range(i):
            g = gcd(polynomials[i], polynomials[j])
            if g.degree() == 1 and g.nvariables() == 2 and g.constant_coefficient() == 0:
                # g = ax + by
                a = int(g.monomial_coefficient(x))
                b = int(g.monomial_coefficient(y))
                yield {x: b, y: a}
                yield {x: -b, y: a}


def find_roots_groebner(pr, polynomials):
    """
    Returns a generator generating all roots of a polynomial in some unknowns.
    Uses Groebner bases to find the roots.
    :param pr: the polynomial ring
    :param polynomials: the reconstructed polynomials
    :return: a generator generating dicts of (x0: x0root, x1: x1root, ...) entries
    """
    # We need to change the ring to QQ because groebner_basis is much faster over a field.
    # We also need to change the term order to lexicographic to allow for elimination.
    gens = pr.gens()
    s = Sequence(polynomials, pr.change_ring(QQ, order="lex"))
    while len(s) > 0:
        G = s.groebner_basis()
        logging.debug(f"Sequence length: {len(s)}, Groebner basis length: {len(G)}")
        if len(G) == len(gens):
            logging.debug(f"Found Groebner basis with length {len(gens)}, trying to find roots...")
            roots = {}
            for polynomial in G:
                vars = polynomial.variables()
                if len(vars) == 1:
                    for root in find_roots_univariate(vars[0], polynomial.univariate_polynomial()):
                        roots |= root

            if len(roots) == pr.ngens():
                yield roots
                return

            return
        else:
            # Remove last element (the biggest vector) and try again.
            s.pop()


def find_roots_resultants(gens, polynomials):
    """
    Returns a generator generating all roots of a polynomial in some unknowns.
    Recursively computes resultants to find the roots.
    :param polynomials: the reconstructed polynomials
    :param gens: the unknowns
    :return: a generator generating dicts of (x0: x0root, x1: x1root, ...) entries
    """
    if len(polynomials) == 0:
        return

    if len(gens) == 1:
        if polynomials[0].is_univariate():
            yield from find_roots_univariate(gens[0], polynomials[0].univariate_polynomial())
    else:
        resultants = [polynomials[0].resultant(polynomials[i], gens[0]) for i in range(1, len(gens))]
        for roots in find_roots_resultants(gens[1:], resultants):
            for polynomial in polynomials:
                polynomial = polynomial.subs(roots)
                if polynomial.is_univariate():
                    for root in find_roots_univariate(gens[0], polynomial.univariate_polynomial()):
                        yield roots | root


def find_roots_variety(pr, polynomials):
    """
    Returns a generator generating all roots of a polynomial in some unknowns.
    Uses the Sage variety (triangular decomposition) method to find the roots.
    :param pr: the polynomial ring
    :param polynomials: the reconstructed polynomials
    :return: a generator generating dicts of (x0: x0root, x1: x1root, ...) entries
    """
    # We need to change the ring to QQ because variety requires a field.
    s = Sequence([], pr.change_ring(QQ))
    for polynomial in polynomials:
        s.append(polynomial)
        I = s.ideal()
        dim = I.dimension()
        logging.debug(f"Sequence length: {len(s)}, Ideal dimension: {dim}")
        if dim == -1:
            s.pop()
        elif dim == 0:
            logging.debug("Found ideal with dimension 0, computing variety...")
            for roots in I.variety(ring=ZZ):
                yield {k: int(v) for k, v in roots.items()}

            return


def find_roots(pr, polynomials, method="groebner"):
    """
    Returns a generator generating all roots of a polynomial in some unknowns.
    The method used depends on the method parameter.
    :param pr: the polynomial ring
    :param polynomials: the reconstructed polynomials
    :param method: the method to use, can be "groebner", "resultants", or "variety" (default: "groebner")
    :return: a generator generating dicts of (x0: x0root, x1: x1root, ...) entries
    """
    if pr.ngens() == 1:
        logging.debug("Using univariate polynomial to find roots...")
        for polynomial in polynomials:
            yield from find_roots_univariate(pr.gen(), polynomial)
    else:
        # Always try this method because it can find roots the others can't.
        yield from find_roots_gcd(pr, polynomials)

        if method == "groebner":
            logging.debug("Using Groebner basis method to find roots...")
            yield from find_roots_groebner(pr, polynomials)
        elif method == "resultants":
            logging.debug("Using resultants method to find roots...")
            yield from find_roots_resultants(pr.gens(), polynomials)
        elif method == "variety":
            logging.debug("Using variety method to find roots...")
            yield from find_roots_variety(pr, polynomials)


def _get_shifts(m, x, k, shift, j, sum, shifts):
    if j == len(x):
        shifts.append(shift)
    else:
        for ij in range(m + 1 - k - sum):
            _get_shifts(m, x, k, shift * x[j] ** ij, j + 1, sum + ij, shifts)


def modular_multivariate(f, N, m, t, X, roots_method="groebner"):
    """
    Computes small modular roots of a multivariate polynomial.
    More information: Herrmann M., May A., "Solving Linear Equations Modulo Divisors: On Factoring Given Any Bits" (Section 3 and 4)
    :param f: the polynomial
    :param N: the modulus
    :param m: the the parameter m
    :param t: the the parameter t
    :param X: a list of approximate bounds on the roots for each variable
    :param roots_method: the method to use to find roots (default: "groebner")
    :return: a generator generating small roots (tuples) of the polynomial
    """
    f = f.change_ring(ZZ)
    pr = f.parent()
    x = pr.gens()

    # Sage lm method depends on the term ordering
    l = 1
    for monomial in f.monomials():
        if monomial % l == 0:
            l = monomial

    al = int(f.coefficient(l))
    assert gcd(al, N) == 1
    f_ = (pow(al, -1, N) * f % N).change_ring(ZZ)

    logging.debug("Generating shifts...")

    shifts = []
    for k in range(m + 1):
        _get_shifts(m, x, k, f_ ** k * N ** max(t - k, 0), 1, 0, shifts)

    L, monomials = create_lattice(pr, shifts, X)
    L = reduce_lattice(L)
    polynomials = reconstruct_polynomials(L, f, N, monomials, X)
    start_time = time.perf_counter()
    solutions = find_roots(pr, polynomials, method=roots_method)
    end_time = time.perf_counter()
    solution_time = end_time - start_time
    logging.info(f"Finding roots within {solution_time:.3f} seconds...")
    for roots in solutions:
        yield tuple(roots[xi] for xi in x)


def modular_bivariate_homogeneous(f, N, m, t, X, Y, roots_method="groebner"):
    """
    Computes small modular roots of a bivariate polynomial.
    More information: Lu Y. et al., "Solving Linear Equations Modulo Unknown Divisors: Revisited (Theorem 7)
    :param f: the polynomial
    :param N: the modulus
    :param m: the the parameter m
    :param t: the the parameter t
    :param X: an approximate bound on the x roots
    :param Y: an approximate bound on the y roots
    :param roots_method: the method to use to find roots (default: "groebner")
    :return: a generator generating small roots (tuples of x and y roots) of the polynomial
    """
    f = f.change_ring(ZZ)
    pr = PolynomialRing(ZZ, ['x', 'y'])
    x, y = pr.gens()

    al = int(f.coefficient(x))
    assert gcd(al, N) == 1
    f_ = (pow(al, -1, N) * f % N).change_ring(ZZ)

    logging.debug("Generating shifts...")

    shifts = []
    for k in range(m + 1):
        g = y ** (m - k) * f_ ** k * N ** max(t - k, 0)
        shifts.append(g)

    L, monomials = create_lattice(pr, shifts, [X, Y])
    L = reduce_lattice(L)
    polynomials = reconstruct_polynomials(L, f, N ** t, monomials, [X, Y])
    start_time = time.perf_counter()
    # solutions = find_roots(pr, polynomials, method=roots_method)
    t = var('t')
    g = polynomials[0].subs(x = t*y).subs(y = 1).simplify()
    logging.debug(f"{g = }")
    root_t = solve(g == 0, t, domain = QQ)
    solutions = []
    for xy in root_t:  
        t0 = xy.rhs()
        x0 = t0.numerator()
        y0 = t0.denominator()
        root = {x: x0, y: y0}
        solutions.append(root)
    end_time = time.perf_counter()
    solution_time = end_time - start_time
    logging.info(f"Finding roots within {solution_time:.3f} seconds...")
    for roots in solutions:
        yield roots[x], roots[y]