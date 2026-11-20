# Stage 0 report — Can You Learn Without Making Mistakes?

*2026-11-20. A self-contained handoff. Detailed proofs are in the files cited. The register of all results is `research/theorem_register.md`.*

## 1. The problem in one paragraph

An agent must choose experiments that are safe for *every* parameter still consistent with its data. Its data come only from those experiments, and the noise is bounded and worst-case. The consistent set $\Theta_t$ determines the certified-safe actions $\mathcal S(\Theta_t)$; the actions determine how $\Theta_t$ shrinks.

Stage 0 asked:
- when this loop stalls, and whether it can be characterised exactly;
- how much of the preliminary scalar picture survives scrutiny;
- which direction is worth a paper.

## 2. What has been independently established

**Scalar model** (`research/scalar_analysis.md`). The model: safe iff $\theta^\* x \le 1$, and $Y = \theta^\* x^p + \eta$ with $|\eta| \le \delta$.
1. **S2 — maximum safe intensity is optimal** for every objective that is monotone under inclusion (upper bound, diameter, identification, certified-safe set), at every horizon. The proof is a coupling: any other policy's consistent set can be kept a superset. So **in this model nothing is gained by a less informative experiment, and all learning objectives share one optimal policy.**
2. **S3/S4 — the preliminary recurrence, the critical value $\lambda_c(p) = (p-1)^{p-1}/p^p$, the $p = 2$ condition $8\delta\theta^\* = 1$, and the fixed points are all correct.** The complete structure for every $p > 0$:
   - $p < 1$: always progress from far, down to a positive floor; no threshold.
   - $p = 1$: threshold $\delta = 1/2$, independent of $\theta^\*$.
   - $p > 1$: a saddle-node at $\lambda_c$. The basin $(v_-, v_+)$ converges to $v_-$; priors above the barrier $v_+$ never improve.
3. **S4a/S4b.**
   - At $\lambda_c$ nothing moves.
   - Below it, the passage time scales as $(\lambda_c - \lambda)^{-1/2}$, with an explicit constant at $p = 2$.
   - The asymptotic upper bound jumps discontinuously in $\delta$ and in $U_0$.
4. **S5 — the uniform answer is one-shot.** Taking the worst case over $\theta^\*$ as well, which is what a guarantee means, the irreducible diameter is exactly $\min(U_0 - L_0,\ 2\delta U_0^{\,p})$. It is attained after **one** experiment and never improved.
5. **S6 — total deadlock** (nothing is ever learned in the worst case) holds iff $2\delta U_0^{\,p} \ge U_0 - L_0$. For $p > 1$ it is forced by a conservative enough prior, $U_0 \ge (2\delta)^{-1/(p-1)}$, for **every** truth.

**Finite spaces** (`research/finite_analysis.md`).
6. **F1.** Uniform $\varepsilon$-identifiability holds iff $\Theta_0$ contains no *trap* — a set $K$ such that every action certified safe for $K$ has an observation compatible with all of $K$ — of diameter $> \varepsilon$. This is the brief's candidate theorem, true as stated for uniform identification. The proof is the standard minimal-losing-set argument.
7. **F2.** At most $|\Theta_0| - 1$ experiments are needed, and the bound is tight.
8. **F3 versus F4 — a complexity dichotomy driven by safety.**
   - Without safety constraints, identifiability is a pairwise property, decidable in polynomial time.
   - With robust safety it is **coNP-complete**, and trap existence is NP-complete, by a reduction from 3-SAT. Checked on 400 random instances.
9. **F5 — non-locality.** A trap of any size $n$ exists whose every proper subset is identified by one experiment. Pairwise safe distinguishability does not imply safe identifiability.

**Multidimensional** (`research/research_directions.md`, Direction C).
10. **C1.** In the natural linear model — observe $\theta^\top u$, safe iff $\theta^\top u \le 1$, $u \ge 0$ — traps are exactly products of scalar traps. Coupling creates no new obstructions. Genuine multidimensional effects need richer structure.

## 3. Preliminary assumptions or derivations that were incorrect or incomplete

| Preliminary claim | Verdict |
|---|---|
| The recurrence $U_{t+1} = \min(U_t, \theta^\* + 2\delta U_t^p)$; $\lambda_c$; the $p = 2$ fixed points | **Correct.** |
| "Whether learning progresses depends on $8\delta\theta^\* < 1$" | **Instance-wise only.** It depends on the unknown $\theta^\*$, so the agent cannot evaluate it. The uniform worst case has no threshold (S5). |
| Tracking only the upper endpoint | **Incomplete.** Under that very adversary, $L_t = \theta^\*$ from $t = 1$. The deadlock is one-sided. |
| "Maybe a less informative experiment helps" | **False in the scalar model** (S2). Still open in richer models. |
| Linear multidimensional models as a source of coupled obstructions | **False for the natural linear model** (C1). |
| Implicit: actions $x \ge 0$ | **An essential assumption.** With two-sided actions, identification is immediate (C1a). |

