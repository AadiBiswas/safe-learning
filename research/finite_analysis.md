# Stage 0 — Finite parameter spaces: traps, identifiability and complexity

*2026-11-20. Direction B of the brief. Proofs are given here in full. Brute-force checks are in `scripts/finite_game.py`, with output in `results/finite_game.txt`.*

**Literature status.** The proof technique of F1 is the standard least-fixed-point / attractor argument for finite reachability games, applied to the knowledge-state (subset) construction that is standard for games of imperfect information (Reif 1984; Chatterjee–Doyen–Henzinger–Raskin 2007, see `research/literature_review.md`). **F1 should be presented as a formulation, not as a deep theorem.** Its value is the specific trap condition it produces. F3 and F4 are the substantive items. Neither has yet been located in the literature, but the search is incomplete.

## 1. Setting

- **Parameters and tolerance.** $\Theta_0$ is a finite set with a metric; I use points on $\mathbb R$ with $\operatorname{diam} K = \max K - \min K$. The tolerance is $\varepsilon \ge 0$, and $\varepsilon = 0$ means exact identification.
- **Actions.** A finite set $\mathcal U$, with a safety relation: $u$ is safe for $\theta$ iff $g(\theta, u) \le 0$. Write $S(K) = \{u : u \text{ safe for every } \theta \in K\}$.
- **Observations.** $\mathcal Y(\theta, u)$ is a nonempty set. In the main case, $\mathcal Y(\theta, u) = [h(\theta, u) - \delta,\ h(\theta, u) + \delta] \subset \mathbb R$.
- **Game.**
  - The consistent set starts at $\Theta_0$.
  - At each step the agent picks $u \in S(\Theta_t)$, which is robust safety. The adversary reports $y \in \mathcal Y(\theta^\*, u)$.
  - Then $\Theta_{t+1} = \{\theta \in \Theta_t : y \in \mathcal Y(\theta, u)\}$.
- **Uniform $\varepsilon$-identifiability.** There is a policy that, for every $\theta^\* \in \Theta_0$ and every admissible observation sequence, reaches $\operatorname{diam}\Theta_t \le \varepsilon$ in finitely many steps.

**On quantifiers.** The adversary may choose $\theta^\*$ lazily, i.e. at the end. Every $\theta$ in the current consistent set is consistent with every observation so far. So "for all $\theta^\*$ and all noise" is the same as an adversary who need only keep $\Theta_t$ nonempty.

## 2. The trap characterisation

**Definition (trap; the brief's "self-preserving indistinguishable set").** $K \subseteq \Theta_0$ is a *trap* if $K \ne \varnothing$ and for every $u \in S(K)$,
$$\bigcap_{\theta \in K}\mathcal Y(\theta, u) \ne \varnothing.$$
- If $S(K) = \varnothing$, $K$ is a trap vacuously: nothing is certified safe, so nothing can be learned.
- For interval observations, Helly's theorem in dimension 1 makes the condition pairwise: $\max_K h(\cdot, u) - \min_K h(\cdot, u) \le 2\delta$.

> **Theorem F1.** $\Theta_0$ is uniformly $\varepsilon$-identifiable **iff** it contains no trap $K$ with $\operatorname{diam} K > \varepsilon$.

*Proof.*
- **(⇐ fails if a trap exists.)** Let $K \subseteq \Theta_0$ be a trap with $\operatorname{diam} K > \varepsilon$, and take $\theta^\* \in K$.
  - Suppose $\Theta_t \supseteq K$. Then $S(\Theta_t) \subseteq S(K)$, so the agent's action $u$ lies in $S(K)$.
  - The adversary reports $y \in \bigcap_{\theta \in K}\mathcal Y(\theta, u)$. This is admissible, since $\theta^\* \in K$. Then $\Theta_{t+1} \supseteq K$.
  - By induction $\operatorname{diam}\Theta_t \ge \operatorname{diam} K > \varepsilon$ forever.
- **(⇒ if no trap, the agent wins.)** Call $K$ *losing* if the adversary can keep the consistent set at diameter $> \varepsilon$ forever starting from $K$.
  - Suppose $\Theta_0$ is losing. The losing subsets of $\Theta_0$ form a finite nonempty family, so take an inclusion-minimal one, $K$.
  - At $K$, for every $u \in S(K)$ the adversary has a response $K' = \{\theta \in K : y \in \mathcal Y(\theta, u)\}$ that is losing. Here $K' \subseteq K$, and $K' \ne \varnothing$ because the adversary must stay consistent.
  - By minimality $K' = K$. So $y \in \mathcal Y(\theta, u)$ for all $\theta \in K$: $K$ is a trap, and $\operatorname{diam} K > \varepsilon$ because $K$ is losing.
  - Finite games of this kind are determined. A state is either winning for the agent or losing in the sense above, since the consistent set can strictly shrink only finitely often. ∎

> **Proposition F2 (experiment count).** If $\Theta_0$ is uniformly $\varepsilon$-identifiable, an optimal policy uses at most $|\Theta_0| - 1$ experiments. The bound is attained.

*Proof.*
- Let $r(K)$ be the attractor rank (the number of steps to win from $K$).
- If the optimal action at $K$ admitted a response with $K' = K$, then $r(K) > r(K') = r(K)$, a contradiction. So every response strictly shrinks $K$, and $r(K) \le |K| - 1$.
- Attainment: the brute-force search found instances with ratio exactly 1 (`results/finite_game.txt`). ∎

