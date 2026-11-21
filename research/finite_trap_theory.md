# Stage 1 — Finite-space trap theory

*2026-11-21. This supersedes the Stage 0 treatment in `research/finite_analysis.md`, which I keep as the historical record. Every claim here is proved below. The exhaustive regression checks are in `scripts/stage1_finite.py` (output `results/stage1_finite.txt`, ledger E003). The literature status of each result is in §8 and in `research/literature_review.md` §6.*

## 0. Summary

| ID | Statement | Status |
|---|---|---|
| T1 | Characterization: no far trap ⇔ uniformly identifiable ⇔ eventually identifiable ⇔ identifiable within $\lvert\Theta_0\rvert-1$ experiments. Valid for arbitrary set-valued observations, an adaptive adversary and randomized policies. | proved; standard technique |
| T2 | **Myopic play is optimal for feasibility.** If no far trap exists, *any* policy that plays some safe informative experiment at each step succeeds within $\lvert\Theta_0\rvert-1$ experiments. The bound is attained, even by optimal policies. | proved |
| T3 | **A universal instance-optimal policy.** The same myopic policy leaves, for every $\theta^\*$, a final set of diameter at most $D(\theta^\*)=\max\{\operatorname{diam}K : K\ni\theta^\*\text{ a trap}\}$, and no policy guarantees less. This settles Stage 0's Q-F1 positively. | proved |
| T4 | Trap families are closed under restriction and under products with independent experiments. They are **not** closed under union, intersection, subsets or supersets. With joint experiments, projections of traps need not be traps. | proved; counterexamples verified |
| T5 | **Minimal traps.** For $n\ge3$, a minimal trap of size $n$ needs at least $n$ experiments that are unsafe somewhere on it. $n$ experiments with deterministic binary observations suffice. | proved |
| T6 | **Universality.** Every family of subsets of size $\ge2$ is the trap family of some instance. | proved |
| Ob | Oblivious noise combined with randomization can break T1. The adaptive-adversary assumption is essential. | example |

The Stage 0 statements F1, F2, F5 survive. F1 and F2 were stated only for interval observations; they hold verbatim for arbitrary set-valued observations. Q-F1 is answered by T3.

## 1. Setting

- **Parameters.** $\Theta_0$ is finite, with a metric $d$. For $K\subseteq\Theta_0$ write $\operatorname{diam}K=\max_{K}d$. Given a tolerance $\varepsilon\ge0$, call $K$ *far* if $\operatorname{diam}K>\varepsilon$. For $\varepsilon=0$, far means $\lvert K\rvert\ge2$.
- **Experiments.** A finite set $\mathcal U$. $U(u)\subseteq\Theta_0$ is the set of parameters for which $u$ is unsafe. The certified-safe set is $\mathcal S(K)=\{u : U(u)\cap K=\varnothing\}$. This is the brief's $\bigcap_{\theta\in K}\{u : g(\theta,u)\le0\}$.
- **Observations.** $\mathcal Y(\theta,u)$ is a nonempty subset of an arbitrary set $\mathsf Y$, finite or not.
  - The *response* to $y$ at $K$ is $K_y=\{\theta\in K : y\in\mathcal Y(\theta,u)\}$.
  - Only the distinct nonempty responses matter. There are at most $2^{\lvert K\rvert}$ of them, so continuous observation spaces add nothing.
- **$u$ is informative on $K$** if $\bigcap_{\theta\in K}\mathcal Y(\theta,u)=\varnothing$, i.e. every response is a proper subset of $K$.
- **Trap.** $K\ne\varnothing$ is a trap if no $u\in\mathcal S(K)$ is informative on $K$. Two cases are vacuous:
  - every singleton is a trap;
  - every $K$ with $\mathcal S(K)=\varnothing$ is a trap.
- **Protocol.**
  - $\Theta_t$ starts at $\Theta_0$. At each step the agent chooses $u_t\in\mathcal S(\Theta_t)$.
  - The adversary reports $y_t\in\mathcal Y(\theta^\*,u_t)$. The report may depend on the whole history, including $u_t$ ("adaptive noise").
  - Then $\Theta_{t+1}=(\Theta_t)_{y_t}$.
  - A policy maps histories to (distributions over) experiments.
- **Identification notions.** The goal is $\operatorname{diam}\Theta_t\le\varepsilon$.
  - *Uniform finite-time:* $\exists T\ \forall\theta^\*\ \forall$ admissible reports, the goal holds by time $T$.
  - *Eventual:* $\forall\theta^\*\ \forall$ reports $\exists T$.
  - *Exact identification* is the case $\varepsilon=0$. Then $\operatorname{diam}\Theta_t=0$ means $\Theta_t=\{\theta^\*\}$, because $\theta^\*\in\Theta_t$ always.
  - For $\varepsilon>0$, $\operatorname{diam}\Theta_t\le\varepsilon$ means every point of $\Theta_t$ is within $\varepsilon$ of $\theta^\*$. That is identification to tolerance $\varepsilon$, which is stronger than any statement about a point estimate.

