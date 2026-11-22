"""Boolean form of trap existence (research/boolean_trap_formulation.md).

For an Instance of scripts/traps.py, x_i = [theta_i in K]. Experiment u contributes, for
every inclusion-minimal set F with empty common observation (a "conflict" of u),
the clause  OR_{i in F} not x_i  OR  OR_{k in U(u)} x_k.  A trap of size >= 2 is a
satisfying assignment with at least two ones. With interval (or deterministic)
observations every conflict is a pair (1-D Helly), which is the form used in the theory.

The solver is a small DPLL, deliberately dependency-free; it is exact, not fast.
"""

import itertools

from traps import members, popcount


def conflicts(inst, u):
    """Minimal sets F of parameters with no observation common to all of F."""
    _, R = inst.actions[u]
    n = inst.n

    def common(F):
        return any(F & r == F for r in R)

    out = []
    for size in range(2, n + 1):
        for c in itertools.combinations(range(n), size):
            F = sum(1 << i for i in c)
            if not common(F) and not any(G & F == G for G in out):
                out.append(F)
    return out


def pair_conflicts(inst, u):
    """Separated pairs only: the complete conflict set when observations have Helly number 2."""
    _, R = inst.actions[u]
    return [1 << i | 1 << j for i, j in itertools.combinations(range(inst.n), 2)
            if not any((r >> i & 1) and (r >> j & 1) for r in R)]


def clauses(inst, pairwise=False):
    """List of (neg_mask, pos_mask): satisfied unless every neg is 1 and every pos is 0."""
    out = set()
    for u, (U, _) in enumerate(inst.actions):
        Fs = [F for F in (pair_conflicts(inst, u) if pairwise else conflicts(inst, u)) if not F & U]
        outside = inst.n - popcount(U)
        if pairwise and len(Fs) == outside * (outside - 1) // 2:
            # every pair outside U conflicts: given |K| >= 2 this is just "K meets U"
            out.add((0, U))
            continue
        out.update((F, U) for F in Fs)      # a conflict meeting the unsafe set is never active
    return sorted(out)


def solve(n, cls, forced=0, at_least=0):
    """DPLL with unit propagation. Returns a satisfying bitmask containing `forced` and
    with at least `at_least` ones, or None."""
    def go(one, zero):
        changed = True
        while changed:
            changed = False
            for neg, pos in cls:
                if neg & zero or pos & one:
                    continue
                free_neg, free_pos = neg & ~one, pos & ~zero
                if not free_neg and not free_pos:
                    return None
                if popcount(free_neg) + popcount(free_pos) == 1:
                    if free_neg:
                        zero |= free_neg
                    else:
                        one |= free_pos
                    changed = True
        free = ((1 << n) - 1) & ~(one | zero)
        if popcount(one) + popcount(free) < at_least:
            return None
        if not free:
            return one
        i = next(members(free))
        return go(one | 1 << i, zero) or go(one, zero | 1 << i)
    return go(forced, 0)


def find_trap_boolean(inst, pairwise=False):
    """A trap of size >= 2 (eps = 0), by one DPLL search with the cardinality bound built in."""
    return solve(inst.n, clauses(inst, pairwise), at_least=2)


def is_horn(cls):
    return all(popcount(pos) <= 1 for _, pos in cls)
