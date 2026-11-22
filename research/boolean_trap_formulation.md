# Stage 3 — Boolean formulation of informational traps

*2026-11-21. Code: `scripts/boolean.py`. Checks: E006 §A.*

## 0. Summary

| ID | Statement | Status |
|---|---|---|
| B1 | Traps of size $\ge2$ are exactly the satisfying assignments, with at least two ones, of an explicit CNF: one clause per experiment and per minimal observation conflict. With interval (Helly-2) observations every conflict is a pair. | proved |
| B2 | $\lvert B_u\rvert\le1$ ⇒ Horn. Stage 1's closure algorithm P3 is least-model propagation. | proved; standard |
| B3 | The constraint language used by the hardness proofs: positive 2-clauses, Horn implications with two negative literals, and one mixed shape with two negative and two positive literals. It is non-Horn, non-dual-Horn, non-bijunctive and non-affine, which is Schaefer's NP-complete case. | proved; classification standard |
| B4 | **Clause shape does not determine complexity; the conflict-graph family does.** Deterministic observations produce clauses of the same shapes but only complete-multipartite conflict graphs, and are polynomial (P2). Every known hardness reduction uses **lone forbidden pairs** (or stars) as its negation primitive. *(Stage 4 audit: "hardness needs a lone pair" is not a theorem about all observation models; see `complexity_map.md` §4 and D-O2.)* | proved (the deterministic part); observation (the reductions) |
| B5 | Geometric meaning of a one-edge conflict: a strictly antipodal pair (R1). In $d=1$ there is exactly one such pair, which explains the $d=1$ tractability from the observation side. | proved |

**Answer to the brief's question 1.**
- Yes. The Boolean form makes the Stage 1 dichotomy transparent:
  - size-1 unsafe sets give Horn, hence P;
  - size 2 adds a second positive literal, hence NP-complete.
- It also exposes the *expressive primitive* that every hardness proof needs, and that geometry must supply: a negative pair $\neg x\vee\neg y$, conditional on avoiding an unsafe set. In the linear model, that primitive is an antipodal pair. This is exactly what D2 realizes in the plane.
- None of the Boolean facts themselves are new. The contribution is the dictionary between geometry and clause shapes.

## 1. The formulation

Fix a finite instance $(\Theta_0,\mathcal U,B,\mathcal Y)$, where $B_u$ is the unsafe set of experiment $u$. A **conflict** of $u$ is an inclusion-minimal $F\subseteq\Theta_0$ with $\bigcap_{\theta\in F}\mathcal Y(\theta,u)=\varnothing$, and $\mathrm{Conf}(u)$ is the set of conflicts. Let $x_i=[\theta_i\in K]$.

> **Theorem B1.** $K$ is a trap iff $x=\mathbf 1_K$ satisfies
> $$\Phi=\bigwedge_{u}\ \bigwedge_{F\in\mathrm{Conf}(u),\ F\cap B_u=\varnothing}\Bigl(\bigvee_{i\in F}\neg x_i\ \vee\ \bigvee_{k\in B_u}x_k\Bigr).$$
> Exact non-identifiability is $\exists x\models\Phi$ with $\sum_ix_i\ge2$. For $\varepsilon>0$, the cardinality condition becomes "$x_i=x_j=1$ for some pair with $d(\theta_i,\theta_j)>\varepsilon$". That is a disjunction over far pairs, decided by branching on the pair.

*Proof.*
- **The trap condition.** $K$ is a trap iff every $u$ either meets $B_u$ or has a common observation over $K$.
- **Conflicts.** The second alternative fails iff $K$ contains some conflict. So the condition is "for every $u$ and every conflict $F\subseteq K$, $K$ meets $B_u$". That is the clause.
- **Dropping clauses.** Clauses with $F\cap B_u\ne\varnothing$ are tautologies on the sets they would constrain, since $F\subseteq K$ already meets $B_u$.
- **Pairs.** With interval or deterministic observations, 1-D Helly makes every conflict a pair. ∎

