# Stage 0 — Comparative assessment of research directions

*2026-11-20. Register IDs refer to `research/theorem_register.md`.*

## Summary table

| Dir. | Topic | Literature | Originality potential | Tractability | Recommendation |
|---|---|---|---|---|---|
| A | Safety–knowledge paradox (scalar thresholds) | SafeOpt reachable closure; incomplete learning | low as stated; the scalar model is now solved | done for the scalar model | **Close.** Keep as the worked example |
| B | Structure of deadlock (traps) | game theory; DES diagnosability (EXPTIME); Moldovan–Abbeel | **medium–high**: complexity dichotomy; continuum; structured classes | high (finite); medium (continuum) | **Pursue (primary)** |
| C | Multidimensional safe identifiability | safe linear bandits (stochastic, safe seed) | medium, *only with a richer model*: the natural linear model decouples (C1) | medium | **Pursue only as an instance of B** |
| D | Reachability of informative experiments | SafeMDP, ROA expansion, viability | medium; easy examples, harder characterisation | medium | Secondary; the B framework lifts to it |
| E | Price of a mistake (risk allowance) | soft-constraint safe bandits; chance constraints | potentially high, but the model is not yet well posed | low at Stage 0 | **Defer** until the model is fixed |
| F | Collective learnability | multi-agent safe exploration | low in the worst case (C2) | high | Defer; a corollary of B |

## Direction A — Safety–knowledge paradox

**Status after Stage 0.** The scalar model is fully analysed (`research/scalar_analysis.md`).
- Maximum safe intensity dominates every policy (S2).
- Instance-wise thresholds: $\lambda_c(p)$, the barrier $v_+$, and saddle-node slowing (S4, §6).
- Uniform irreducible diameter $\min(U_0 - L_0, 2\delta U_0^p)$, reached in one step (S5).
- Total deadlock iff $2\delta U_0^p \ge U_0 - L_0$ (S6).
- Answers: "Is the largest safe experiment the most informative?" Yes, here. "Can a less informative one be better?" No, here.

**Literature.** "Certified-safe expansion stops at a fixed point" is established, in the GP/Lipschitz form of SafeOpt ($\bar R_\epsilon(S_0)$). Learning that stops short of the truth is established in economics (incomplete learning, self-confirming equilibrium).

**Assessment.** The scalar model is a clean example, not a contribution. Its useful lessons for the paper:
1. **The uniform-versus-instance distinction.** Thresholds involving $\theta^\*$ are not uniform guarantees.
2. **The one-shot phenomenon.** In the uniform worst case, all guaranteed learning happens at the first experiment.
3. **The asymptotic set is a trap with equality.** This connects A to B.

**Open in A.**
- A model in which a *less* informative experiment is better. This needs a non-monotone coupling between risk and information. Candidate: two experiment families, one that shrinks the set in a direction that enlarges $\mathcal S$ and one that is more informative but does not. That is a Direction C/B question.

## Direction B — Structural characterisation of deadlock (**recommended primary direction**)

**Established in Stage 0** (`research/finite_analysis.md`):
- **F1.** In finite spaces, uniform $\varepsilon$-identifiability holds iff there is no trap of diameter $> \varepsilon$. *Standard technique; the formulation is the contribution.*
- **F2.** At most $|\Theta_0| - 1$ experiments are needed, and the bound is tight.
- **F3.** Without safety, identifiability is pairwise and polynomial.
- **F4.** With robust safety, non-identifiability is NP-complete (by reduction from 3-SAT) and identifiability is coNP-complete.
- **Non-locality.** A trap of size $n$ can have every proper subset identifiable in one experiment.

**Potential theorems (ordered by expected value).**
1. **B1 — complexity dichotomy (sharpen F3/F4).** Classify safety/observation structures by tractability.
   - Polynomial: threshold (monotone) safety in one dimension, which covers the scalar model, and convex/linear structures (C1).
   - coNP-complete: general safety.
   - Is there a natural middle class, such as safety with bounded VC dimension, or interval safety sets?
2. **B2 — continuum characterisation (Q-F3).** For compact $\Theta_0$ with continuous $g$ and $h$, is the worst-case asymptotic diameter equal to the supremum of $\operatorname{diam}$ over closed traps? Do finite-time and asymptotic identification differ exactly when the maximal trap is approached but never reached? The scalar model is the test case.
3. **B3 — uniform versus instance-wise (Q-F1).** Is there one policy that identifies every $\theta^\*$ that lies in no large trap? A negative answer would be a genuine "price of not knowing $\theta^\*$" result.
4. **B4 — adaptivity gap (Q-C3).** In the scalar model, adaptive and non-adaptive policies have the same uniform value. In general, safety makes the admissible information operators state-dependent. Is there a model with a large *uniform* adaptivity gap? That would contrast with the information-based-complexity theorem that adaption barely helps for linear worst-case problems.
5. **B5 — minimal number of experiments.** Hardness of approximation (via test cover). A rank bound in terms of a "trap depth".

**Obstacles.**
- The active-diagnosis literature has EXPTIME-completeness for a dynamic version (Haar et al.). F4 may be a known special case, so it must be read first.
- B2 needs care with open versus closed sets. The strict/closed boundary effect reappears in the scalar model, where the limit set satisfies the trap condition *with equality*.

