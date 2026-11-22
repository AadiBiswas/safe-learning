# Stage 3 report — The critical dimension of safe learning

*2026-11-23. This is a self-contained handoff. Details are in `research/fixed_dimension_complexity.md` (principal), `research/boolean_trap_formulation.md` and `research/geometric_realizations.md`. Every ID is in `research/theorem_register.md`, and the computations are ledger E006.*

## 1. Result in one sentence

**Exact safe identifiability with linear safety constraints and linear bounded-error observations is polynomial-time decidable in dimension 1 and coNP-complete in every fixed dimension $d\ge2$. Hardness holds already when every parameter lies on the unit circle.**

The critical dimension is therefore exactly 2. This is a complete dimensional dichotomy for the linear model, with explicit rational encodings.

## 2. Answers to the seven questions

1. **Does the Boolean formulation give new insight?** Yes, as a dictionary rather than new Boolean theory.
   - Trap existence is satisfiability of clauses $(\bigvee_{F}\neg x\vee\bigvee_{B_u}x)$, one per experiment and minimal conflict $F$, plus "at least two ones" (B1).
   - Unsafe sets of size $\le1$ give Horn clauses, hence P. Size 2 gives Schaefer-hard languages (B2, B3).
   - Clause shapes do not determine complexity. Deterministic observations produce the same shapes but only complete-multipartite conflicts, and are polynomial. **Every known hardness construction uses a lone forbidden pair** (B4), and the realization theory identifies that geometrically as a strictly antipodal pair (R1). *(Stage 4 audit: this is a property of the constructions, not a theorem that every hard observation family must contain lone pairs; D-O2 is open.)*
2. **Is fixed-dimensional coNP-completeness provable?** Yes, in $\mathbb Q^2$ (D2), hence in every $\mathbb Q^d$ with $d\ge2$ (D1).
3. **Smallest dimension with hardness:** 2. This is tight, because $d=1$ is polynomial (L5).
4. **Is the planar model polynomial?** Not unless P $=$ NP, even in strict convex position, with laminar unsafe sets of size $\le2$ and a common noise radius. It is polynomial or XP under:
   - one or boundedly many observation directions (D5, $O(n^{2k+1}m)$);
   - boundedly many safety directions (L7);
   - unsafe sets of size $\le1$ (P3).
5. **Can the earlier incompatibilities be characterized?** Yes.
   - A lone forbidden pair is realizable iff the pair is strictly antipodal (R1).
   - A planar configuration has at most $n$ such pairs (R5(c), cited).
   - Halfplane traces in convex position are arcs.
   - The Stage 2 reductions failed because they demanded clause traces through literal points and negations between literal clusters. Both requirements are artefacts of the encoding (D6).
6. **What governs joint realizability?** The compatibility, on a single configuration, of:
   - the **trace hypergraph** of the safety halfspaces;
   - the **strict antipodality graph** of the observation side.

   On an antipodally symmetric circle these are independent: adjacency of upper points versus antipodal matching. That is exactly what hardness needs (R6). Fixed-dimensional observation alphabets are polynomially bounded (R2). Block sums combine separate realizations, for exact identification only (R3).
7. **Is this a contribution beyond the literature?** Probably yes; see §6. The model itself is not new: it is the self-loop case of partial observable nondeterministic FSMs. The new content is:
   - the coNP-completeness at the critical dimension 2;
   - the polynomial cases;
   - the structural explanation via lone antipodal pairs.

## 3. The planar construction (D2)

**From a 3-SAT formula** with $n$ variables and $m$ clauses, $6n+10m$ parameters are placed on the unit circle at rational points $\pm v(k)$, $v(k)=\bigl(\tfrac{1-k^2}{1+k^2},\tfrac{2k}{1+k^2}\bigr)$:
- literal points $T_v,F_v$;
- primed copies $T'_v,F'_v$;
- per clause, selectors $s_j,s'_j$ and private literal copies $\kappa_{j1},\kappa_{j2},\kappa_{j3}$;
- one helper per antecedent, placed at the antipode of its antecedent.

