# safe-learning

**Can you learn without making mistakes?** This project studies the fundamental limits of information acquisition under safety constraints.

An agent learns an unknown parameter from experiments. It may only run experiments that are certified safe for every parameter still consistent with its data. Knowledge decides which experiments are allowed, and experiments decide what becomes known. The project asks when this loop allows progressive learning and when safety itself makes further learning impossible. The emphasis is on algorithm-independent statements: thresholds, characterisations, impossibility results and complexity.

## Status: Stage 2 (2026-11-22)

- **Literature.** The static safe model is exactly the self-loop case of observable partial nondeterministic FSMs. Their published hardness (Türker et al. 2023) concerns forest size and uses dynamics, so it does not cover this problem.
- **Linear models.** Traps are support-function objects determined by the convex hull, and minimal traps are in convex position.
  - Identifiability is NP-complete in unbounded dimension, even with convex position, a common noise radius and laminar size-2 unsafe sets.
  - It is W[1]-hard in the number of safety directions (XP algorithm $O(n^{r+2}m)$).
  - It is polynomial in one dimension. Fixed dimension $\ge2$ is open, with the obstruction identified.
- **Safety-witness number.** $\sigma\le$ the number of safety rays. Computing $\sigma$ is polynomial in the plane and NP-hard in space.
- **Continuum.** Approximate witnesses give sound, conditionally complete net certificates, and explicit covering-number learning horizons under an informativeness margin. No margin-free bound exists.

Start with `research/stage2_report.md`; earlier stages are in `research/stage1_report.md` and `research/stage0_report.md`. The full index of results is `research/theorem_register.md`.

## Layout

- `research/`: specification, analyses, literature review, register, report
- `scripts/`: small verification scripts (`scalar.py`, `scalar_check.py`, `finite_game.py`, `traps.py`, `stage1_finite.py`, `critical_scaling.py`, `linear.py`, `stage2_checks.py`)
- `results/`: their outputs, and `ledger.md` (the experiment ledger)
- `tests/`: invariants of the proved statements

## Reproduce

```bash
python3.12 -m venv .venv && .venv/bin/pip install numpy pytest
.venv/bin/python -m pytest
.venv/bin/python scripts/scalar_check.py
.venv/bin/python scripts/finite_game.py   # a few minutes
.venv/bin/python scripts/stage1_finite.py   # seconds
.venv/bin/python scripts/critical_scaling.py
.venv/bin/python scripts/stage2_checks.py   # about a minute
```

Numerical checks illustrate the proofs in `research/`; none of them is itself a proof.
