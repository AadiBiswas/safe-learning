# Experiment ledger

One row per experiment. Quantities that count different things are kept in separate columns: trajectories, solver calls, search nodes. "—" means not applicable. "n.r." means not recorded.

| ID | Date | Question | Script / config | Scale | Seed | Commit | Output | Findings |
|---|---|---|---|---|---|---|---|---|
| E001 | 2026-11-20 | Check the scalar-model claims S2–S7 | `scripts/scalar_check.py` | §A: 6 bisections × 100 steps. §C: 2,000 random trajectories × 40 coupled steps (80,000). §D: 500 disturbance sequences × 30 steps. §E: 3 × 50 steps. §F: 7 runs of up to 26,464 map iterations. §G: 4 × 10⁵ iterations. | 20261120 | 5e9a078 | `results/scalar_check.txt` | All checks as predicted. Passage-time exponent −0.506; constant 2.646 (normal form gives 2.647). |
| E002 | 2026-11-20 | Trap characterisation F1, bound F2, non-locality F5, reduction F4 | `scripts/finite_game.py` | 3,000 random finite games ($\vert\Theta\vert \le 7$, $\vert\mathcal U\vert \le 5$), each solved exactly by memoised search over subsets (game-state count n.r.). 5 non-local instances ($n = 3..7$). 400 random 3-SAT instances (2–5 variables; half dense). | 20261120 | 5e9a078 | `results/finite_game.txt` | 3,000/3,000 agree with F1; F2 bound attained; minimal traps of sizes 2/3/4 seen; 30 pairwise-identifiable but non-identifiable instances; 400/400 SAT agreement (232 satisfiable). |
| E003 | 2026-11-21 | Stage 1 finite theory: T1, T2, T4–T6, B1, H1, P2–P4, G1–G3 | `scripts/stage1_finite.py` | Exhaustive subset search on every instance ($\le8$ parameters; $\le12$ for the $\lvert U\rvert\le2$ reduction). §A: 4,000 + 1,500 random instances. §B–D: 3,000 each. §E: 1,500 + 2,000 + 2,000. §F: 309 formulas (degenerate cases included). §G: 1,500. §H: $n=3..8$ constructions + 2,000 random. §I: explicit counterexamples, 500 restrictions, 300 products. §J: all $2^{11}$ families on 4 points. | 20261121 | 5893d0f | `results/stage1_finite.txt` | All checks pass. A repeated-literal bitmask bug in the first encoding was caught here and fixed before the commit. Interval-realizable families: 1218/2048. |
| E004 | 2026-11-21 | Scalar fold asymptotics S4a′ | `scripts/critical_scaling.py` | $p\in\{1.5,2,3\}$; 3 (start, target) pairs; $\epsilon=10^{-3},10^{-5},10^{-7}$; map iterations n.r. (at most about $1.3\times10^4$ per run). | — (deterministic) | 9cfb03f | `results/critical_scaling.txt` | $\sqrt\epsilon N$ within 0.1% of the prediction at $\epsilon=10^{-7}$; relaxation rate to 4 digits. |
| E005 | 2026-11-21 | Stage 2: linear model L1–L9, witness geometry W1–W4, approximate witnesses A1–A2, net perturbations CandA/CandB | `scripts/stage2_checks.py` | §A: 48,520 subsets over 1,320 random instances ($d=1,2,3$; generic, collinear, repeated, rational-circle points; equality and touching cases; $a=0$, $c=0$, $\delta=0$). §B: 1,200 planar instances, all subsets. §C: 600 instances, all subsets. §D: explicit. §E: 1,500. §F: 12,647 (instance, subset) pairs. §G: 150 graphs. §H: 63 formulas ($\le14$ parameters). §I: 1,500 aligned instances + parabola $n=3..8$. §J: 300 random sets × 50 directions (floats) + circle with 1,439 rational points at 3 margins. §K: 33,056 (set, subnet) pairs. | 20261122 | b59b708 | `results/stage2_checks.txt` | All checks pass after fixing three bugs in the checks themselves (a wrong halfplane in §D, indices used as coordinates in the 1-D routine, half-circle sampling in §J). Only 2 minimal traps of size ≥3 arose in §B, so the evidence for L3 is the proof. |
| E006 | 2026-11-21 | Stage 3: Boolean formulation B1, planar reduction D2, padding/block sums D1/R3, observation-direction XP D5, lone-pair lemma R1 | `scripts/stage3_checks.py` | §A: 600 set-valued + 600 linear instances ($d\le3$) + 300 Horn checks. §B: 58 formulas (8 degenerate + 50 random, 1–3 variables, sparse and dense), up to 138 parameters, exact geometry for every experiment. §C: 200 padding + 200 block-sum instances. §D: 300 ($k=1$) + 120 ($k=2$) instances. §E: 300 configurations × 20 directions × all critical thresholds (3,582 one-edge relations). | 20261123 | 8407d20 | `results/stage3_checks.txt` | All checks pass. A generator bug was found while building §D: per-component random rescaling produced new directions instead of rescaled ones. It was fixed here, and the same idiom affects E005 (see the note below). |
| E007 | 2026-11-21 | Independent verification of the planar reduction D2 (structure, margins, encoding) | `scripts/verify_d2.py` | 48 formulas (8 degenerate + 40 random, $n\le6$, $m\le24$), up to 176 parameters and 184 experiments, every experiment checked exactly. No satisfiability solving. | 20261124 | 8402eb6 | `results/verify_d2.txt` | All pass after one fix found by the verifier (constant safety was tight at equality; now $0\le1$). Max bits per number $\le5.14\log_2N$. |
| E008 | 2026-11-21 | Aligned model AL1–AL3; W5′ | `scripts/stage4_checks.py` | §A: 400 configurations × ≤15 directions × all thresholds (19,049 lone-pair cases). §B: 600 aligned instances vs exhaustive. §C: 47 formulas (aligned 3-SAT encoding). §D: 200 random graphs (moment curve, vertex cover). | 20261124 | 0fcc906 | `results/stage4_checks.txt` | All pass. |

