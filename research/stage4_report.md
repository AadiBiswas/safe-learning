# Stage 4 report — Separation of safety and sensing, final audit, consolidation

*2026-11-24. Details:*
- `research/aligned_identifiability.md`
- `research/planar_hardness_audit.md`
- `research/complexity_map.md`
- `research/mathematical_audit.md`
- `research/manuscript_plan.md`
- `research_handoff.md` (the sourcebook)

*Computations: ledger E007, E008.*

## Answers to the seven questions

1. **Does alignment restore tractability in the D2 family? Yes.**
   - Lemma AL1: an aligned *global* lone pair always meets any nonempty unsafe set.
   - So in the exact D2 experiment family — global conflicts complete or one pair, unsafe sets of size $\le2$ — aligned safety and sensing reduce trap existence to 2-SAT with two forced ones (AL2): $O(n^2(n+m))$, in every dimension and for every tolerance.
   - D2 proves the same family coNP-complete with independent directions. So **within that family, hardness requires safety and sensing to use different functionals.**
2. **A broader aligned classification? Partly.**
   - Alignment alone does not remove hardness when the dimension is unbounded (AL3). An aligned direction can still produce an *effective* lone pair: second-from-top against bottom, below an unsafe cap. Only effective conflicts matter (B1).
   - In the plane, such aligned implications are cyclically local (AL4). The aligned fixed-dimension case remains open (AL-O1), with a bounded-width sketch only.
   - The orthogonal case is open (OR-O1).
3. **Does D2 survive an independent audit? Yes.**
   - **What was reconstructed from definitions:** both implications, with no assumption that traps contain the helpers or represent consistent assignments; the exact rational realization; strict margins; polynomial encoding; the precise NP/coNP and ETH statements; and the $\varepsilon<1$ extension via $\sqrt{306}/17$.
   - **The independent verifier** checked 48 formulas, up to 176 parameters, and found one defect: constant "always safe" experiments were tight at equality. It is now $0\le1$, with no unsafe set changed.
   - **Distinctness of projections**, previously checked only numerically, is now proved analytically for every formula.
4. **Are the complexity claims precise? Yes**, after the corrections in `complexity_map.md`:
   - W[1]-hardness concerns TRAP; SAFEID is the complement, and no exponent optimality is claimed;
   - D5 is XP, and its FPT status is open;
   - ETH gives no $2^{o(N)}$ or $2^{o(m)}$ algorithm, and no $2^{o(L/\log L)}$ in bit length $L$.
5. **Are the structural and continuum results consistent and rigorous? Yes.**
   - `mathematical_audit.md` re-derives every area, checks each counterexample against exactly the hypotheses it isolates, and confirms the meaning and constants of the packing horizon.
   - No proved theorem was false. Corrections C1–C6 are presentational or strengthening.
6. **Strongest defensible original contributions:**
   1. **The complexity map of static safe identification.** It has three parts:
      - coNP-completeness under ambiguous observations, against the known polynomial deterministic case;
      - the unsafe-size 1/2 transition;
      - **the dimensional dichotomy:** P at $d=1$, coNP-complete for every fixed $d\ge2$ on the unit circle, refined by alignment.
   2. **The structural theory:** traps, $\sigma(K)=\lvert K\rvert$ for minimal traps, and the exact local-to-global principle.
   3. **The compact-space characterization under (L)**, with its counterexamples, certified discretization and covering-number horizons.

   The model itself is the self-loop case of partial observable nondeterministic FSMs. That is acknowledged throughout, and is not claimed as new.
7. **Ready for manuscript preparation? Yes.**
   - No principal theorem depends on an unverified citation.
   - The remaining open problems (AL-O1, OR-O1, D-O1, D-O2) are refinements, and would not change the main theorem.

## Corrections made in Stage 4

| # | Item | Correction |
|---|---|---|
| C1 | D2 constant safety | Strict margin: $b=1$. |
| C2 | D2 experiment count | Sharpened to $\le5n+11m$. |
| C3 | "Hardness needs a lone forbidden pair" | Restated as a property of all known reductions. The general claim is open (D-O2). |
| C4 | W5 | Added W5′: σ is NP-hard in $\mathbb Q^4$, by a self-contained proof (vertex cover on moment-curve pairs, verified on 200 graphs). The principal results no longer touch Johnson 1982. |

## Primary-source status

- **Johnson 1982:** not obtained. Only W5 ($d=3$) depends on it.
- **The sharp coreset exponent:** confirmed only from secondary sources (Mount et al.; the survey arXiv:2512.02379). It is used only as a remark.
- **Bronshtein's 2007 survey** is the recommended alternative primary source.

## Final classification

See `research/complexity_map.md` §2. It has 23 rows, with hypotheses, references and literature status for each.

## Verification

- **E007** (`verify_d2.py`): 48 formulas, exact structural verification.
- **E008** (`stage4_checks.py`):
  - AL1: 19,049 cases;
  - AL2: 600 instances against exhaustive search;
  - AL3: 47 formulas;
  - W5′: 200 graphs.
- **Reproducibility:** the Stage 0–3 outputs were re-run where feasible, and reproduced byte for byte.
- **Inventory:** `results/ledger.md`.
- **Tests:** 51, all passing.

## Recommendation

**Conclude substantive research and begin manuscript preparation**, following `research/manuscript_plan.md`. Before submission:
1. run a final novelty search (geometric CSP, adaptive testing with forbidden tests);
2. consult Bronshtein's 2007 survey;
3. optionally attempt AL-O1 in the plane, if a reviewer-facing statement "alignment is tractable in the plane" is wanted.
