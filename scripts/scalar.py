"""Scalar model: safe iff theta*x <= 1, observe theta*x^p + eta, |eta| <= delta.

Consistent sets are intervals [L, U]. Everything here is the elementary
interval bookkeeping plus the dimensionless upper-bound map
    v -> min(v, 1 + lam * v**p),   v = U/theta*,  lam = 2 delta theta*^(p-1).
See research/scalar_analysis.md for the derivations these functions check.
"""

import math


def update(L, U, theta, x, eta, delta, p):
    """One experiment at intensity x with disturbance eta. Returns the new interval."""
    if x == 0:
        return L, U
    y = theta * x**p + eta
    return max(L, (y - delta) / x**p), min(U, (y + delta) / x**p)


def upper_map(v, lam, p):
    return min(v, 1 + lam * v**p)


def phi(v, lam, p):
    # strict progress of the upper bound at v  <=>  phi(v) > 0
    return v - 1 - lam * v**p


def lam_crit(p):
    """Largest lam (p > 1) for which phi has a positive value; double root at p/(p-1)."""
    return (p - 1) ** (p - 1) / p**p


def roots(lam, p, tol=1e-15):
    """Roots of phi on (1, inf), by bisection on the monotone pieces of phi."""

    def bisect(a, b):
        fa = phi(a, lam, p)
        for _ in range(200):
            m = (a + b) / 2
            fm = phi(m, lam, p)
            if (fm > 0) == (fa > 0):
                a, fa = m, fm
            else:
                b = m
            if b - a < tol * max(1.0, a):
                break
        return (a + b) / 2

    if p == 1:
        return [1 / (1 - lam)] if lam < 1 else []
    if p < 1:
        # phi convex, phi(1) < 0, phi -> +inf: exactly one root
        hi = 2.0
        while phi(hi, lam, p) <= 0:
            hi *= 2
        return [bisect(1.0, hi)]
    vm = (lam * p) ** (-1 / (p - 1))  # argmax of phi
    if phi(vm, lam, p) <= 0:
        return []
    hi = 2 * vm
    while phi(hi, lam, p) > 0:
        hi *= 2
    return [bisect(1.0, vm), bisect(vm, hi)]


def iterate(v0, lam, p, steps):
    v = v0
    out = [v]
    for _ in range(steps):
        v = upper_map(v, lam, p)
        out.append(v)
    return out


def steps_to(v0, lam, p, target, cap=10**8):
    v, n = v0, 0
    while v > target:
        v = upper_map(v, lam, p)
        n += 1
        if n >= cap:
            return None
    return n


def p2_fixed_points(delta, theta):
    """U-coordinates of the p = 2 fixed points (1 +- sqrt(1 - 8 delta theta)) / (4 delta)."""
    disc = 1 - 8 * delta * theta
    if disc < 0:
        return []
    r = math.sqrt(disc)
    return [(1 - r) / (4 * delta), (1 + r) / (4 * delta)]