**Lazy adversary.** Every $\theta\in\Theta_t$ is consistent with every report so far. So "for all $\theta^\*$, for all reports" is the same as an adversary who only has to keep $\Theta_t$ nonempty, with $\theta^\*$ chosen at the end. I use this freely. Where $\theta^\*$ is fixed in advance (T3), the argument is given explicitly.

## 2. Characterization

> **Theorem T1.** For finite $\Theta_0$, $\mathcal U$ and arbitrary $\mathcal Y$, the following are equivalent:
> 1. no far trap $K\subseteq\Theta_0$ exists;
> 2. some deterministic policy achieves $\operatorname{diam}\Theta_t\le\varepsilon$ within $\lvert\Theta_0\rvert-1$ steps, uniformly;
> 3. some policy, possibly randomized, achieves eventual identification surely, i.e. for every realization of its randomness.

*Proof.*
- **(1)⇒(2)** is Theorem T2 below.
- **(2)⇒(3)** is trivial.
- **(3)⇒(1)**, by contraposition. Let $K$ be a far trap and fix $\theta^\*\in K$.
  - Whenever $\Theta_t\supseteq K$, $\mathcal S(\Theta_t)\subseteq\mathcal S(K)$. So whatever $u_t$ the policy draws, $u_t$ is not informative on $K$.
  - The adversary therefore has some $y\in\bigcap_{\theta\in K}\mathcal Y(\theta,u_t)$, which is admissible since $\theta^\*\in K$. The new set is $\Theta_{t+1}\supseteq K$.
  - By induction $\operatorname{diam}\Theta_t\ge\operatorname{diam}K>\varepsilon$ for all $t$, on every realization of the policy's randomness. ∎

**Remarks.**
- **Empty safe sets.** If $\mathcal S(K)=\varnothing$, the agent cannot move at $K$. The definition counts such $K$ as traps, which is what T1 needs. If $\mathcal S(\Theta_0)=\varnothing$ and $\Theta_0$ is far, nothing can be learned.
- **Singletons** are traps but never far, so they never obstruct identification.
- **Randomization does not help against adaptive noise.** The adversary answers after seeing $u_t$, so the trap is held on every sample path.
- **Example Ob — oblivious noise is different.** Take $K=\{0,1\}$, no safety constraints, $\delta=\tfrac12$, and two experiments with $h(\theta,u_1)=\theta$ and $h(\theta,u_2)=-\theta$.
  - Both are uninformative on $K$, because the intervals touch. But the only common reports are $y=\tfrac12$ for $u_1$ and $y=-\tfrac12$ for $u_2$.
  - When $\theta^\*=0$ these need $\eta=+\tfrac12$ and $\eta=-\tfrac12$ respectively. So an adversary who must fix $\eta_t$ before seeing $u_t$ is caught with probability $\tfrac12$ per step by a uniformly randomizing agent.
  - $K$ is a trap, yet $\theta^\*$ is identified almost surely, in expected time 2.
  - **So T1 is a theorem about adaptive (worst-case) noise.** Against a deterministic policy, oblivious noise is no weaker, since the adversary can predict $u_t$.

## 3. Constructive policy and experiment counts

> **Theorem T2 (myopic play suffices).** Suppose $\Theta_0$ has no far trap. Let $\pi$ be any policy that, at a far $\Theta_t$, plays some $u\in\mathcal S(\Theta_t)$ informative on $\Theta_t$. Such a $u$ always exists, and $\pi$ reaches $\operatorname{diam}\Theta_t\le\varepsilon$ within $\lvert\Theta_0\rvert-1$ experiments. The bound is attained by optimal policies.

*Proof.*
- **Existence.** Every reachable $\Theta_t$ is a subset of $\Theta_0$. If it is far it is not a trap, so a safe informative $u$ exists. By definition every response to it is a proper subset, so $\lvert\Theta_{t+1}\rvert\le\lvert\Theta_t\rvert-1$.
- **Count.** Far sets have at least 2 elements, so at most $\lvert\Theta_0\rvert-1$ strict decreases occur before the set is not far.
- **Sharpness.** Take $n$ points and, for each $k$, an always-safe experiment that reveals only whether $\theta=k$. A far set remains while at least two candidates remain, and the adversary answers "no" each time. So $n-1$ experiments are necessary for every policy. This was checked for $n=3,5,8$, and on random instances the ratio of optimal count to $n-1$ reaches 1 (E003 §A). ∎