**Four experiment types** make up the gadgets:

| Gadget | Unsafe set | Observation | Constraint on traps |
|---|---|---|---|
| force$(w)$ | $\{w\}$ | separates all pairs | $w\in K$ |
| imply$(x\to V)$ | $V$ | separates only $\{x,w_x\}$ | $x\Rightarrow K\cap V\ne\varnothing$ |
| notboth$(T',F')$ | $\varnothing$ | separates only $\{T',F'\}$ | $\neg(T'\wedge F')$ |
| some$(s,s')$ | $\{s,s'\}$ | separates all pairs | $s\vee s'$ |

**How the formula is encoded:**
- Consistency: $T\Rightarrow T'$, $F\Rightarrow F'$, and $\neg(T'\wedge F')$.
- Clauses: $s'\Rightarrow\kappa_1\vee\kappa_2$ and $s\Rightarrow\kappa_3$.
- Copies: $\kappa\Rightarrow$ its literal.

**How the geometry realizes it:**
- Each unsafe set is a singleton or a cyclically adjacent pair, so it is a halfplane trace.
- Each one-pair observation is an antipodal pair, which is the unique maximum and minimum of $c=v(k)$.

**Correctness.** Traps of size $\ge2$ correspond exactly to satisfying assignments (FD §2.2), and there are no unintended traps. All coordinates and coefficients have $O(\log(n+m))$ bits.

**Verified exactly** on 58 formulas, including the degenerate ones (single variables, the empty clause, tautologies, repeated literals). The checks covered every point lying on the circle, every unsafe set and separated-pair set matching its intent, and satisfiable ⇔ trap (E006 §B).

## 4. Other results

| ID | Statement |
|---|---|
| D1 | Zero-padding preserves instances exactly: hardness in $\mathbb Q^d$ implies hardness in all $\mathbb Q^D$, $D\ge d$. |
| D3 | The dichotomy holds for $\varepsilon$-identification too, for every $\varepsilon<1$: two helpers are always at distance $>1$ once $n\ge2$. |
| D4 | ETH ⇒ no $2^{o(n)}$ algorithm in the plane, since the reduction has linear size. |
| D5 | XP in the number of observation lines, in every dimension: guess the extremes, then take the largest set within them. This is the observation-side twin of L7. **Hardness needs unboundedly many safety *and* observation directions;** D2 uses $\Theta(n)$ of each. |
| R4 | Arbitrary unsafe pairs are realizable in $\mathbb Q^4$ (moment curve), and $k$-sets in $\mathbb Q^{2k}$. |
| R5 | Arbitrary bipartite lone-pair graphs are realizable in $\mathbb Q^3$, via two orthogonal arcs. |

The route the brief proposed would have given hardness in $\mathbb Q^7$ (block sum of R4 and R5). D2 makes it unnecessary.

## 5. Stage 2 audit

- **G-O1 (fixed dimension open) is resolved:** coNP-complete for $d\ge2$.
- **The Stage 2 obstruction** (L10, arcs in convex position) is correct, and strengthened to an iff (R1). Its reading as an obstruction to hardness is corrected: it rules out only direct encodings.
- **The W[1] statement is corrected.** W[1]-hardness in $r$ rules out FPT. It does not show the XP exponent $r+2$ is optimal. The "essentially optimal in form" wording in the Stage 2 report has been amended.
- **Large minimal traps versus hardness.** The two are now explicitly separated. Planar convex position has both, but they are proved by different arguments, and aligned observations have large minimal traps with *unknown* complexity.
- **Computing $\sigma$ versus deciding identifiability.** These now have opposite complexities in the plane: $\sigma$ is polynomial (W4), TRAP is coNP-complete (D2).
- **Dimension requirements.**
  - *Hardness:* L6 and L7 need unbounded dimension; D2 does not.
  - *Tractability:* L7 and D5 need bounded directional complexity, not bounded dimension. L5 needs $d=1$.
