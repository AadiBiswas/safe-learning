# Stage 4 — Mathematical audit of Stages 0–3

*2026-11-24. For each area I re-derived the result from its definitions and record either "verified" or the correction made. Corrections are applied in the source documents, with a dated note there. D2 has its own audit in `research/planar_hardness_audit.md`.*

## 0. Corrections made in Stage 4

| # | Item | Problem | Correction |
|---|---|---|---|
| C1 | D2, constant "always safe" experiments | $a=0$, $b=0$ was safe only at equality: no strict margin | $b=1$; no unsafe set changes; E006 output unchanged |
| C2 | D2 experiment count | stated $\le7n+13m$ | exactly $5n+11m'+(m-m')\le5n+11m$ |
| C3 | B4 / Stage 3 report, "hardness needs a lone forbidden pair" | stated as if a theorem about all observation models | reformulated: lone pairs are the negation primitive of every known reduction; deterministic models have none and are P; general status open (D-O2). See `complexity_map.md` §4 |
| C4 | W5 ($\sigma$ NP-hard in $d=3$) | depends on an unread citation (Johnson 1982) | kept, and supplemented by **W5′**: $\sigma$ is NP-hard in $\mathbb Q^4$ by a self-contained proof (vertex cover on moment-curve pairs, R4(c)) |
| C5 | E005 §C generator | per-component rescaling, so the instances did not have 1–3 rays as described | recorded in the ledger (Stage 3). The check's conclusion is unaffected. |
| C6 | Stage 2 L7 wording | "essentially optimal in form" | corrected in Stage 3: W[1]-hardness excludes FPT, not the exponent |

**No proved theorem was found to be false.**

## 1. Finite trap theory

**T1 (characterization). Verified.**

*Quantifier order:* for all $\theta^\*$, for all adaptive report sequences.
- **Adaptive adversary.** The report $y_t$ may depend on $u_t$ and the history, and the lazy-adversary reduction uses exactly this.
- **Fixed true parameter.** It is consistent with the proof, since trap-holding reports are common to all of $K\ni\theta^\*$.
- **Randomized policies.** The trap is held on every sample path, so randomization does not help against adaptive noise.
- **Oblivious noise.** It is a different model: example Ob shows a randomizing agent escaping a trap with probability 1.
- **Exact versus approximate.** "Far" is $\operatorname{diam}>\varepsilon$, and success is $\operatorname{diam}\le\varepsilon$; at $\varepsilon=0$ this is singleton identification.
- **Observation generality.** T1 needs no Helly property.

**T2, T3. Verified.** A myopic policy terminates within $n-1$ steps at a trap containing $\theta^\*$, so $D(\theta^\*)$ is achieved. The lower bound comes from the adversary holding the maximal trap containing $\theta^\*$.

**T4. Verified, including the counterexamples.**
- Independent products have additive counts: the lower bound holds because the adversary plays the two factor games independently and each experiment advances one factor.

**T5, Lemma W. Verified, for general set-valued observations at $\varepsilon=0$.**
- *Cardinality restriction.* $\sigma(K)=\lvert K\rvert$ holds for minimal traps with $\lvert K\rvert\ge3$. For $\lvert K\rvert=2$ it can fail trivially, since any pair with no blocked experiment is a minimal trap with $\sigma=0$.
- *For $\varepsilon>0$*, minimal far traps have size $\le\sigma+2$, and the equality $\sigma=\lvert K\rvert$ is not claimed.
- *Minimum experiment count.* The bound "$\ge\lvert K\rvert$ experiments unsafe on $K$" follows because each member must be the only member of some trace.

**G1′ (local to global, $\varepsilon=0$). Verified.**

**T6 and G2b (realizability). Verified.** G2b's necessity direction uses the Helly number of the observation family *of each experiment*.

## 2. Complexity, finite

**Verified:**
- **M** (membership);
- **B1** (no safety ⇒ pairwise; diameter goals; explicit representations);
- **H1(a–d)** (degenerate formulas audited in Stage 1);
- **P2** (known);
- **P3** (Horn);
- **P4, P5.**

**Restrictions.**
- H1(c) uses $\delta=\tfrac35$. The touching-endpoint encoding with $\delta=\tfrac12$ (R7) also works.
- OPTCOUNT's NP-hardness without safety is cited (A), not proved here.

## 3. Linear and geometric results

**L1–L5, L8. Verified.**
- Safety is at equality and intervals are closed. Strict variants are discussed in L1.
- **L3** (convex position) needs hull invariance, so it is specific to the linear model. Stage 1's general σ results do not need it.
- **L4.** Verified: the interior point is necessary for a *minimum* witness. Hull invariance holds for traps, not for witness optimization.

**L6, L7. Verified.**
- They need unbounded dimension.
- L7(b)'s parameter is the number of positive rays. Opposite rays count separately.

**L9. Verified for $n\ge4$.** This is a large-minimal-trap statement only. It says nothing about complexity, which is open in the plane (AL-O1).

**W1–W4. Verified.**
- W1's constant-safety convention: a blocked constant experiment counts once, and only if there are no blocked rays.
- W4(c) is cited (A).
- W4(b) is proved, with complexity $O(k\,m\log m)$.

