"""Prop. C1: in the linear model (observe theta.u, safe iff theta.u <= 1, u >= 0) a set is a
trap iff each coordinate projection is a scalar trap: min K_i >= (1 - 2 delta) max K_i."""

import numpy as np


def coordinate_trap(K, delta):
    return bool(np.all(K.min(axis=0) >= (1 - 2 * delta) * K.max(axis=0)))


def worst_ratio(K, n_dirs, rng):
    # min_K theta.u / max_K theta.u over random u >= 0; the trap condition is ratio >= 1 - 2 delta
    U = rng.random((n_dirs, K.shape[1])) ** 3  # cubing pushes samples toward the axes too
    vals = K @ U.T
    return float((vals.min(axis=0) / vals.max(axis=0)).min())


def test_coordinate_condition_implies_trap():
    rng = np.random.default_rng(11)
    for _ in range(300):
        d = rng.integers(2, 5)
        delta = rng.uniform(0.02, 0.3)
        centre = rng.uniform(0.5, 3, d)
        # points within a box that is a coordinate trap by construction
        lo = centre * (1 - 2 * delta) ** 0.5
        K = rng.uniform(lo, centre, (rng.integers(2, 8), d))
        assert coordinate_trap(K, delta)
        assert worst_ratio(K, 2000, rng) >= 1 - 2 * delta - 1e-12


def test_failing_coordinate_is_a_witness():
    rng = np.random.default_rng(12)
    for _ in range(300):
        d = rng.integers(2, 5)
        delta = rng.uniform(0.02, 0.3)
        K = rng.uniform(0.2, 3, (rng.integers(2, 8), d))
        if coordinate_trap(K, delta):
            continue
        i = int(np.argmin(K.min(axis=0) / K.max(axis=0)))
        e = np.zeros(d)
        e[i] = 1
        vals = K @ e
        assert vals.min() < (1 - 2 * delta) * vals.max()