- **A verification defect.** In E005 §C the "1–3 rays" generator rescaled components independently. The ledger now records this; the conclusion of that check is unaffected.

## 6. Contributions after Stage 3

**Strongest: the dimensional dichotomy for linear safe identifiability.** It has four parts:
- P for $d=1$;
- coNP-complete for every fixed $d\ge2$, already on the unit circle (D2/D3);
- XP in either directional parameter (L7, D5);
- W[1]-hard in safety directions when $d$ is unbounded.

Together with the Stage 1 combinatorial dichotomy (unsafe size 1 versus 2) and the deterministic-observation case, it gives a coherent statement: **safe learning becomes intractable exactly when ambiguous observations can isolate single forbidden pairs while safety can block those pairs from being tested. Two dimensions already provide both.**

**Novelty check (LR §8).**
- Not implied by the partial-FSM literature, which gives upper bounds only.
- Not implied by geometric hitting-set hardness, which concerns a different problem and is polynomial in the plane.
- No match found in targeted searches.

**Also substantive:**
- the lone-antipodal-pair characterization (R1/B4), which explains *why*;
- the observation-direction XP algorithm (D5).

**Not contributions:** B1–B3 (standard Boolean facts) and R4 (standard neighbourliness).

## 7. Verification

**`scripts/stage3_checks.py`** (E006, a few minutes):
- the Boolean formulation against exhaustive enumeration: 600 set-valued and 600 linear instances;
- the exact geometry and satisfiability equivalence of D2 on 58 formulas, up to 138 parameters;
- padding and block sums: 400 instances;
- D5 against exhaustive search: 420 instances;
- the lone-pair lemma: 3,582 one-edge relations.

**Bugs found and fixed:**
- an $O(n^2)$ exact-response routine, replaced by a sweep over sorted projections (Stage 2 output reproduced byte for byte);
- the per-component rescaling bug in random generators, fixed for E006 and recorded for E005.

**Tests:** 49, all passing (9 new).

**No theorem relies on computation.** D2's correctness is proved; the checks confirm the geometric realization and the equivalence on concrete formulas.

## 8. Remaining questions

**Mathematical:**
- A-O1, A-O2: aligned ($c\parallel a$) and orthogonal ($c\perp a$) planar models.
- D-O1: FPT status in the number of observation lines $k$.
- D-O2: binary-pattern observations without lone pairs in the plane.
- W-O1: FPT in $r$ for fixed $d$.
- Continuum: Q-K4′ and Q-K5 (Stage 2).

**Literature:**
- Johnson 1982 (W5's NP-hardness source, unread);
- the coreset size bound of Dudley / Bronshteyn–Ivanov / AHPV;
- a final targeted check that no "geometric CSP with halfplane scopes" result contains D2.

## 9. Recommendation

**Begin consolidating.** The central complexity question of the project, how much geometry is needed before safe learning becomes intractable, now has a sharp answer: two dimensions, and nothing less. The surrounding theory is in place:
- traps, $\sigma$, local-to-global principles;
- the continuum theorem, certificates and horizons;
- the Boolean and realization dictionaries.

The remaining open problems (aligned and orthogonal models, FPT refinements) are refinements that would not change the paper's main theorem.

**For Stage 4:**
1. Settle the two literature items and one more novelty search specifically for D2.
2. Decide whether A-O1 (aligned observations) is worth one focused attempt. A polynomial algorithm there would show that hardness *requires* safety and sensing to use different functionals, which is a natural interpretive statement for the paper.
3. Then begin manuscript architecture:
   - **main theorems:** T1/K1 (characterization), H1/D2/D3 (complexity), T5/G1′ ($\sigma$ and local-to-global), Q1′ (horizons);
   - **worked example:** the scalar model.