**W5. Cited.** **W5′ (new, proved).**
- *Construction.* For any graph $G$, put its vertices on the moment curve in $\mathbb Q^4$ at integers. Each edge $\{i,j\}$ is the trace of $\{-(t-t_i)^2(t-t_j)^2>-\tfrac12\}$ (R4(c)).
- *Consequence.* $\sigma(\Theta_0)$ equals the minimum vertex cover of $G$, so computing $\sigma$ is NP-hard in $\mathbb Q^4$, with polynomial bits and convex position.

**D1, D5, R1–R7. Verified.**
- D5 uses only the observation lines, so it holds for every safety structure.
- R5(c) is cited (A).

**D2, D3, D4.** See `planar_hardness_audit.md`. **They survive, with C1 and C2 applied.**

**AL0–AL4. New in Stage 4; verified** (`aligned_identifiability.md`).

## 4. Scalar model

**Verified:**
- the recurrence $U_{t+1}=\min(U_t,\theta^\*+2\delta U_t^p)$, with worst case $\eta\equiv\delta$ (S3);
- the fixed points and basins for every $p>0$ (S4);
- max-intensity optimality by coupling (S2);
- the uniform one-shot value $\min(U_0-L_0,2\delta U_0^p)$ (S5), consistent with K2 on the continuum;
- total deadlock (S6);
- the fold asymptotics S4a′, with explicit hypotheses on start and target.

**The distinctions that must be preserved, as kept in `scalar_analysis.md`:**
- the **instance-wise upper-bound threshold** $\lambda_c$, which depends on the unknown $\theta^\*$;
- the **one-sided stagnation**: the lower endpoint is identified at $t=1$;
- **total deadlock**: nothing is learned in the worst case;
- the **uniform minimax value**, which has no threshold and is reached in one step.

**The $\lambda_c$ transition is not a transition in uniform minimax learnability.** The scalar section of the manuscript must say so.

## 5. Continuum theory

**K1–K3. Verified.**
- Compactness of $\Theta_0$, $\mathcal U$ and $\mathsf Y$; continuity of $g$; a closed observation graph; (L).
- Traps are closed sets with the common-observation property for every safe experiment.
- $\varepsilon>0$, with success "$\operatorname{diam}<\varepsilon$" in finite time and failure "trap of diameter $\ge\varepsilon$".
- K3: eventual implies uniform under (L).

**Counterexamples.** Each is checked against the hypotheses it is meant to isolate:

| Example | Compact | $g$ continuous | Closed graph | (L) | Joint continuity | What it shows |
|---|---|---|---|---|---|---|
| X1 | ✓ | ✓ | ✓ | **✗** | ✓ | without (L), K1 fails |
| X2 | ✓ | ✓ | ✓ | ✓ | ✓ | sharpness of "$<\varepsilon$" at $\varepsilon=D^\*$ |
| X3 | ✓ | ✓ | **✗** | ✓ | ✗ (only at the graph defect) | without a closed graph, the supremum is not attained |
| X4 | ✓ | **✗** (jointly) | n/a | n/a | **✗** | eventual ≠ uniform without joint continuity |

X4 also fails (L) in its natural topology. It is presented as "without joint continuity" and makes no claim about (L) alone. Whether (L) is needed for K3 is Q-K1, which is open.

**Q1, Q1′, Q2. Verified.** The meaning of
$$T(\varepsilon)\le\operatorname{Pack}\bigl(\Theta_0,\mu(\varepsilon)/4L_h\bigr):$$
- **The packing number** $\operatorname{Pack}(\Theta_0,r)$ is the largest cardinality of a subset with pairwise distances $\ge r$. Removed balls are open, so successive centres are at distance $\ge r$.
- **The margin** is $\mu(\varepsilon)=\min\{\Delta(K) : K\text{ closed},\ \operatorname{diam}K\ge\varepsilon\}$, with $\Delta(K)=\sup_{u\in\mathcal S(K)}[w_K(u)-2\delta_u]$. The minimum exists by lower semicontinuity under (L) and joint continuity.
- **The constant 4:** the supremum may not be attained, so the margin used is $\mu/2$, and the ball radius is $(\mu/2)/(2L_h)$.
- **Uniformity** is over all closed sets of diameter $\ge\varepsilon$, which contain every reachable set.
- **Boundary:** at $\varepsilon\le D^\*$, $\mu(\varepsilon)\le0$ and the bound is void, as it must be.
- **Necessity:** the bump family (exponent $d$, scale $L_h/\mu$), and X2 variants (no margin ⇒ unbounded horizons at fixed $d$, $D$, $L_g$, $L_h$).
- **Classical inputs:** covering and packing volume bounds only.

**A1–A4, CandA, CandB, X5. Verified.**
- A1 and the sharp exponent in A2 are classical. The sharp upper exponent $(d-1)/2$ is cited from Dudley / Bronshteyn–Ivanov through secondary sources (A).
- The certificate statements A3–A4 are the safe-learning consequences, and are proved.

## 6. Internal consistency

- **D2 and W4:** $\sigma$ is polynomial in the plane while TRAP is coNP-complete. No conflict: different problems.
- **D2 and L3:** D2's traps lie on a circle, so they are in convex position, consistent with L3.
- **AL2 and D2:** they share an experiment family but differ in alignment. Consistent, with AL1 as the hinge.
- **AL3 and AL2:** AL3's gadgets have *effective* lone pairs with nonempty unsafe sets, which AL2's family excludes.
- **K2 and S5:** the scalar model satisfies Lemma 0, and K2 recovers S5's value.
- **T2's bound $n-1$ and Q1's packing bound** coincide for finite $\Theta_0$ at small scales: the packing number is $\le n$.
