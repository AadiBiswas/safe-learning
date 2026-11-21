"""Stage 2 linear model (research/linear_identifiability.md, research/witness_geometry.md)."""

import itertools
import random
from fractions import Fraction as Fr

import pytest

from linear import (extreme_points, find_trap_1d, geometric_trap, has_multicolored_clique,
                    multicolored_clique, sigma_convex_planar, sigma_ray_bound, to_instance)
from traps import find_trap_split, is_laminar, popcount, safety_witness_number, sat_laminar, satisfiable


def rand_planar(rng, n, m):
    pts = [(Fr(rng.randint(-4, 4)), Fr(rng.randint(-4, 4))) for _ in range(n)]
    exps = []
    for _ in range(m):
        a = (Fr(rng.randint(-3, 3)), Fr(rng.randint(-3, 3)))
        b = Fr(rng.choice([a[0] * p[0] + a[1] * p[1] for p in pts]))      # equality cases
        c = (Fr(rng.randint(-3, 3)), Fr(rng.randint(-3, 3)))
        exps.append((a, b, c, Fr(rng.randint(0, 4), 2)))
    return pts, exps


def test_support_function_characterization_and_hull_invariance():
    rng = random.Random(20)
    for _ in range(60):
        pts, exps = rand_planar(rng, rng.randint(2, 6), rng.randint(1, 5))
        inst = to_instance(pts, exps)
        for K in range(1, inst.full + 1):
            assert geometric_trap(pts, exps, K) == inst.is_trap(K)
            assert inst.is_trap(K) == inst.is_trap(extreme_points(pts, K))


def test_sigma_ray_bound():
    rng = random.Random(21)
    for _ in range(60):
        pts, exps = rand_planar(rng, rng.randint(2, 6), rng.randint(1, 6))
        inst = to_instance(pts, exps)
        for K in range(1, inst.full + 1):
            assert safety_witness_number(inst, K) <= sigma_ray_bound(pts, exps, K)


def test_interior_point_needed_for_minimum_witness():
    pts = [(Fr(0), Fr(0)), (Fr(6), Fr(0)), (Fr(0), Fr(6)), (Fr(2), Fr(2))]
    e = (Fr(1), Fr(0))
    exps = [((Fr(-1), Fr(-1)), Fr(-5), e, Fr(100)), ((Fr(1), Fr(0)), Fr(3, 2), e, Fr(100)),
            ((Fr(0), Fr(1)), Fr(3, 2), e, Fr(100))]
    inst = to_instance(pts, exps)
    assert safety_witness_number(inst, inst.full) == 1
    assert safety_witness_number(inst, extreme_points(pts, inst.full)) == 3


def test_one_dimension_pairs():
    rng = random.Random(22)
    for _ in range(200):
        n = rng.randint(2, 6)
        pts = [(Fr(x),) for x in rng.sample(range(-6, 7), n)]
        exps = [((Fr(rng.choice([-2, -1, 1, 2])),), Fr(rng.randint(-6, 6)), (Fr(rng.randint(-2, 2)),),
                 Fr(rng.randint(0, 3))) for _ in range(rng.randint(1, 5))]
        inst = to_instance(pts, exps)
        assert (find_trap_1d(pts, exps) is None) == (inst.value(inst.full) is not None)


def test_convex_planar_sigma_matches_brute_force():
    rng = random.Random(23)
    for _ in range(40):
        ts = rng.sample(range(-8, 9), rng.randint(3, 8))
        pts = [(Fr(1 - t * t, 1 + t * t), Fr(2 * t, 1 + t * t)) for t in ts]
        exps = [((Fr(rng.randint(-3, 3)), Fr(rng.randint(-3, 3))), Fr(rng.randint(-3, 3), 3),
                 (Fr(0), Fr(0)), Fr(0)) for _ in range(rng.randint(1, 6))]
        inst = to_instance(pts, exps)
        for K in range(1, inst.full + 1):
            assert sigma_convex_planar(pts, exps, K) == safety_witness_number(inst, K)


@pytest.mark.parametrize("seed", [24, 25])
def test_multicolored_clique_reduction(seed):
    rng = random.Random(seed)
    for _ in range(20):
        classes = [[0, 1], [2, 3], [4]][: rng.randint(2, 3)]
        verts = [v for c in classes for v in c]
        edges = [e for e in itertools.combinations(verts, 2) if rng.random() < 0.6]
        pts, exps, _ = multicolored_clique(classes, edges)
        inst = to_instance(pts, exps)
        assert has_multicolored_clique(classes, edges) == (find_trap_split(inst) is not None)


def test_laminar_reduction():
    for nv, cl in [(1, [(1,)]), (2, [(1,), (-1,)]), (2, [(1, -2), (-1, 2)]), (2, [()]), (2, [(1, 1)])]:
        inst = sat_laminar(nv, cl)
        assert is_laminar(inst) and inst.unsafe_size() <= 2
        assert satisfiable(nv, cl) == (find_trap_split(inst) is not None)


@pytest.mark.parametrize("n", [4, 6])
def test_aligned_parabola_minimal_trap(n):
    pts = [(Fr(i), Fr(i * i)) for i in range(n)]
    exps = [((Fr(2 * k), Fr(-1)), Fr(k * k) - Fr(1, 2), (Fr(2 * k), Fr(-1)), Fr(1, 4)) for k in range(n)]
    inst = to_instance(pts, exps)
    assert inst.minimal_traps() == [inst.full] and popcount(inst.full) == n