**Answer to the brief's question in §4.1.** *Every non-trap set admits a robust-safe experiment that strictly reduces its cardinality under every admissible observation.* That is the definition of a non-trap. More useful is the converse direction contained in T2: under the no-trap hypothesis, **no lookahead is needed**. Any strictly-reducing safe experiment is a correct move, because no subset reachable afterwards can be a trap.

**Optimal counts are another matter.** The least worst-case number of experiments is the attractor rank $r(\Theta_0)$, computed by dynamic programming over subsets (`Instance.value`). Its complexity is in `research/complexity_analysis.md` §6. Myopic play can use up to $\lvert\Theta_0\rvert-1$ experiments when $r(\Theta_0)=1$, e.g. when one separating experiment exists but the policy chooses equality tests.

> **Theorem T3 (one policy is instance-optimal for every $\theta^\*$).** Let $D(\theta)=\max\{\operatorname{diam}K : \theta\in K,\ K\text{ a trap}\}$, where singletons count, so $D\ge0$. Let $\pi$ play any safe informative experiment while one exists and stop otherwise. Then:
> - (a) for every $\theta^\*$ and every report sequence, $\pi$ stops within $\lvert\Theta_0\rvert-1$ steps at a set of diameter $\le D(\theta^\*)$;
> - (b) for every policy and every $\theta^\*$, the adversary, keeping its reports consistent with this fixed $\theta^\*$, can keep $\operatorname{diam}\Theta_t\ge D(\theta^\*)$ forever.
>
> In particular, $\pi$ identifies exactly the parameters outside $B=\bigcup\{K : K \text{ a far trap}\}$. Those inside $B$ are not identifiable by any policy.

*Proof.*
- (a) Each step strictly shrinks $\Theta_t$. $\pi$ stops only at a trap, and that trap contains $\theta^\*$, so its diameter is at most $D(\theta^\*)$.
- (b) Take $K\ni\theta^\*$ attaining $D(\theta^\*)$ and argue as in T1 (3)⇒(1). The reports are common to all of $K$, hence consistent with the fixed $\theta^\*$. ∎

**Reading.**
- In the finite model the **price of not knowing $\theta^\*$ is zero**: one policy is simultaneously minimax for every instance. The uniform guarantee $\max_{\theta}D(\theta)$, the largest trap diameter, follows as a corollary.
- This matches the scalar model, where maximum safe intensity is optimal (S2). T3 is weaker in one respect: it is about the terminal set, not about every horizon.
- Q-F1 of Stage 0 is closed. Whether a similarly universal policy exists in the continuum is open (`research/continuum_analysis.md` §5).

## 4. Closure properties of the trap family

Let $\mathcal T$ be the family of traps.

> **Theorem T4.**
> 1. **Restriction (hereditary).** Restricting to $\Theta'\subseteq\Theta_0$, keeping the experiments and the observation sets, gives an instance whose traps are exactly $\{K\in\mathcal T : K\subseteq\Theta'\}$.
> 2. **Products with independent experiments.** Given instances $A$ and $B$, form $A\otimes B$:
>    - the parameters are $\Theta_A\times\Theta_B$;
>    - the experiments are $\mathcal U_A\sqcup\mathcal U_B$;
>    - an experiment of $A$ is safe and observed through the $A$ coordinate only, and likewise for $B$.
>
>    Then $K$ is a trap iff both projections $\pi_AK$ and $\pi_BK$ are traps. Products and projections of traps are therefore traps. For $\varepsilon=0$, $r_{A\otimes B}=r_A+r_B$.
> 3. **Failures.** $\mathcal T$ is in general not closed under union, intersection, subsets or supersets. With *joint* experiments, where $(u_A,u_B)$ is played together and safe iff both components are, the projection of a trap need not be a trap.

*Proof.*
1. $\mathcal S(K)$ and informativeness on $K$ depend only on $K$.
2. **Trap condition.**
   - $\mathcal S(K)=\mathcal S_A(\pi_AK)\sqcup\mathcal S_B(\pi_BK)$.
   - $u\in\mathcal U_A$ is informative on $K$ iff it is informative on $\pi_AK$, since $\mathcal Y((a,b),u)=\mathcal Y_A(a,u)$. The same holds for $B$.

   **Experiment count.**
   - *Upper bound:* run an optimal $A$-strategy, then an optimal $B$-strategy.
   - *Lower bound:* the adversary answers $A$-experiments with an optimal $A$-adversary and $B$-experiments with an optimal $B$-adversary. The consistent set stays a product $\Theta^A_t\times\Theta^B_t$, and each experiment advances only one factor's game. Identification needs both factors resolved, so at least $r_A+r_B$ experiments are needed.