## 4. What appears already known

- **"Certified-safe expansion stops at a fixed point."** Established in GP safe optimisation. Sui et al. (ICML 2015) define a reachability closure $\bar R_\epsilon(S_0)$ and state that nothing outside it can ever be certified. **Our deadlock must be positioned against this.**
- **"Learning stops short of the truth because the chosen actions are uninformative."** Established in economics: incomplete learning (Easley–Kiefer 1988) and self-confirming equilibrium (Fudenberg–Levine 1993). **The project's motivating question needs to cite these up front.**
- **Feasible-set (set-membership) estimation.** Standard (Milanese–Vicino 1991).
- **F1's technique.** Standard for finite games on knowledge states.
- **Hardness of safe exploration in a Bayesian MDP model.** Moldovan–Abbeel 2012 (NP-hard existence of $\delta$-safe policies).
- **Active diagnosability is EXPTIME-complete in a dynamic DES model.** Haar–Haddad–Melliti–Schwoon 2013, seen only as a summary. **F4 may be a special case of known DES results. This is the main unresolved literature risk.**
- **Known safe actions and slack.** Safe linear bandits assume a known safe action (or 0 in the interior) and treat the zero-slack case separately (Amani et al. 2019). Gangrade et al. (COLT 2024) drop the safe point, but only with soft (cumulative) constraints.

## 5. Promising directions

**Direction B (structure of deadlock) is recommended as primary.** The others become instances of it:
- C: richer observation/safety geometry;
- D: product with physical state;
- F: enlarged action sets.

Direction A is now closed in the scalar model and becomes the worked example. Direction E needs its model fixed before anything can be said.

## 6. Conjectures that deserve immediate investigation

1. **Q-F3 (continuum characterisation).** For compact $\Theta_0$ and continuous $g, h$, the worst-case asymptotic diameter equals the supremum of $\operatorname{diam}$ over closed traps. The scalar model satisfies it, uniformly and instance-wise; there the limit set is a trap *with equality*. **This is the most natural candidate for a substantial theorem.**
2. **Q-F2 (dichotomy).** Identify the structure that makes trap detection polynomial (monotone/threshold safety, linear models) against coNP-complete. A clean dichotomy would be a real result.
3. **Q-F1 (price of not knowing $\theta^\*$).** Can one policy achieve, for each $\theta^\*$, the instance-wise optimum? In the scalar model yes (S2). In general unknown.
4. **Q-C2.** Genuinely multidimensional traps when safety and observation use different functionals.
5. **Q-C3.** A model with a large uniform adaptivity gap. This would contrast with the information-based-complexity result that adaption barely helps in linear worst-case problems.

## 7. Recommended next stage

**Stage 1A (literature, about one session).** Before any further theorem work:
- read in full the active-diagnosis complexity papers (Haar et al. 2013/2017);
- read safe diagnosability (Paoli–Lafortune 2005);
- read the 2026 set-membership experiment-design paper (arXiv:2607.00844);
- run the generic queries listed in `research/literature_review.md` §5.

*Reason:* F4 and the trap formulation are the only potentially distinct items, and the DES literature is where they would already live under other names.

**Stage 1B (mathematics), if 1A leaves room.** Q-F3 (continuum) and Q-F2 (dichotomy), in that order.
- Q-F3 connects the elementary scalar example to the finite theory, and is the most likely publishable core.
- Q-F2 turns F3/F4 from an example of hardness into a structural statement.

**Not recommended now:** Direction E (ill-posed until the risk model is fixed); a general safe-learning framework or RL experiments (out of scope); scaling the brute-force solvers (it would not change any conclusion).

## 8. Files

| File | Content |
|---|---|
| `research/stage0_spec.md` | Formal definitions, quantifiers, objectives, later models |
| `research/scalar_analysis.md` | Scalar model: S1–S8 with proofs |
| `research/finite_analysis.md` | Finite spaces: F1–F5 with proofs |
| `research/research_directions.md` | Directions A–F; C1 |
| `research/literature_review.md` | Sources with access levels; novelty table; gaps |
| `research/theorem_register.md` | All IDs and statuses |
| `scripts/scalar.py`, `scripts/scalar_check.py`, `scripts/finite_game.py` | Numerical and brute-force checks |
| `results/ledger.md` | Experiment ledger |
| `tests/` | 19 tests of the invariants |
