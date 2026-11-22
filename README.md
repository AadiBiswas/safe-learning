# safe-learning

**Can you learn without making mistakes?** This project studies the fundamental limits of information acquisition under safety constraints.

An agent learns an unknown parameter from experiments. It may only run experiments that are certified safe for every parameter still consistent with its data. Knowledge decides which experiments are allowed, and experiments decide what becomes known. The project asks when this loop allows progressive learning and when safety itself makes further learning impossible. The emphasis is on algorithm-independent statements: thresholds, characterisations, impossibility results and complexity.

## Status: Stage 3 (2026-11-23)

- **Critical dimension 2.** Exact safe identifiability with linear safety and linear bounded-error observations is polynomial in dimension 1 and coNP-complete in every fixed dimension $\ge2$. Hardness holds already with every parameter on the unit circle, laminar unsafe sets of size $\le2$ and a common noise radius.
- **Why.** Hardness needs a *lone forbidden pair*: an observation that separates exactly two hypotheses while safety stops other experiments from testing them. Geometrically that is a strictly antipodal pair, and the plane already supplies a perfect matching of them.
- **Tractable cases.** Boundedly many observation directions (XP, any dimension), boundedly many safety directions (XP), or unsafe sets of size $\le1$ (Horn).
- **Literature.** The model is the self-loop case of partial observable nondeterministic FSMs. Existing results give only upper bounds for it.

Start with `research/stage3_report.md`. Earlier stages are in `research/stage2_report.md`, `research/stage1_report.md` and `research/stage0_report.md`. The full index of results is `research/theorem_register.md`.

## Layout

- `research/`: specification, analyses, literature review, register, report
- `scripts/`: small verification scripts (`scalar.py`, `scalar_check.py`, `finite_game.py`, `traps.py`, `stage1_finite.py`, `critical_scaling.py`, `linear.py`, `stage2_checks.py`, `boolean.py`, `planar_hardness.py`, `stage3_checks.py`)
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
```

Numerical checks illustrate the proofs in `research/`; none of them is itself a proof.
