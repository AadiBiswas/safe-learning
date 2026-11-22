# safe-learning

**Can you learn without making mistakes?** This project studies the fundamental limits of information acquisition under safety constraints.

An agent learns an unknown parameter from experiments. It may only run experiments that are certified safe for every parameter still consistent with its data. Knowledge decides which experiments are allowed, and experiments decide what becomes known. The project asks when this loop allows progressive learning and when safety itself makes further learning impossible. The emphasis is on algorithm-independent statements: thresholds, characterisations, impossibility results and complexity.

## Status: Stage 4 (2026-11-21), research consolidated

- **Main theorem.** Exact safe identifiability with linear safety and linear bounded-error observations is polynomial in dimension 1, and coNP-complete in every fixed dimension $\ge2$, already on the unit circle. It survived an independent audit, with a standalone verifier (`scripts/verify_d2.py`).
- **Safety versus sensing.** With aligned safety and observation functionals, the experiment family of the hardness proof becomes polynomial (2-SAT). Alignment alone does not help in unbounded dimension.
- **Theory.** Informational traps, the safety-witness number and local-to-global principles, compact-space characterization, certified discretization and covering-number learning horizons.

Start with `research_handoff.md`, the sourcebook. Then see `research/stage4_report.md`, `research/complexity_map.md` and `research/manuscript_plan.md`. Earlier stage reports are in `research/`, and the full index of results is `research/theorem_register.md`.

## Layout

- `research/`: specification, analyses, literature review, register, report
- `scripts/`: small verification scripts (`scalar.py`, `scalar_check.py`, `finite_game.py`, `traps.py`, `stage1_finite.py`, `critical_scaling.py`, `linear.py`, `stage2_checks.py`, `boolean.py`, `planar_hardness.py`, `stage3_checks.py`, `verify_d2.py`, `stage4_checks.py`)
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
.venv/bin/python scripts/stage3_checks.py   # a few minutes
.venv/bin/python scripts/verify_d2.py
.venv/bin/python scripts/stage4_checks.py
```

Numerical checks illustrate the proofs in `research/`; none of them is itself a proof.
