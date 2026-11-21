"""Audit of the scalar critical slowing-down claim (S4a; research/scalar_analysis.md §6a).
Ledger E004.

    .venv/bin/python scripts/critical_scaling.py   ->  results/critical_scaling.txt

Map v -> min(v, 1 + lam v^p), eps = lam_c - lam. Normal form at the fold
(v_c = p/(p-1)): z' = z + a z^2 - b eps with a = p(p-1) lam_c v_c^(p-2)/2, b = v_c^p,
so the passage time from v_c + rho (v_+ - v_c) to v_c + s (v_- - v_c) is
    N ~ (artanh rho + artanh s) / sqrt(a b eps),
and the linear rate at v_- is 1 - 2 sqrt(a b eps) + O(eps). Numerics, not proof.
"""

import math
from pathlib import Path

from scalar import lam_crit, roots, upper_map

OUT = Path(__file__).resolve().parents[1] / "results" / "critical_scaling.txt"


def ab(p):
    lc, vc = lam_crit(p), p / (p - 1)
    return p * (p - 1) * lc * vc ** (p - 2) / 2 * vc**p


def passage(p, eps, rho, s):
    lam = lam_crit(p) - eps
    vm, vp = roots(lam, p)
    vc = p / (p - 1)
    v, target, n = vc + rho * (vp - vc), vc + s * (vm - vc), 0
    while v > target:
        v = upper_map(v, lam, p)
        n += 1
    return n, vm, lam


def main():
    lines = ["Passage time N through the fold, scaled by sqrt(eps); prediction (artanh rho + artanh s)/sqrt(ab).",
             "rate = (1 - g'(v_-)) / sqrt(eps), prediction 2 sqrt(ab).", ""]
    for p in (1.5, 2.0, 3.0):
        c = math.sqrt(ab(p))
        lines.append(f"p = {p}: sqrt(ab) = {c:.6f}")
        for rho, s in ((0.0, 0.5), (0.0, 0.99), (0.9, 0.5)):
            pred = (math.atanh(rho) + math.atanh(s)) / c
            row = []
            for k in (3, 5, 7):
                eps = 10.0**-k
                n, _, _ = passage(p, eps, rho, s)
                row.append(f"1e-{k}: {n * math.sqrt(eps):.4f}")
            lines.append(f"  rho = {rho}, s = {s}: predicted {pred:.4f}; observed " + ", ".join(row))
        row = []
        for k in (3, 5, 7):
            eps = 10.0**-k
            _, vm, lam = passage(p, eps, 0.0, 0.5)
            gp = lam * p * vm ** (p - 1)
            row.append(f"1e-{k}: {(1 - gp) / math.sqrt(eps):.4f}")
        lines.append(f"  rate: predicted {2 * c:.4f}; observed " + ", ".join(row))
    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
