"""Stage 4: aligned safety and sensing (research/aligned_identifiability.md)."""

import random

from boolean import find_trap_boolean
from linear import aligned, aligned_2sat_trap, aligned_sat_u2, to_instance
from stage4_checks import aligned_family_instance
from traps import satisfiable


def test_aligned_2sat_matches_exhaustive():
    rng = random.Random(40)
    tot = 0
    while tot < 150:
        r = aligned_family_instance(rng, rng.randint(2, 6), rng.randint(1, 6), rng.choice([1, 2]))
        if r is None:
            continue
        pts, exps = r
        inst = to_instance(pts, exps)
        assert (aligned_2sat_trap(pts, exps) is None) == (inst.value(inst.full) is not None)
        tot += 1


def test_aligned_hardness_construction():
    for nv, cl in [(1, [(1,)]), (1, [(1,), (-1,)]), (2, [()]), (2, [(1, -2), (-1, 2)]), (2, [(1, 1, -2)])]:
        pts, exps = aligned_sat_u2(nv, cl)
        assert aligned(exps)
        inst = to_instance(pts, exps)
        assert inst.unsafe_size() <= 2
        assert satisfiable(nv, cl) == (find_trap_boolean(inst, pairwise=True) is not None)