3. Explicit counterexamples, all verified in E003 §I:
   - *Union and supersets.* $\Theta=\{0,1,2\}$, one always-safe experiment with $\mathcal Y(0)=\{0\}$, $\mathcal Y(1)=\{0,1\}$, $\mathcal Y(2)=\{1\}$. Then $\{0,1\}$ and $\{1,2\}$ are traps and $\{0,1,2\}$ is not.
   - *Intersection.* $\Theta=\{0,1,2,3\}$, one experiment unsafe for $\{2,3\}$ that separates 0 from 1. Then $\{0,1,2\}$ and $\{0,1,3\}$ are traps, since nothing is safe for them, but $\{0,1\}$ is not.
   - *Subsets.* The cycle trap of T5 with $n=3$: $\Theta$ is a trap and no 2-subset is.
   - *Joint products.* $A=\{a_1,a_2\}$ with one always-safe separating experiment. $B=\{b\}$ with one experiment, unsafe for $b$. Then $A\times B$ is a trap, because every joint experiment is unsafe, while $\pi_A(A\times B)=A$ is identifiable. ∎

**Other transformations.**
- Relabeling parameters, experiments or symbols preserves $\mathcal T$.
- Adding experiments can only remove traps.
- Adding an experiment $u'$ that is a *garbling* of an existing $u$ — $U(u')\supseteq U(u)$, with every response of $u'$ a union of responses of $u$ — changes nothing.
- Refining observations can only remove traps.

**Reading.** The joint-product failure is the simplest genuinely coupled obstruction. Each factor is identifiable on its own, but the factors cannot be probed separately and one factor has no safe experiment at all. It is degenerate, but it isolates the mechanism a richer multidimensional model (Q-C2) would need: **safety couples coordinates even when observations do not.**

## 5. Minimal traps

For $K\subseteq\Theta_0$, the **safety-witness number** is
$$\sigma(K)=\min\{\lvert W\rvert : W\subseteq K,\ \mathcal S(W)=\mathcal S(K)\}.$$
Equivalently, $\sigma(K)$ is the minimum size of a hitting set for the nonempty traces $U(u)\cap K$. It is at most the number of experiments unsafe somewhere on $K$, and at most $\lvert K\rvert$.

> **Lemma W.** If $K$ is a far trap, then some far trap $K_0\subseteq K$ has $\lvert K_0\rvert\le\sigma(K)+2$. For $\varepsilon=0$ the bound improves to $\lvert K_0\rvert\le\max(2,\sigma(K))$.

*Proof.*
- Let $W$ be a minimum witness and $\{a,b\}\subseteq K$ a far pair. Put $K_0=W\cup\{a,b\}$.
- $W\subseteq K_0\subseteq K$ gives $\mathcal S(K)\subseteq\mathcal S(K_0)\subseteq\mathcal S(W)=\mathcal S(K)$.
- For $u\in\mathcal S(K_0)=\mathcal S(K)$, $\bigcap_{K_0}\mathcal Y(\cdot,u)\supseteq\bigcap_K\mathcal Y(\cdot,u)\ne\varnothing$. So $K_0$ is a trap, and it is far.
- For $\varepsilon=0$: if $\lvert W\rvert\ge2$, take $K_0=W$; otherwise add one point. ∎

This is the key structural lemma. It reappears as Theorem G1 in `research/geometric_obstructions.md`.

> **Theorem T5 (cardinality of minimal traps; $\varepsilon=0$).**
> - (a) If $K$ is a minimal trap with $\lvert K\rvert\ge3$, then $\sigma(K)=\lvert K\rvert$. Hence at least $\lvert K\rvert$ experiments are unsafe for some member of $K$, and each member of $K$ is the only member of $K$ in the unsafe set of some experiment.
> - (b) For every $n\ge3$ there is an instance with $n$ parameters, $n$ experiments and deterministic **binary** observations whose only trap of size $\ge2$ is $\Theta_0$. Every proper subset is identified with one experiment.
>
> So the minimum number of experiments needed to realize a minimal trap of cardinality $n\ge3$ is exactly $n$, and binary deterministic observations suffice.

*Proof.*
- **(a)**
  - By Lemma W a trap of size $\le\max(2,\sigma(K))$ lies inside $K$. Minimality and $\lvert K\rvert\ge3$ force $\sigma(K)=\lvert K\rvert$.
  - A hitting set must then use every element. So for each $\theta\in K$ some trace $U(u)\cap K$ is exactly $\{\theta\}$; otherwise $K\setminus\{\theta\}$ would still hit every trace.
  - These $\lvert K\rvert$ traces are distinct, so the experiments are distinct.