## 3. Without safety the problem is pairwise; with safety it is not

> **Proposition F3 (unconstrained case).** Suppose $S(K) = \mathcal U$ for all $K$ (no safety constraints), and observations are intervals. Then $\Theta_0$ is uniformly $\varepsilon$-identifiable iff every pair $\theta, \theta'$ with $|\theta - \theta'| > \varepsilon$ is separated by some action, i.e. $|h(\theta, u) - h(\theta', u)| > 2\delta$. This is checkable in $O(|\Theta_0|^2|\mathcal U|)$ time.

*Proof.*
- If a trap $K$ with $\operatorname{diam} > \varepsilon$ exists, its two extreme points form a trap pair: they have fewer constraints and the same action set.
- Conversely, a non-separated far pair is a trap. Apply F1. ∎

**Example (non-locality of safe identifiability).**
- Take $\Theta_0 = \{1, \dots, n\}$ and actions $a_1, \dots, a_n$. Action $a_k$ is safe for every $\theta \ne k$, and $h(\theta, a_k) = \theta$, with $\delta < 1/2$.
- Then $\Theta_0$ is a trap: every action is unsafe for some member.
- Yet every proper subset is identified by **one** experiment: if $k \notin K$, play $a_k$.
- So the minimal trap has size $n$. Knowing *any* single fact of the form "$\theta^\* \ne k$" would unlock everything, and no safe experiment can supply it.
- Checked for $n \le 7$ in `results/finite_game.txt`. Random instances also contain cases where every pair is identifiable on its own but $\Theta_0$ is not (30 of 3,000).

**Reading.** Safety turns identifiability from a pairwise (graph) property into a genuinely higher-order (hypergraph) property. The obstruction can be invisible to every proper sub-question.

> **Proposition F4 (complexity; safety makes it hard).** With interval observations and rational data:
> - deciding whether $\Theta_0$ contains a trap of size $\ge 2$ (non-identifiability at $\varepsilon = 0$) is **NP-complete**;
> - uniform exact identifiability is **coNP-complete**.

*Proof.*
- **Membership.** A trap $K$ is a certificate. Checking it means computing $S(K)$ and, for each $u \in S(K)$, the spread of $h(\cdot, u)$ on $K$: polynomial.
- **Hardness, from 3-SAT.** For variables $x_1, \dots, x_n$ ($n \ge 2$), take parameters $T_i, F_i$ (distinct points) and $\delta = 0.6$. Introduce three kinds of action:
  - $b_i$: safe for all. $h = 1$ at $T_i$, $h = -1$ at $F_i$, and $h = 0$ elsewhere. It kills exactly those $K$ that contain both $T_i$ and $F_i$, since only there is the spread $2 > 1.2$.
  - $a_i$: unsafe exactly for $T_i$ and $F_i$, with pairwise-separating values, e.g. $h = 10\cdot(\text{index})$. It kills exactly those $K$ with $|K| \ge 2$ that meet neither $T_i$ nor $F_i$.
  - $c_j$ for clause $C_j$: unsafe exactly for the parameters of the literals of $C_j$, with pairwise-separating values. It kills exactly those $K$ that contain no literal of $C_j$.
- So a set $K$ with $|K| \ge 2$ is a trap iff it contains exactly one of $T_i, F_i$ for each $i$ and meets every clause, i.e. iff it is the set of true literals of a satisfying assignment. The size is $2n$ parameters and $2n + m$ actions. ∎

*Check.* 400 random 3-SAT instances with 2–5 variables gave 400/400 agreement between satisfiability, trap existence and the brute-force game value (`results/finite_game.txt`).

**Reading.**
- Without safety constraints, worst-case identifiability is a pairwise, polynomial question (F3).
- With robust safety constraints it is coNP-complete (F4).
- The entire hardness comes from the circular dependency the project is about: whether an experiment may be run depends on what is still unknown.

**Caveats.**
- F4 is a worst-case complexity statement about general finite instances. It says nothing about structured (e.g. monotone or convex) families, where traps may be polynomially detectable. The scalar model is one such family (`research/scalar_analysis.md` §8).
- For non-interval observation sets, Helly fails. Then even the unconstrained problem may not be pairwise; this is not examined yet.
- Uniformity over $\theta^\*$ is essential to F1. The question "which $\theta^\*$ does a *single* policy identify?" is open (Q-F1 in the register).

## 4. Open questions raised here

1. **Q-F1 (instance-wise).** Is there one policy that identifies exactly those $\theta^\*$ that lie in no trap of diameter $> \varepsilon$? Or does the agent's ignorance of $\theta^\*$ force a loss?
2. **Q-F2 (structure).** For which structured classes is trap detection polynomial? Candidates: safety monotone in a one-dimensional parameter and $h$ monotone, i.e. "threshold" safety, which is what the scalar model has.
3. **Q-F3 (continuum).** For compact $\Theta_0$ with continuous $g$ and $h$: is the worst-case limiting diameter equal to the supremum of $\operatorname{diam} K$ over closed traps? The scalar model satisfies this, both uniformly (S5) and instance-wise, where the limit set is a trap with equality. A proof would need a compactness argument like the one for viability kernels; in the instance-wise scalar case the limit is attained only asymptotically.
4. **Q-F4 (approximation).** Is the minimum number of experiments (the attractor rank) hard to approximate? It is at least as hard as decision-tree minimisation in the unconstrained case, which is known to be hard (to be checked against the literature).
