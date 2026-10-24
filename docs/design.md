# Football Urn Model — Design

## Purpose

Simulate football matches as a game of drawing balls from urns, so that simulated seasons look like real Premier
League seasons. Each team's skill is the number of red balls in its skill pool.

## Goals

1. **Realistic:** simulated shots, xG values and results match real Premier League data (see
   [data-analysis.md](data-analysis.md)).
2. **Physically playable:** every random step is a draw of balls from an urn, so a match could be played with real
   urns and balls. No step may use a fitted function or continuous distribution.
3. **Skill separate from form:** skill is the skill pool, which changes slowly and only as set by whoever runs the
   simulation. Matchday form is the match urn, a separate and faster source of randomness.
4. **Ready for inference later:** every probability in the model can be written down exactly, so that a later
   project can infer the red balls in each skill pool from observed data. Inference is not part of this project.

## Fundamental approximation

A team has one skill. A match is then a two-dimensional affair: it depends on the home team's skill and the away
team's skill, or equivalently on the skill difference and the skill sum. The difference and the sum are therefore
taken to cover all dependencies on skill. Home advantage makes the order matter, so the difference has a sign.

Real skill cannot be observed, so the project use uses final points of a season as a skill proxy. This way the project can assess if variables are dependent on skill and roughly how.

## Notation

- M = total number of balls in a container, m = number of red balls in it. The subscript names the container:
  s = skill pool, u = match urn, t = tempo urn.
- k = number of balls drawn. The subscripts names the context:
  w = phase 4, c = attacking team during phase 5, d = defending team during phase 5.
- n = rounds per match, μ = average number of shots per match, $b$ = big-chance margin (red balls).
- Marked balls: $m_h$ = extra red h-marked balls for the home team, $M_{xo}$ = extra x-marked balls added to the shot urn for ordinary chance, $m_{xo}$ = extra red x-marked balls added to the shot urn for ordinary chance, $M_{xb}$ = extra x-marked balls added to the shot urn for big chance, $m_{xb}$ = extra red x-marked balls added to the shot urn for big chance.

## Chapters