- **(b) The cycle trap.**
  - *Construction.* Experiment $a_j$ ($j\in\mathbb Z_n$) is unsafe only for $j$ and reports whether $\theta=j+1$.
  - *$\Theta_0$ is a trap,* vacuously: every experiment is unsafe for some member.
  - *Proper subsets are not traps.* Let $K'\subsetneq\Theta_0$ with $\lvert K'\rvert\ge2$.
    - Going around the cycle, some $j\notin K'$ has $j+1\in K'$.
    - Then $a_j$ is safe for $K'$ and splits $\{j+1\}$ from the rest of $K'$. Every response is identified or smaller, and repeating the argument identifies $\theta^\*$.
    - In fact every proper subset of size $\ge2$ has value 1 for $n\le8$: verified exhaustively (E003 §H).
  - Stage 0's F5 used $n-1$ observation values; binary observations suffice. ∎

**Reading.** The arbitrarily large minimal traps of Stage 0 are explained exactly by $\sigma$. A minimal trap of size $n$ is a set where **every member is individually responsible for blocking some experiment**. The obstruction disappears as soon as any single member is excluded, and no safe experiment can exclude one. Large minimal traps require many distinct experiments with singleton unsafe traces. Bounded $\sigma$ forces small minimal traps, and gives polynomial algorithms (`research/complexity_analysis.md` §4).

## 6. Realizability

> **Theorem T6 (universality).** Let $\mathcal N$ be any family of subsets of $\Theta_0$ of size $\ge2$. Some instance has exactly $\mathcal N$ as its non-traps of size $\ge2$. The construction uses $\lvert\mathcal N\rvert$ experiments, each with an alphabet of size at most $\lvert\Theta_0\rvert$.

*Proof.*
- For each $N\in\mathcal N$, take an experiment $u_N$ unsafe exactly outside $N$, with alphabet $N$ and $\mathcal Y(\theta,u_N)=N\setminus\{\theta\}$ for $\theta\in N$. Parameters outside $N$ get any symbol; they are never in a set for which $u_N$ is safe.
- $u_N$ is safe for $K$ iff $K\subseteq N$, and then $\bigcap_K\mathcal Y=N\setminus K$. So $u_N$ kills exactly $N$.
- The non-traps are the union of the killed sets, which is $\mathcal N$. ∎

Verified for all $2^{11}$ families on 4 points (E003 §J).

**So trap families carry no combinatorial structure in general.** Every structural statement needs a restriction on safety or on observations. The natural observation restriction is a Helly number. With interval observations, exactly 1218 of the 2048 families on 4 points are realizable. The characterization is Theorem G2 in `research/geometric_obstructions.md`.

## 7. What changed relative to Stage 0

- F1 and F2 hold for arbitrary set-valued observations; Stage 0 stated them for intervals. The proof of F3 (the unconstrained case) never needed Helly's theorem; see `research/complexity_analysis.md` §2.
- F5 (non-locality) is strengthened to T5: exact minimum experiment count, and binary observations.
- Q-F1 is resolved by T3.
- A latent bug in Stage 0 was never triggered there. Its random 3-SAT generator drew distinct variables, so repeated literals were not exercised. My first Stage 1 encoding did break on them: it summed bitmasks instead of OR-ing them, and the exhaustive check caught it (E003). The Stage 0 code itself used Python sets and was correct.

## 8. Literature status

- **T1** is the standard minimal-losing-set / attractor argument on the knowledge-state lattice. No contribution is claimed for the technique.
- **The deterministic special case is known.** A static instance is a *partially specified FSM* (Hierons–Türker 2014) whose transitions are all self-loops:
  - an experiment undefined in a state is an unsafe experiment;
  - their adaptive distinguishing sequence must apply only inputs "defined in all states" of the current set, which is robust safety;
  - with deterministic outputs, existence of an adaptive distinguishing sequence for a partially specified FSM is exactly T1 at $\varepsilon=0$, and they prove it polynomial.
- **Static, nondeterministic outputs with partial inputs** appear to be covered only by much more general dynamic results: Alur–Courcoubetis–Yannakakis 1995 (EXPTIME-complete, seen only through secondary summaries) and Türker et al. 2023 (PSPACE-hard, not read).
- **T2, T3, T5, T6** have not been located in the sources read. T3 is simple enough that I expect it is folklore somewhere in adaptive testing. I record it as *potentially known*.
