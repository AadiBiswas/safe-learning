"""Scalar model invariants (research/scalar_analysis.md)."""

import math
import random

import pytest

from scalar import lam_crit, p2_fixed_points, phi, roots, update, upper_map


@pytest.mark.parametrize("p", [1.25, 1.5, 2, 3, 7])
def test_critical_lambda_is_where_progress_appears(p):
    lc = lam_crit(p)
    assert roots(lc * (1 - 1e-9), p)  # two roots just below
    assert not roots(lc * (1 + 1e-9), p)
    vc = p / (p - 1)
    assert phi(vc, lc, p) == pytest.approx(0, abs=1e-12)


def test_p2_fixed_points_match_closed_form():
    theta, delta = 1.7, 0.05
    lam = 2 * delta * theta
    lo, hi = (v * theta for v in roots(lam, 2))
    flo, fhi = p2_fixed_points(delta, theta)
    assert lo == pytest.approx(flo, rel=1e-12) and hi == pytest.approx(fhi, rel=1e-12)
    assert 8 * delta * theta < 1


def test_basin_of_lower_fixed_point():
    lam, p = 0.2, 2
    vm, vp = roots(lam, p)
    v = vp * (1 - 1e-3)
    for _ in range(5000):
        v = upper_map(v, lam, p)
    assert v == pytest.approx(vm, rel=1e-9)
    assert upper_map(vp * 1.01, lam, p) == vp * 1.01  # above the barrier nothing moves
    assert upper_map(vm * 0.99, lam, p) == vm * 0.99


def test_worst_case_noise_pins_lower_endpoint():
    theta, delta, p = 1.3, 0.04, 2
    L, U = 0.2, 4.0
    L, U = update(L, U, theta, 1 / U, delta, delta, p)
    assert L == pytest.approx(theta) and U == pytest.approx(min(4.0, theta + 2 * delta * 16))


def test_uniform_one_shot_trap_never_shrinks():
    p, delta, L0, U0 = 2, 0.05, 0.2, 3.0
    w = min(U0 - L0, 2 * delta * U0**p)
    theta = U0 - 0.5 * w
    L, U = L0, U0
    for _ in range(30):
        x = 1 / U
        L, U = update(L, U, theta, x, U * x**p - delta - theta * x**p, delta, p)
    assert (L, U) == pytest.approx((U0 - w, U0))


def test_total_deadlock_condition_p_gt_1():
    # U0 >= (2 delta)^(-1/(p-1)) and L0 >= 0 imply 2 delta U0^p >= U0 - L0
    p, delta = 3, 0.02
    U0 = (2 * delta) ** (-1 / (p - 1))
    assert 2 * delta * U0**p >= U0 - 0.0 - 1e-12


def test_max_intensity_dominates_random_policies():
    rng = random.Random(7)
    for _ in range(200):
        p, theta, delta = rng.choice([0.5, 1, 2]), rng.uniform(0.5, 2), rng.uniform(0, 0.1)
        Lm, Um = Lp, Up = 0.1, theta * rng.uniform(1, 5)
        for _ in range(20):
            eta = rng.uniform(-delta, delta)
            xm, xp = 1 / Um, rng.uniform(1e-3, 1 / Up)
            wm, wp = 2 * delta / xm**p, 2 * delta / xp**p
            a = theta + (eta - delta) / xm**p - (wp - wm) / 2
            Lm, Um = update(Lm, Um, theta, xm, eta, delta, p)
            Lp, Up = update(Lp, Up, theta, xp, (a - theta) * xp**p + delta, delta, p)
            assert Lp <= Lm + 1e-9 and Up >= Um - 1e-9


def test_favourable_noise_identifies_in_two_steps():
    L, U = update(0.1, 5.0, 1.3, 0.2, 0.05, 0.05, 2)
    L, U = update(L, U, 1.3, 1 / U, -0.05, 0.05, 2)
    assert math.isclose(L, 1.3) and math.isclose(U, 1.3)
