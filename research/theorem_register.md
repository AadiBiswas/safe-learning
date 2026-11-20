# Theorem register

*Stage 0, 2026-11-20. IDs are stable: a result keeps its ID if it is later strengthened, refuted or found in the literature, and the status column records the change.*

**Status codes:**
- **P**: proved in this repository;
- **P-std**: proved here, but by a standard argument (no contribution claimed);
- **N**: numerical evidence only;
- **C**: conjecture;
- **O**: open question;
- **R**: refuted;
- **K**: known in the literature.

**Abbreviations.** SA = `research/scalar_analysis.md`, FA = `research/finite_analysis.md`, RD = `research/research_directions.md`, LR = `research/literature_review.md`.

## Scalar model ($\theta^\* x \le 1$; $Y = \theta^\* x^p + \eta$, $|\eta| \le \delta$)

| ID | Statement | Status | Proof | Checks |
|---|---|---|---|---|
| S1 | One experiment at $x > 0$: the adversary can produce exactly the sets $\Theta_t \cap I$, with $I$ any closed interval of length $2\delta x^{-p}$ containing $\theta^\*$. | P | SA §2 | — |
| S2 | Maximum safe intensity $x_t = 1/U_t$ is worst-case optimal for every inclusion-monotone objective, at every horizon, instance-wise and uniformly. Consequently no policy separation exists in the scalar model. | P (elementary coupling) | SA §3 | `scalar_check` §C: 80,000 coupled steps, 0 violations |
| S3 | Instance-wise: $\eta \equiv \delta$ maximises $U_T$, so $U_{t+1} = \min(U_t, \theta^\* + 2\delta U_t^p)$; and $L_t = \theta^\*$ for all $t \ge 1$. Any $\vert\eta_t\vert \le \delta$ is consistent. | P | SA §4 | §D |
| S4 | Full fixed-point and basin structure for every $p > 0$. The threshold is $\lambda_c = (p-1)^{p-1}/p^p$ for $p > 1$; $8\delta\theta^\* = 1$ and $U_\pm = (1 \pm \sqrt{1 - 8\delta\theta^\*})/(4\delta)$ at $p = 2$; $\delta = 1/2$ at $p = 1$; no threshold for $p < 1$. | P | SA §5 | §A, §B, §F, §G |
| S4a | At $\lambda = \lambda_c$ nothing moves. The passage time from $v_c$ is $\Theta\bigl((\lambda_c - \lambda)^{-1/2}\bigr)$, equal to $\operatorname{artanh}(s)/\sqrt{\lambda_c - \lambda}$ at $p = 2$ (normal-form calculation). | P (normal form) + N | SA §6 | §F: fitted exponent −0.506; constant 2.646 against 2.647 |
| S4b | The asymptotic upper bound is discontinuous in $\delta$ and in $U_0$ at the unstable fixed point $v_+$. | P | SA §7 | — |
| S5 | **Uniform one-shot trap.** $\inf_\pi\sup_{\theta^\*,\eta}\operatorname{diam}\Theta_T = \min(U_0 - L_0, 2\delta U_0^p)$ for every $T \ge 1$, attained at $T = 1$. | P | SA §8 | §E |
| S6 | Total deadlock iff $2\delta U_0^p \ge U_0 - L_0$. For $p > 1$ and $L_0 \ge 0$ it is implied by $U_0 \ge (2\delta)^{-1/(p-1)}$. | P | SA §8 | — |
| S7 | Favourable data ($+\delta$ then $-\delta$) identify $\theta^\*$ exactly in two experiments. | P | SA §9 | §H |
| S8 | The instance-wise asymptotic set $[\theta^\*, \theta^\* v_-]$ satisfies the trap condition with equality. | P | SA §8 | — |

## Finite spaces (Direction B)

