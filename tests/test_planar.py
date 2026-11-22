"""Stage 3: Boolean formulation, planar hardness, observation-direction XP algorithm."""

import random
from fractions import Fraction as Fr

import pytest

from boolean import clauses, find_trap_boolean, is_horn
from linear import dot, find_trap_obsdirs, to_instance
from planar_hardness import build, verify
from traps import random_instance, satisfiable


def test_boolean_matches_enumeration():
    rng = random.Random(30)
    for _ in range(150):
        inst = random_instance(rng, rng.randint(2, 6), rng.randint(1, 5), alphabet=rng.choice([2, 3]), p_unsafe=0.3)
        assert (find_trap_boolean(inst) is None) == (inst.value(inst.full) is not None)
    for _ in range(100):
        inst = random_instance(rng, rng.randint(2, 6), rng.randint(1, 5), p_unsafe=0.5, max_unsafe=1)
        assert is_horn(clauses(inst))


@pytest.mark.parametrize("nv,cl", [(1, [(1,)]), (1, [(1,), (-1,)]), (2, [()]), (2, [(1, 1, -2)]),
                                   (2, [(1, 2), (-1, 2), (1, -2), (-1, -2)]), (3, [(1, 2, 3), (-1, -2), (-3, 1)])])
def test_planar_reduction(nv, cl):
    pts, exps, meta = build(nv, cl)
    assert all(p[0] ** 2 + p[1] ** 2 == 1 for p in pts)
    assert verify(pts, exps, meta)
    inst = to_instance(pts, exps)
    assert inst.unsafe_size() <= 2
    assert satisfiable(nv, cl) == (find_trap_boolean(inst, pairwise=True) is not None)


def test_padding_and_obsdirs():
    rng = random.Random(31)
    for _ in range(60):
        d = rng.choice([1, 2])
        pts = [tuple(Fr(rng.randint(-3, 3)) for _ in range(d)) for _ in range(rng.randint(2, 6))]
        c0 = tuple(Fr(rng.randint(1, 3)) for _ in range(d))
        exps = [(tuple(Fr(rng.randint(-2, 2)) for _ in range(d)), Fr(rng.randint(-3, 3)),
                 tuple(rng.choice([1, -2]) * x for x in c0), Fr(rng.randint(0, 4), 2)) for _ in range(rng.randint(1, 5))]
        inst = to_instance(pts, exps)
        pad = lambda v: tuple(v) + (Fr(0),)  # noqa: E731
        assert to_instance([pad(p) for p in pts], [(pad(a), b, pad(c), dl) for a, b, c, dl in exps]).actions == inst.actions
        assert (find_trap_obsdirs(pts, exps) is None) == (inst.value(inst.full) is not None)


def test_touching_and_equality_cases():
    # safety at equality is safe; touching intervals are not informative
    pts = [(Fr(0),), (Fr(2),)]
    inst = to_instance(pts, [((Fr(1),), Fr(2), (Fr(1),), Fr(1))])
    assert inst.actions[0][0] == 0 and inst.is_trap(3)
    inst = to_instance(pts, [((Fr(1),), Fr(2), (Fr(1),), Fr(1) - Fr(1, 10**6))])
    assert not inst.is_trap(3)
    assert dot((Fr(1),), pts[1]) == 2
