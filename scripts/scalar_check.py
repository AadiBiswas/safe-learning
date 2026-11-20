"""Numerical checks of research/scalar_analysis.md. Not proofs.

    .venv/bin/python scripts/scalar_check.py   ->  results/scalar_check.txt
"""

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from scalar import lam_crit, p2_fixed_points, phi, roots, steps_to, update, upper_map  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "scalar_check.txt"
SEED = 20261120
lines = []


def log(s=""):
    print(s)
    lines.append(s)


# A. critical lam: bisect on lam for the appearance of positive phi
log("A. critical lambda (p > 1): numeric threshold vs (p-1)^(p-1)/p^p")
for p in (1.25, 1.5, 2, 3, 5, 10):
    lo, hi = 0.0, 1.0
    for _ in range(100):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if roots(m, p) else (lo, m)
    log(f"  p={p:<5} numeric={lo:.15f}  formula={lam_crit(p):.15f}  diff={abs(lo - lam_crit(p)):.1e}")

# B. p = 2 fixed points in U coordinates
log("\nB. p = 2 fixed points: roots*theta vs (1 +- sqrt(1-8 delta theta))/(4 delta)")
worst = 0.0
for theta in (0.5, 1.0, 3.0):
    for delta in (0.01, 0.03, 0.1 / theta):
        lam = 2 * delta * theta
        r = [v * theta for v in roots(lam, 2)]
        f = p2_fixed_points(delta, theta)
        if r:
            worst = max(worst, max(abs(a - b) / b for a, b in zip(r, f)))
log(f"  max relative difference over 9 cases: {worst:.1e}")

# C. domination of max intensity: an adversary facing any policy keeps a superset
#    of the max-intensity consistent set (the coupling used in the proof).
log("\nC. coupling: any policy's consistent set contains the max-intensity one")
rng = random.Random(SEED)
violations = trials = 0
for _ in range(2000):
    p = rng.choice([0.5, 1.0, 1.5, 2.0, 3.0])
    theta = rng.uniform(0.2, 3.0)
    L0, U0 = theta * rng.uniform(0.1, 1.0), theta * rng.uniform(1.0, 6.0)
    delta = rng.uniform(0.0, 0.2)
    Lm, Um, Lp, Up = L0, U0, L0, U0
    for _ in range(40):
        eta_m = rng.uniform(-delta, delta)  # arbitrary adversary against max intensity
        xm = 1 / Um
        xp = rng.uniform(0, 1 / Up)  # arbitrary safe choice for the other policy
        wm, wp = 2 * delta / xm**p, (2 * delta / xp**p if xp > 0 else math.inf)
        # interval for max policy: [theta + (eta_m - delta)/xm^p, ... + w_m]
        a_m = theta + (eta_m - delta) / xm**p
        # centre the wider window on the narrower one; it then contains theta, so eta_p is admissible
        if xp > 0:
            a_p = a_m - (wp - wm) / 2
            eta_p = (a_p - theta) * xp**p + delta
            assert -delta * (1 + 1e-12) <= eta_p <= delta * (1 + 1e-12)
        Lm, Um = update(Lm, Um, theta, xm, eta_m, delta, p)
        if xp > 0:
            Lp, Up = update(Lp, Up, theta, xp, eta_p, delta, p)
        trials += 1
        if Lp > Lm + 1e-9 * Um or Up < Um - 1e-9 * Um:
            violations += 1
log(f"  {trials} steps, inclusion violations: {violations}")

# D. eta = +delta maximises the upper bound under max intensity
log("\nD. eta = +delta gives the largest U_T among random disturbance sequences")
bad = 0
for _ in range(500):
    p = rng.choice([0.5, 1.0, 2.0, 3.0])
    theta, delta = rng.uniform(0.5, 2), rng.uniform(0, 0.1)
    U0 = theta * rng.uniform(1, 4)
    Lw, Uw = 0.0, U0
    Lr, Ur = 0.0, U0
    for _ in range(30):
        Lw, Uw = update(Lw, Uw, theta, 1 / Uw, delta, delta, p)
        Lr, Ur = update(Lr, Ur, theta, 1 / Ur, rng.uniform(-delta, delta), delta, p)
    bad += Ur > Uw * (1 + 1e-12)
    assert abs(Lw - theta) < 1e-9 * theta  # lower end pinned at theta after one step
