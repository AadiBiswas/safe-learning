# Experiment ledger

One row per experiment. Quantities that count different things are kept in separate columns: trajectories, solver calls, search nodes. "—" means not applicable. "n.r." means not recorded.

| ID | Date | Question | Script / config | Scale | Seed | Commit | Output | Findings |
|---|---|---|---|---|---|---|---|---|
| E001 | 2026-11-20 | Check the scalar-model claims S2–S7 | `scripts/scalar_check.py` | §A: 6 bisections × 100 steps. §C: 2,000 random trajectories × 40 coupled steps (80,000). §D: 500 disturbance sequences × 30 steps. §E: 3 × 50 steps. §F: 7 runs of up to 26,464 map iterations. §G: 4 × 10⁵ iterations. | 20261120 | 5e9a078 | `results/scalar_check.txt` | All checks as predicted. Passage-time exponent −0.506; constant 2.646 (normal form gives 2.647). |
| E002 | 2026-11-20 | Trap characterisation F1, bound F2, non-locality F5, reduction F4 | `scripts/finite_game.py` | 3,000 random finite games ($\vert\Theta\vert \le 7$, $\vert\mathcal U\vert \le 5$), each solved exactly by memoised search over subsets (game-state count n.r.). 5 non-local instances ($n = 3..7$). 400 random 3-SAT instances (2–5 variables; half dense). | 20261120 | 5e9a078 | `results/finite_game.txt` | 3,000/3,000 agree with F1; F2 bound attained; minimal traps of sizes 2/3/4 seen; 30 pairwise-identifiable but non-identifiable instances; 400/400 SAT agreement (232 satisfiable). |

**Commit note.** E001 and E002 were produced by the code at commit 5e9a078. The scripts are deterministic, so rerunning them at that commit reproduces the outputs byte for byte.

**Not experiments** (no ledger rows): `tests/` (19 tests at Stage 0), and the literature searches (logged in `research/literature_review.md` §5).