| ID | Statement | Status | Proof | Checks |
|---|---|---|---|---|
| F1 | Uniform $\varepsilon$-identifiability holds iff there is no trap of diameter $> \varepsilon$. | P-std (attractor / minimal losing set) | FA §2 | `finite_game`: 3,000/3,000 random instances agree |
| F2 | An optimal policy uses at most $\vert\Theta_0\vert - 1$ experiments, and every one of its experiments strictly shrinks the set. Tight. | P | FA §2 | ratio 1.000 attained |
| F3 | Without safety constraints, with interval observations: identifiable iff every far pair is separated by some action. Polynomial. | P | FA §3 | — |
| F4 | With robust safety and interval observations: trap existence ($\varepsilon = 0$) is NP-complete; identifiability is coNP-complete. | P (3-SAT reduction) | FA §3 | 400/400 random 3-SAT instances (232 satisfiable) |
| F5 | **Non-locality.** For every $n$ there is a trap of size $n$ with every proper subset identifiable in one experiment. In particular, pairwise safe distinguishability does not imply safe identifiability. | P | FA §3 | $n \le 7$ checked; 30/3,000 random instances are pairwise-OK but not identifiable |

## Multidimensional (Direction C)

| ID | Statement | Status | Proof | Checks |
|---|---|---|---|---|
| C1 | Linear observation $\theta^\top u$, linear safety $\theta^\top u \le 1$, $u \ge 0$, $\Theta_0 \subset \mathbb R^d_{>0}$: $K$ is a trap iff every coordinate projection is a scalar trap, $\min K_i \ge (1 - 2\delta)\max K_i$. Coupling creates no new traps. | P | RD, Direction C | `tests/test_linear_traps.py` (random point sets) |
| C1a | If negative action components are allowed while $\Theta_0 \subset \mathbb R^d_{>0}$, then identification is immediate (unbounded safe scaling). | P (one line) | RD, Direction C | — |

## Conjectures and open questions

| ID | Statement | Status |
|---|---|---|
| Q-F1 | One policy identifies exactly those $\theta^\*$ contained in no trap of diameter $> \varepsilon$ (the instance-wise version of F1). | O |
| Q-F2 | Trap detection is polynomial for threshold-monotone safety, for linear structures, and for other natural classes. A dichotomy? | O |
| Q-F3 | Continuum: the worst-case asymptotic diameter equals $\sup\operatorname{diam}$ over closed traps (compact $\Theta_0$, continuous $g$, $h$). | C (holds in the scalar model: S5, S8) |
| Q-F4 | The minimum number of experiments is NP-hard to approximate within $o(\log n)$ (via test cover). | C |
| Q-C2 | Genuinely $d$-dimensional traps exist when safety and observation use different linear functionals of $\theta$. | C |
| Q-C3 | There is a safe-identification model with a large *uniform* adaptivity gap. In the scalar model there is none. | O |
| Q-E1 | The risk-allowance frontier is continuous at $\epsilon = 0$ under bounded noise. | O (model not yet fixed) |

## Refuted or corrected (from the brief)

| Item | Correction |
|---|---|
| "Ability to reduce the upper bound depends on $8\delta\theta^\* < 1$" (read as a learnability criterion) | True **instance-wise** only. The criterion involves the unknown $\theta^\*$. The uniform worst case has no threshold (S5). |
| Tracking only the upper endpoint | Under the same worst case the lower endpoint is identified exactly at $t = 1$ (S3). |
| "A deliberately less informative experiment may be better" (as a scalar possibility) | Refuted in the scalar model (S2). Still open in richer models. |
| "Each coordinate identifiable but not the vector" (as a linear-model possibility) | Refuted for the natural linear model at the level of traps (C1). Still open for richer models (Q-C2). |

## Literature status

See LR §2. Nothing here is labelled novel. F1 is standard in technique. F4 and F5 are "potentially distinct", pending the active-diagnosis complexity literature (Haar–Haddad–Melliti–Schwoon) and safe diagnosability (Paoli–Lafortune).
