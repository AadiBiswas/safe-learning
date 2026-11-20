"""Finite safe-identification game (research/finite_analysis.md)."""

import random

from finite_game import nonlocal_example, random_game, sat_game, satisfiable


def test_trap_characterization_on_random_instances():
    rng = random.Random(1)
    for _ in range(300):
        g = random_game(rng)
        K0 = (1 << g.n) - 1
        assert (g.win(K0) is None) == bool(g.traps(K0))


def test_experiment_count_bound():
    rng = random.Random(2)
    for _ in range(300):
        g = random_game(rng)
        r = g.win((1 << g.n) - 1)
        if r is not None:
            assert r <= g.n - 1


def test_nonlocal_trap():
    g = nonlocal_example(5)
    K0 = (1 << 5) - 1
    assert g.win(K0) is None
    assert g.traps(K0) == [K0]
    for K in range(1, K0):
        if bin(K).count("1") >= 2:
            assert g.win(K) == 1


def test_sat_reduction():
    rng = random.Random(3)
    seen = set()
    for _ in range(60):
        nv = rng.randint(2, 4)
        cl = [tuple(rng.choice([-1, 1]) * v for v in rng.sample(range(1, nv + 1), min(3, nv)))
              for _ in range(rng.randint(1, 8 * nv))]
        g = sat_game(nv, cl)
        s = satisfiable(nv, cl)
        seen.add(s)
        assert s == bool(g.traps((1 << g.n) - 1))
    assert seen == {True, False}


def test_unconstrained_identifiability_is_pairwise():
    # F3: with every action always safe, a trap exists iff a far pair is never separated
    rng = random.Random(4)
    for _ in range(200):
        g = random_game(rng)
        g.safe = [[True] * g.m for _ in range(g.n)]
        g.win.cache_clear()
        K0 = (1 << g.n) - 1
        far_pairs = [(1 << i) | (1 << j) for i in range(g.n) for j in range(i + 1, g.n)
                     if abs(g.points[i] - g.points[j]) > g.eps]
        assert (g.win(K0) is None) == any(g.self_preserving(P) for P in far_pairs)
