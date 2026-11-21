"""Stage 1 finite theory (research/finite_trap_theory.md, research/complexity_analysis.md,
research/geometric_obstructions.md). Small, fast versions of scripts/stage1_finite.py."""

import random

import pytest

from traps import (binary_to_intervals, convex_trap, cycle_trap, find_trap_closure, find_trap_pairwise,
                   find_trap_split, popcount, random_instance, safety_witness_number, sat_u2, sat_u3,
                   satisfiable)


def rand(rng, **kw):
    kw.setdefault("alphabet", rng.choice([2, 3]))
    return random_instance(rng, rng.randint(2, 6), rng.randint(1, 5), **kw)


def test_characterization_and_count():
    rng = random.Random(10)
    for _ in range(400):
        inst = rand(rng)
        v = inst.value(inst.full)
        assert (v is None) == bool(inst.traps())
        assert v is None or v <= inst.n - 1


@pytest.mark.parametrize("kind", ["split", "closure", "pairwise"])
def test_polynomial_algorithms_match_exhaustive(kind):
    rng = random.Random(11)
    for _ in range(400):
        if kind == "split":
            inst, alg = rand(rng, deterministic=True), find_trap_split
        elif kind == "closure":
            inst, alg = rand(rng, max_unsafe=1, p_unsafe=0.5), find_trap_closure
        else:
            inst, alg = rand(rng, p_unsafe=0.0), find_trap_pairwise
        assert (alg(inst) is None) == (inst.value(inst.full) is not None)


def test_witness_bound():
    rng = random.Random(12)
    for _ in range(200):
        inst = rand(rng, p_unsafe=0.4)
        T = set(inst.traps())
        for K in T:
            s = safety_witness_number(inst, K)
            assert any(K2 & K == K2 and popcount(K2) <= s + 2 for K2 in T)


@pytest.mark.parametrize("red,maxU", [(sat_u3, 3), (sat_u2, 2)])
def test_reductions_including_degenerate_formulas(red, maxU):
    # repeated literals, tautologies, the empty clause, no clauses, one variable
    cases = [(1, [(1,)]), (1, [(1,), (-1,)]), (2, []), (2, [()]), (2, [(1, 1)]), (2, [(1, -1, 2)]),
             (3, [(1, 1, -2), (-1,), (2, 3)]), (3, [(1,), (-1, 2), (-2,)])]
    for nv, cl in cases:
        inst = red(nv, cl)
        assert inst.unsafe_size() <= maxU
        assert satisfiable(nv, cl) == (inst.value(inst.full) is None)


def test_binary_is_interval():
    rng = random.Random(13)
    for _ in range(200):
        inst = rand(rng, alphabet=2)
        assert set(binary_to_intervals(inst).traps()) == set(inst.traps())


@pytest.mark.parametrize("n", [3, 5, 7])
def test_large_minimal_traps(n):
    c = cycle_trap(n)
    g, _, _ = convex_trap(n)
    for inst in (c, g):
        assert inst.minimal_traps() == [inst.full]
        assert all(inst.value(K) is not None for K in range(1, inst.full) if popcount(K) >= 2)
