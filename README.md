# safe-learning

**Can you learn without making mistakes?** This project studies the fundamental limits of information acquisition under safety constraints.

An agent learns an unknown parameter from experiments. It may only run experiments that are certified safe for every parameter still consistent with its data. Knowledge decides which experiments are allowed, and experiments decide what becomes known. The project asks when this loop allows progressive learning and when safety itself makes further learning impossible. The emphasis is on algorithm-independent statements: thresholds, characterisations, impossibility results and complexity.

## Status: Stage 1 (2026-11-21)

- **Finite spaces.** Traps characterize safe identifiability for any set-valued observations. One myopic policy is instance-optimal.
- **Minimal traps.** Their size is governed exactly by the *safety-witness number* $\sigma$. This gives a sharp local-to-global principle: identifiable iff all $k$-subsets are, exactly when minimal traps have $\sigma\le k$.
- **Complexity.** Identifiability is coNP-complete already with binary observations and experiments unsafe for at most two parameters. It is polynomial with one, polynomial without safety, and polynomial with deterministic observations (the last case is already known from FSM testing).
- **Compact spaces.** The characterization holds under a lower-semicontinuity condition on the certified-safe set. Counterexamples show that each hypothesis matters.
- **Next:** settle whether nondeterministic-FSM testing results already contain the static hardness theorem, then study fixed-dimension halfspace safety.

Start with `research/stage1_report.md`; Stage 0 is in `research/stage0_report.md`. The full index of results is `research/theorem_register.md`.

## Layout

- `research/`: specification, analyses, literature review, register, report
- `scripts/`: small verification scripts (`scalar.py`, `scalar_check.py`, `finite_game.py`, `traps.py`, `stage1_finite.py`, `critical_scaling.py`)
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
```

Numerical checks illustrate the proofs in `research/`; none of them is itself a proof.