**Size.**
- With pair conflicts, $\Phi$ has $O(mn^2)$ clauses.
- If *every* pair outside $B_u$ is a conflict, then under $\lvert K\rvert\ge2$ the experiment's clauses collapse to the single positive clause $\bigvee_{k\in B_u}x_k$. The solver uses this.

**Regression (E006 §A).**
- 600 random set-valued instances, with hyperedge conflicts: 600/600.
- 600 random linear instances in $d=1,2,3$, with pair conflicts: 600/600.

## 2. Horn, and the dichotomy at unsafe size two

> **B2.** If $\lvert B_u\rvert\le1$ for all $u$, every clause has at most one positive literal, i.e. it is Horn. Satisfiability with $x_i=x_j=1$ forced is decided by unit propagation from $\{i,j\}$, which yields the least model. Iterating over pairs gives Stage 1's P3.

*Proof.* Horn-SAT; standard (e.g. Dowling–Gallier). ∎

**What size two adds (B3).** The Stage 1–3 reductions use exactly these clause types:
- $(y\vee z)$, from an experiment that separates every pair and has unsafe set $\{y,z\}$;
- $(\neg a\vee\neg b)$, from an always-safe experiment with a one-edge conflict;
- $(\neg x\vee\neg w\vee y)$ and $(\neg x\vee\neg w\vee y\vee z)$, from one-edge conflicts $\{x,w\}$ with unsafe sets $\{y\}$ and $\{y,z\}$;
- $(w)$, i.e. $\neg x_i\vee\neg x_j\vee w$ for all pairs, which under $\lvert K\rvert\ge2$ forces $w$.

**The language is NP-complete, and each class of clauses is needed.**
- Positive 2-clauses rule out Horn.
- Negative 2-clauses rule out dual-Horn.
- The 4-literal clauses rule out bijunctive.
- The relations are not affine.

By Schaefer's dichotomy the language is NP-complete. The reductions supply the cardinality-$\ge2$ side condition through forced helpers.

## 3. Conflict graphs decide; clause shapes do not

**Deterministic observations (B4).** If observations are deterministic, the pair conflicts of $u$ form the **complete multipartite graph** whose parts are the level sets of the observation. For $n\ge3$ such a graph never has exactly one edge. If $a$ and $b$ are in different parts, every other $z$ lies in a part different from at least one of them, so it conflicts with at least one of them.

The clauses of P2 instances look as non-Horn as those of the hard instances, yet P2 is polynomial: the split recursion exploits the multipartite structure.

**So the expressive primitive is a lone forbidden pair.** That is a pair $\{x,y\}$ that conflicts while neither conflicts with anything else. Its geometric meaning is in R1 (`research/geometric_realizations.md`).

**One dimension (B5).**
- In $d=1$ the only lone forbidden pair available to any experiment is $\{\min\Theta_0,\max\Theta_0\}$.
- Safety traces in $d=1$ are prefixes and suffixes, so unsafe sets are thresholds and $\sigma\le2$.
- Both sides of the Boolean language collapse. This is the structural content of L5.

**Bounded observation directions** (D5) bound the number of *distinct* conflict orders. That is a different collapse, and it gives XP rather than P.

## 4. Relation to known frameworks

- **Closure systems.** Horn constraint sets define closure systems (Moore families). The traps of a $\lvert B\rvert\le1$ instance containing a fixed pair have a least element. For $\lvert B\rvert\ge2$, traps are not closed under intersection (Stage 1 T4), consistent with leaving Horn.
- **Constraint satisfaction.** The trap problem is a CSP over the Boolean domain with one global cardinality constraint. Schaefer's theorem classifies its clause language. The geometric question is which clause sets are *realizable*. That is a realizability, not expressiveness, question, settled for $d\ge2$ by D2.