**Computational needs.**
- B1: small exact solvers, already built (`scripts/finite_game.py`).
- B2: a discretisation that is sound by monotone over- and under-approximation. **Grids are unreliable near trap boundaries**, as the previous project's experience shows.

## Direction C — Multidimensional safe identifiability

> **Proposition C1 (the natural linear model decouples).** Take $h(\theta, u) = \theta^\top u$, safety $\theta^\top u \le 1$, actions $u \in \mathbb R^d_{\ge 0}$, $\Theta_0 \subset \mathbb R^d_{>0}$, and $|\eta| \le \delta$. A compact $K$ is a trap iff every coordinate projection $K_i = \{\theta_i : \theta \in K\}$ is a scalar trap, i.e. $\min K_i \ge (1 - 2\delta)\max K_i$.

*Proof.*
- **Rewriting the trap condition.** For $u \ge 0$, $u \ne 0$, let $m(u) = \min_K \theta^\top u$ and $M(u) = \max_K\theta^\top u > 0$. The actions in $\mathcal S(K)$ in direction $u$ are those scaled to $M \le 1$. The common-observation condition is $M - m \le 2\delta$ at $M = 1$. By homogeneity this is $m(u) \ge (1 - 2\delta)M(u)$ for all $u \ge 0$.
- **"If".** Coordinatewise, $m(u) \ge \sum_i u_i\min K_i \ge (1 - 2\delta)\sum_i u_i \max K_i \ge (1 - 2\delta)M(u)$.
- **"Only if".** Take $u = e_i$. ∎

**Consequences.**
- In this model, coupling creates **no** new worst-case obstructions. The answer to the brief's "identify each coordinate but not the vector?" is **no**, at the level of traps.
- Interesting multidimensional phenomena need at least one of the following:
  - **(a)** a safety function that depends on parameters other than the ones the action excites, e.g. $g = a(\theta)^\top u - 1$ with $h = b(\theta)^\top u$ and $a \ne b$;
  - **(b)** nonlinear intensity ($p \ne 1$ per coordinate, or cross-terms);
  - **(c)** a non-conic action set;
  - **(d)** dynamics (Direction D).
- **Caution.** If actions may have negative components and $\Theta_0 \subset \mathbb R^d_{>0}$, then directions $u \le 0$ are always safe and unboundedly scalable, so identification is trivial. The *action geometry relative to the risk geometry* is what matters. This matches the scalar caveat $x \ge 0$.

**Potential theorems.**
- C2: a characterisation of traps for the model in (a), via a ratio of support functions (a "polar width"). Expected to be genuinely $d$-dimensional.
- C3: a model where a lower-dimensional certified-safe cone permanently hides a direction of $\Theta$. "Safe excitation" as a rank condition on $\mathcal S(K)$ relative to the trap.
- C4: the adaptivity gap of B4 in a linear model.

**Literature.** Safe linear bandits (Amani et al.; Gangrade et al.) treat the stochastic, regret version with a safe seed or a soft constraint. Worst-case set-membership with endogenous safety appears unstudied, per the 2026 set-membership experiment-design paper's own future-work statement (seen in summary only).

## Direction D — Geometry and reachability of informative experiments

- **Easy facts (constructible immediately).** An environment can be identifiable by independently chosen experiments but not along a feasible safe trajectory. Example: the informative states lie beyond a region whose safety is uncertain. This is folklore in SafeMDP (reachability/returnability). **Not a contribution by itself.**
- **What would be a contribution.** A trap characterisation on the product of physical state and knowledge state:
  - "knowledge-trap × viability kernel";
  - a proof that a connected safe region is *not* sufficient;
  - quantitative mobility thresholds (control authority versus identifiability).
- **Obstacle.** The state-space blow-up. Active diagnosis is EXPTIME-complete in general, so only structured instances are tractable.
- **Recommendation.** Treat it after B, as "B with dynamics".

## Direction E — The price of a mistake

- **Not yet well posed.** With deterministic $\theta^\*$ and bounded noise, $\Pr^\pi_\theta(\text{violation})$ is either 0 or 1 unless $\pi$ randomises.
- A randomised risky probe with probability $\epsilon$ changes the minimax *expected* error by $O(\epsilon)$ in the scalar model. That suggests continuity at 0 there; not proved.
- Discontinuities are more plausible under:
  - **(i)** unbounded noise, where a hard constraint forbids almost everything;
  - **(ii)** lifetime budgets with $T \to \infty$, where the order of limits matters.
- **Recommendation.** Fix the model first (`research/stage0_spec.md` §6). Defer.

## Direction F — Collective learnability

- **Worst case with identical agents:** the adversary can replicate observations, so the team equals a single agent with the union of actions.
- **Heterogeneous safety:** the team's admissible set is $\bigcup_i \mathcal S_i(K)$, and the trap condition F1 holds verbatim with that union. In the non-local example a single agent able to run $a_k$ breaks the deadlock.
- So, in the worst case, F reduces to B with an enlarged action set. Interesting effects need stochastic noise, communication constraints or shared budgets.
- **Recommendation.** Defer.

## Overall recommendation

Make **B the primary direction**, with C, D and F as instances of B with more structure.
- The scalar model (A) is the expository anchor.
- The concrete Stage 1 targets are B1 (dichotomy), B2 (continuum) and B3 (uniform versus instance-wise), after reading the active-diagnosis complexity papers and the 2026 set-membership experiment-design paper in full.
