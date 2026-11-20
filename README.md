# safe-learning

**Can you learn without making mistakes?** This project studies the fundamental limits of information acquisition under safety constraints.

An agent learns an unknown parameter from experiments. It may only run experiments that are certified safe for every parameter still consistent with its data. Knowledge decides which experiments are allowed, and experiments decide what becomes known. The project asks when this loop allows progressive learning and when safety itself makes further learning impossible. The emphasis is on algorithm-independent statements: thresholds, characterisations, impossibility results and complexity.

## Status: Stage 0 (2026-11-20)

- The preliminary scalar model is fully analysed. The thresholds are confirmed. In the uniform worst case all guaranteed learning happens in one experiment.
- In finite spaces, safe identifiability is characterised by the absence of "traps".
- Deciding safe identifiability is coNP-complete, against polynomial time without safety.
- The natural linear multidimensional model decouples into scalar problems.
- **Next:** literature on active-diagnosis complexity, then a continuum version of the trap characterisation.

Start with `research/stage0_report.md`. The full index of results is `research/theorem_register.md`.

## Layout

- `research/`: specification, analyses, literature review, register, report
- `scripts/`: small verification scripts (`scalar.py`, `scalar_check.py`, `finite_game.py`)
- `results/`: their outputs, and `ledger.md` (the experiment ledger)
- `tests/`: invariants of the proved statements

## Reproduce

```bash
python3.12 -m venv .venv && .venv/bin/pip install numpy pytest
.venv/bin/python -m pytest
.venv/bin/python scripts/scalar_check.py
.venv/bin/python scripts/finite_game.py   # a few minutes
```

Numerical checks illustrate the proofs in `research/`; none of them is itself a proof.