log(f"  random sequences beating eta = +delta: {bad} / 500; lower endpoint pinned at theta*: yes")

# E. uniform worst case: theta* in the top window keeps [U0 - w, U0] forever
log("\nE. uniform trap: theta* in [U0 - 2 delta U0^p, U0], common observation every step")
for p, delta, U0, L0 in [(2, 0.05, 3.0, 0.2), (0.5, 0.2, 4.0, 0.1), (1, 0.1, 2.0, 0.5)]:
    w = min(U0 - L0, 2 * delta * U0**p)
    theta = U0 - 0.37 * w
    L, U = L0, U0
    for _ in range(50):
        x = 1 / U
        y = U * x**p - delta  # in the common intersection of [t x^p - d, t x^p + d], t in [U - w, U]
        L, U = update(L, U, theta, x, y - theta * x**p, delta, p)
    log(f"  p={p}: predicted diameter {w:.6f}, after 50 steps [{L:.6f}, {U:.6f}] -> {U - L:.6f}")

# F. dynamics: basins and critical slowing down (p = 2)
log("\nF. p = 2 basins and passage time from v_c = p/(p-1) near lam_c")
p = 2
lc = lam_crit(p)
for lam in (0.2, 0.24):
    vm, vp = roots(lam, p)
    a = upper_map(vp * (1 - 1e-6), lam, p) < vp * (1 - 1e-6)
    b = upper_map(vp * (1 + 1e-6), lam, p) == vp * (1 + 1e-6)
    log(f"  lam={lam}: v- = {vm:.6f}, v+ = {vp:.6f}; just below v+ moves: {a}; just above v+ stuck: {b}")
pts = []
for k in range(2, 9):
    gap = 10.0**-k
    lam = lc - gap
    vm, _ = roots(lam, p)
    vc = p / (p - 1)
    n = steps_to(vc, lam, p, vm + 0.01 * (vc - vm))
    pts.append((gap, n))
    log(f"  lam_c - lam = 1e-{k}: steps = {n}, steps * sqrt(gap) = {n * math.sqrt(gap):.3f}")
x = [math.log(g) for g, _ in pts]
y = [math.log(n) for _, n in pts]
mx, my = sum(x) / len(x), sum(y) / len(y)
slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
log(f"  fitted exponent of steps vs (lam_c - lam): {slope:.4f} (saddle-node prediction -0.5)")
log(f"  at lam = lam_c: max phi over a fine grid = {max(phi(1 + i * 1e-4, lc, p) for i in range(1, 50000)):.2e} (<= 0)")

# G. p = 1 and p < 1
log("\nG. p <= 1")
for p, lam in [(1, 0.5), (1, 1.0), (0.5, 2.0), (0.5, 20.0)]:
    r = roots(lam, p)
    v = 1e3
    for _ in range(10**5):
        v = upper_map(v, lam, p)
    log(f"  p={p}, lam={lam}: roots {[round(t, 6) for t in r]}, v after 1e5 steps from 1e3: {v:.6f}")

# H. favourable noise identifies exactly in two experiments
log("\nH. favourable disturbances (+delta then -delta) identify theta* exactly")
L, U = update(0.1, 5.0, 1.3, 1 / 5.0, 0.05, 0.05, 2)
L, U = update(L, U, 1.3, 1 / U, -0.05, 0.05, 2)
log(f"  [L, U] = [{L:.12f}, {U:.12f}] for theta* = 1.3")

OUT.parent.mkdir(exist_ok=True)
OUT.write_text("\n".join(lines) + "\n")