**Commit note.** E001 and E002 were produced by the code at commit 5e9a078; E003 at 5893d0f; E004 at 9cfb03f; E005 at b59b708; E006 at 8407d20 (rerun unchanged at 8402eb6 after the D2 margin fix); E007 at 8402eb6; E008 at 0fcc906. The scripts are deterministic, so rerunning them at that commit reproduces the outputs byte for byte.

**Not experiments** (no ledger rows): `tests/` (19 tests at Stage 0, 30 at Stage 1, 40 at Stage 2, 49 at Stage 3, 51 at Stage 4), and the literature searches (logged in `research/literature_review.md` §5).

**Audit note (Stage 3) on E005 §C.** The generator `random_exps(..., rays=...)` rescaled each *component* of a ray by its own random factor. So the safety normals were not restricted to 1–3 rays, and the description "random instances with 1–3 rays" in E005 was inaccurate. The check itself compares $\sigma(K)$ with the ray count $r(K)$ *of the normals actually generated*, so its conclusion (σ ≤ r on every subset) is unaffected. E005's output is left unchanged as a historical record.

## Computational inventory (Stages 0–4)

Incomparable quantities are kept apart. Every count below is a recorded, completed trial from E001–E008. Developmental runs during debugging were not recorded and are not counted.

| Kind | Count | Where |
|---|---|---|
| Boolean formulas checked through a reduction, with SAT ⇔ trap decided | 400 (E002) + 309 and 146 (E003, two reductions on one formula list) + 63 (E005 §H) + 58 (E006 §B) + 47 (E008 §C) | reductions F4/H1(b), H1(a), L6, D2, AL3 |
| Formulas checked for D2's geometry only | 58 (E006 §B) + 48 (E007) | D2 |
| Graph instances through a reduction | 150 multicolored-clique graphs (E005 §G); 200 vertex-cover graphs (E008 §D) | L7(b), W5′ |
| Random finite instances solved exhaustively (game value or full trap enumeration) | E002: 3,000. E003: §A 5,500, §B 6,000, §C 3,000, §D 3,000, §E 5,500, §G 1,500, §H 2,000, §I 800. E005: §B 1,200, §C 600, §E 1,500, §I 1,500. E006: §A 1,200, §C 400, §D 420. E008: §B 600. | — |
| Subset-level comparisons | E005 §A: 48,520 subsets; §F: 12,647 (instance, subset) pairs; §K: 33,056 (set, subnet) pairs | L1, W4(b), CandA/B |
| Trap families enumerated | all $2^{11}$ on 4 points (E003 §J) | T6, G2b |
| Geometric relation cases | 3,582 one-edge relations (E006 §E); 19,049 aligned lone-pair cases (E008 §A) | R1, AL1 |
| Scalar and continuum numerics | E001 (scalar claims; 80,000 coupled steps in §C); E004 (27 fold-asymptotic runs); E005 §J (300 float sets × 50 directions; 3 exact circle margins) | S2–S7, S4a′, A1–A2 |
| Automated tests | 51 (`tests/`) | — |

**Reproducibility.**
- Every script listed above is deterministic, with a fixed seed or none. Outputs contain no wall-clock timings; one was removed from E006 in Stage 3.
- In Stage 4 these were re-run, with byte-identical outputs: `scalar_check`, `critical_scaling`, `stage1_finite`, `stage2_checks`, `stage3_checks`.
- `finite_game` (E002, a few minutes) was not re-run in Stage 4.
- **Remaining concerns:**
  - E005 §C's generator defect (above);
  - E005 §J uses floating point for the sampling bound. The accompanying proof is exact.