This is basic training: the model is fitted to the basic observations of a match. Each chapter covers one part of a match and names its observables. It describes the model (the rules are in the [README](../README.md#how-to-play)) and gives equations for each observable given the output of the previous phase. Then, for each observable, it compares real and simulated data in a 3×3 grid of skill proxy sum and difference (terciles): a figure in [data-analysis.md](data-analysis.md), tables of matches, mean, standard deviation and skewness per panel (real / sim, with all matches and the theory above each table), a short evaluation and a one-sentence verdict. Phase 1 (skill change) is an input to the simulation, and phase 2 (match urn) and final points are left out for now.

## Shot (phase 3)

Observable: total shots per match.

### Model

[README step 3](../README.md#how-to-play): one draw from the tempo urn in each of the n rounds. Parameters: n,
$M_t$, $m_t$.

### Equations

The tempo urn does not depend on the earlier phases. With $p = m_t / M_t$:

- The total number of shots is binomially distributed. Its variance is always below its mean, and grows towards the mean as n grows.
- Mean: $\mu = n p$
- Standard deviation: $\sigma = \sqrt{n p (1 - p)} = \sqrt{\mu - \mu^2 / n}$
- Skewness: $\frac{1 - 2p}{\sigma}$

### Total shots per match

Simulated 100 seasons with $n = 100$ and $m_t = 1$ and $M_t = 4$ ($p = 0.25$), and compared against the real Premier League 2025/26 season. See analysis 6 in [data-analysis.md](data-analysis.md)

**Matches** (real / sim)

All matches (real / sim): 380 / 38000

| Sum \ difference | low [-65 to -8 pts] | mid [-7 to 8 pts] | high [9 to 65 pts] |
| --- | --- | --- | --- |
| high [112 to 163 pts] | 55 / 5086 | 19 / 4899 | 52 / 4797 |
| mid [97 to 111 pts] | 28 / 4028 | 70 / 4686 | 24 / 3796 |
| low [42 to 96 pts] | 50 / 3881 | 37 / 3153 | 45 / 3674 |

**Mean** (real / sim)

All matches (real / sim / theory): 24.96 / 24.99 / 25.00

| Sum \ difference | low [-65 to -8 pts] | mid [-7 to 8 pts] | high [9 to 65 pts] |
| --- | --- | --- | --- |
| high [112 to 163 pts] | 24.98 / 25.01 | 27.32 / 25.00 | 25.77 / 25.02 |
| mid [97 to 111 pts] | 24.00 / 24.95 | 24.43 / 25.07 | 23.96 / 25.08 |
| low [42 to 96 pts] | 24.72 / 24.87 | 25.00 / 25.02 | 25.16 / 24.87 |

**Standard deviation** (real / sim)

All matches (real / sim / theory): 5.43 / 4.33 / 4.33

| Sum \ difference | low [-65 to -8 pts] | mid [-7 to 8 pts] | high [9 to 65 pts] |
| --- | --- | --- | --- |
| high [112 to 163 pts] | 4.32 / 4.35 | 6.07 / 4.34 | 5.27 / 4.29 |
| mid [97 to 111 pts] | 7.06 / 4.28 | 4.91 / 4.31 | 5.24 / 4.44 |
| low [42 to 96 pts] | 5.99 / 4.30 | 5.12 / 4.46 | 5.89 / 4.26 |

**Skewness** (real / sim)

All matches (real / sim / theory): 0.23 / 0.12 / 0.12

| Sum \ difference | low [-65 to -8 pts] | mid [-7 to 8 pts] | high [9 to 65 pts] |
| --- | --- | --- | --- |
| high [112 to 163 pts] | -0.19 / 0.15 | -0.66 / 0.15 | 0.58 / 0.18 |
| mid [97 to 111 pts] | 0.28 / 0.03 | -0.30 / 0.08 | 0.41 / 0.15 |
| low [42 to 96 pts] | 0.30 / 0.03 | 0.52 / 0.19 | 0.74 / 0.11 |

The simulated mean, standard deviation and skewness match the theory, which confirms the equations. The mean fits the real data within about one shot in every panel except the thinnest (high sum, mid difference, 19 matches). The standard deviation is too small in 8 of 9 panels (real 4.3–7.1, simulated 4.3–4.5), and the theory shows that the tempo urn cannot reach the real 5.43. The real skewness jumps between panels (−0.66 to 0.74), which with 19–70 matches per panel is mostly noise, but over all matches it is higher than the model's (0.23 against 0.12).

Verdict: the mean fits, but the spread of total shots between matches is too small, and the tempo urn alone cannot fix it.

## Attack/defend (phase 4)

Observables: home share of shots per match.

### Model

[README step 4](../README.md#how-to-play): both teams grab $k_w$ balls from their match urns; the one with the
most red balls gets the shot. If they have equal red balls, they draw one more ball each until one gets red and the
other white. Parameters: $k_w$, and through the match urns $m_s$, $M_s$, $M_u$, $m_h$.

### Equations

Given the match urns:

- Distribution: [eq]
- Mean: [eq]
- Variance: [eq]

Averaged over the match urns (phase 2): [eq]

$k_w$ and the difference in red balls between teams both set how uneven the split of shots is. A larger $k_w$ gives
the better team a bigger share, and more so when $M_u$ is small, since grabbing $k_w$ of a small match urn reveals
more of it. Example share of shots for A, $M_u$ = 20:

| A red share | B red share | $k_w$ = 1 | $k_w$ = 3 | $k_w$ = 5 | $k_w$ = 10 |
| --- | --- | --- | --- | --- | --- |
| 0.55 | 0.45 | 0.60 | 0.64 | 0.67 | 0.77 |
| 0.60 | 0.40 | 0.70 | 0.76 | 0.81 | 0.93 |
| 0.30 | 0.20 | 0.64 | 0.67 | 0.71 | 0.82 |
| 0.15 | 0.10 | 0.62 | 0.64 | 0.66 | 0.76 |

### Home share of shots per match

| Home share of shots | Skill proxy difference | Skill proxy sum |
| --- | --- | --- |
| Mean | Depends (analysis 1) | Not checked |
| Variance | Not checked | Not checked |
| Shape | Not checked | Not checked |

The mean goes from X to Y rather linearly with changing skill proxy difference. For a given set of skills the
distribution looks like X.

Figure: [3×3 grid, real vs simulated]

Verdict: [one short sentence]

## xG (phase 5)

Observables: xG per shot, ordinary shots and big chances in one distribution.

### Model

[README step 5](../README.md#how-to-play): the xG is modelled in two ways, ordinary chance and big chance. If the
team won the shot (phase 4) by $b$ (the big-chance margin) or more red balls, it is a big chance. A shot urn is
filled with balls:

- x-marked balls: $M_x$ of them, $m_x$ red. $M_x$, $m_x$ = $M_{xb}$, $m_{xb}$ for a big chance and $M_{xo}$,
  $m_{xo}$ for an ordinary chance.
- The attacking team draws $k_c$ balls from its match urn and gets $R_1$ red balls.
- The defending team draws $k_d$ balls from its match urn and gets $R_2$ red balls.
- The defender's red balls cancel the attacker's red balls: $c = \min(R_1, R_2)$ red balls are removed.
- The remaining $k_c - c$ drawn balls are placed in the shot urn together with the marked balls.

$$\text{xG} = \frac{m_x + R_1 - c}{M_x + k_c - c}$$

Parameters: $k_c$, $k_d$, $M_{xo}$, $m_{xo}$, $M_{xb}$, $m_{xb}$, and through the big chances $b$ and $k_w$.

### Equations

Given the match urns and who shoots:

- Ordinary chance: distribution [eq], mean [eq], variance [eq]
- Big chance: distribution [eq], mean [eq], variance [eq]
- All shots, ordinary and big chances together: distribution [eq], mean [eq], variance [eq]

### xG per shot

| xG per shot | Skill proxy difference | Skill proxy sum |
| --- | --- | --- |
| Mean | Depends (analysis 2) | Not checked |
| Variance | Not checked | Not checked |
| Shape | Not checked (analysis 2 shows the whole distribution shifting, but not standardised) | Not checked |

The distribution looks like X.

Figure: [3×3 grid, real vs simulated]

Verdict: [one short sentence]

## Goal (phase 6)

Observables: goals per team per match.

### Model

[README step 6](../README.md#how-to-play): one ball is drawn from the shot urn; red (or marked red) is a goal. A
shot's xG is therefore exactly the probability that it becomes a goal. No parameters of its own.

### Equations

Given the xG of each shot:

- Distribution: [eq]
- Mean: [eq]
- Variance: [eq]

### Goals per team per match

| Goals per team per match | Skill proxy difference | Skill proxy sum |
| --- | --- | --- |
| Mean | Not checked | Not checked |
| Variance | Not checked | Not checked |
| Shape | Not checked | Not checked |

The distribution looks like X.

Figure: [3×3 grid, real vs simulated]

Verdict: [one short sentence]

## Result

Observables: home win, draw, away win.

### Model

The result follows from the goals of both teams. No parameters of its own.

### Equations

Given the goals of both teams:

- Probability of a home win, a draw and an away win: [eq]

### Home win, draw, away win

| Home win, draw, away win | Skill proxy difference | Skill proxy sum |
| --- | --- | --- |
| Rates | Not checked | Not checked |

Figure: [3×3 grid, real vs simulated]

Verdict: [one short sentence]

## Parameters

The current values are in `model_settings()` in `src/football_urn_model/simulate.py`. Goal and Result have no
parameters of their own.

| Parameter | Symbol | Chapters, and what it changes |
| --- | --- | --- |
| Red balls in a team's skill pool | $m_s$ | Attack/defend: home share of shots; xG |
| Balls in the skill pool | $M_s$ | Attack/defend: spread of the home share between matches (form); xG |
| Balls in the match urn | $M_u$ | Attack/defend: home share of shots and its spread; xG |
| Extra red balls for the home team | $m_h$ | Attack/defend: home share of shots; xG: home xG |
| Rounds per match | n | Shot: mean and variance of total shots |
| Balls and red balls in the tempo urn | $M_t$, $m_t$ | Shot: mean and variance of total shots |
| Balls grabbed to decide who shoots | $k_w$ | Attack/defend: home share of shots; xG: through big chances |
| Big-chance margin | $b$ | xG: through big chances |
| Chance balls drawn by the shooting team | $k_c$ | xG |
| Balls drawn by the defending team | $k_d$ | xG |
| x-marked balls and red x-marked balls, ordinary shot | $M_{xo}$, $m_{xo}$ | xG of ordinary shots |
| x-marked balls and red x-marked balls, big chance | $M_{xb}$, $m_{xb}$ | xG of big chances |
