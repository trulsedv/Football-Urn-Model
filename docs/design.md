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

This is basic training: the model is fitted to the basic observations of a match. Each chapter covers one part of a match and names its observables. It describes the model (the rules are in the [README](../README.md#how-to-play)) and gives equations for each observable given the output of the previous phase. Then, for each observable, it compares real and simulated data in a 3×3 grid of skill proxy sum and difference (terciles): a figure, tables of mean, standard deviation and skewness per panel (real / sim, with all matches and the theory above each table), a short evaluation and a one-sentence verdict. Phase 1 (skill change) is an input to the simulation, and phase 2 (match urn) and final points are left out for now.

The real data are the Premier League seasons 2023/24, 2024/25 and 2025/26 (Understat), with each team's final points in its own season as the skill proxy. Each real season's fixture list is simulated 100 times, with red balls $m_s$ from 10 (weakest team) to 25 (strongest team), scaled linearly with the real final points, and the simulated final points as the skill proxy. The tables and figures are made with `uv run chapters` (analyses 6 and 7 in [data-analysis.md](data-analysis.md)). The match-level chapters share the same matches in each panel:

**Matches** (real / sim)

All matches (real / sim): 1140 / 114000

| Sum \ difference | low [-75 to -11 pts] | mid [-10 to 11 pts] | high [12 to 75 pts] |
| --- | --- | --- | --- |
| high [116 to 180 pts] | 136 / 10408 | 99 / 15848 | 133 / 9764 |
| mid [96 to 115 pts] | 114 / 13317 | 164 / 20925 | 108 / 12500 |
| low [34 to 95 pts] | 142 / 9843 | 107 / 12113 | 137 / 9282 |

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

Simulated with $n = 100$, $m_t = 1$ and $M_t = 4$ ($p = 0.25$), and compared against the three real seasons. Figure: `output/shot_grid.html`.

**Mean** (real / sim)

All matches (real / sim / theory): 26.14 / 24.97 / 25.00

| Sum \ difference | low [-75 to -11 pts] | mid [-10 to 11 pts] | high [12 to 75 pts] |
| --- | --- | --- | --- |
| high [116 to 180 pts] | 26.18 / 24.95 | 26.54 / 25.03 | 26.99 / 24.92 |
| mid [96 to 115 pts] | 25.75 / 24.98 | 25.19 / 24.96 | 26.55 / 24.96 |
| low [34 to 95 pts] | 26.07 / 25.02 | 26.16 / 24.96 | 26.20 / 24.91 |

**Standard deviation** (real / sim)

All matches (real / sim / theory): 6.01 / 4.34 / 4.33

| Sum \ difference | low [-75 to -11 pts] | mid [-10 to 11 pts] | high [12 to 75 pts] |
| --- | --- | --- | --- |
| high [116 to 180 pts] | 5.82 / 4.34 | 6.14 / 4.34 | 6.22 / 4.32 |
| mid [96 to 115 pts] | 5.47 / 4.32 | 5.68 / 4.36 | 6.64 / 4.32 |
| low [34 to 95 pts] | 5.59 / 4.35 | 5.58 / 4.32 | 6.82 / 4.34 |

**Skewness** (real / sim)

All matches (real / sim / theory): 0.42 / 0.13 / 0.12

| Sum \ difference | low [-75 to -11 pts] | mid [-10 to 11 pts] | high [12 to 75 pts] |
| --- | --- | --- | --- |
| high [116 to 180 pts] | 0.65 / 0.12 | 0.48 / 0.16 | 0.21 / 0.12 |
| mid [96 to 115 pts] | 0.06 / 0.08 | -0.03 / 0.14 | 0.35 / 0.14 |
| low [34 to 95 pts] | 0.29 / 0.14 | 0.57 / 0.12 | 0.87 / 0.09 |

The simulated mean, standard deviation and skewness match the theory, which confirms the equations. The real mean is higher than the model's in every panel (by 0.2–2.1 shots), because the tempo urn was set from 2025/26 alone and the earlier seasons had more shots (27.6 per match in 2023/24, 25.9 in 2024/25, 25.0 in 2025/26). The standard deviation is too small in every panel (real 5.5–6.8, simulated 4.3–4.4), and the real one is too large for the tempo urn within each single season too (5.4–6.3). The real skewness is higher than the model's in most panels and over all matches (0.42 against 0.12).

Verdict: the mean is close, but the spread of total shots between matches is too small, and the tempo urn alone cannot fix it.

## Attack/defend (phase 4)

Observables: home share of shots per match.

### Model

[README step 4](../README.md#how-to-play): both teams grab $k_w$ balls from their match urns; the one with the
most red balls gets the shot. If they have equal red balls, they draw one more ball each until one gets red and the
other white. Parameters: $k_w$, and through the match urns $m_s$, $M_s$, $M_u$, $m_h$.

### Equations

Given the match urns, each shot is the home team's with the same probability $q$: the probability of grabbing more red balls, plus the probability of a tie times the probability of winning the tie-break. $q$ is computed exactly from the two match urns, including putting all balls back when an urn runs empty. The number of shots $T$ comes from the tempo urn (phase 3), independently of $q$, so the home shots are binomial($T$, $q$) and the home share is $S$ = home shots / $T$:

- Mean: $E[S \mid q] = q$
- Variance: $\text{Var}(S \mid q) = q(1-q)\,E[1/T]$
- Third central moment: $\mu_3(S \mid q) = q(1-q)(1-2q)\,E[1/T^2]$

Over the matches, $q$ varies with the match urns (phase 2) and with the teams that meet:

- Mean: $E[q]$
- Standard deviation: $\sigma = \sqrt{E[1/T]\,E[q(1-q)] + \text{Var}(q)}$. The first term is the noise from the limited number of shots, the second how much $q$ varies between matches.
- Skewness: $\left(E[1/T^2]\,E[q(1-q)(1-2q)] + 3\,E[1/T]\,\text{Cov}(q, q(1-q)) + \mu_3(q)\right) / \sigma^3$
- Distribution: not a standard one. Given $q$ it is a binomial divided by $T$, and over the matches a mixture of these, so its shape is judged from the figure.

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

Simulated with $k_w = 3$, $M_u = 20$, $m_h = 1$ and $M_s = 100$. These are starting values, not fitted ones. Compared against the three real seasons. Figure: `output/attack_defend_grid.html`.

**Mean** (real / sim)

All matches (real / sim / theory): 0.55 / 0.57 / 0.57

| Sum \ difference | low [-75 to -11 pts] | mid [-10 to 11 pts] | high [12 to 75 pts] |
| --- | --- | --- | --- |
| high [116 to 180 pts] | 0.44 / 0.46 | 0.56 / 0.57 | 0.67 / 0.67 |
| mid [96 to 115 pts] | 0.48 / 0.46 | 0.55 / 0.58 | 0.60 / 0.68 |
| low [34 to 95 pts] | 0.45 / 0.46 | 0.53 / 0.59 | 0.65 / 0.71 |

**Standard deviation** (real / sim)

All matches (real / sim / theory): 0.17 / 0.23 / 0.23

| Sum \ difference | low [-75 to -11 pts] | mid [-10 to 11 pts] | high [12 to 75 pts] |
| --- | --- | --- | --- |
| high [116 to 180 pts] | 0.17 / 0.21 | 0.12 / 0.22 | 0.14 / 0.20 |
| mid [96 to 115 pts] | 0.17 / 0.22 | 0.13 / 0.22 | 0.16 / 0.20 |
| low [34 to 95 pts] | 0.17 / 0.23 | 0.13 / 0.23 | 0.13 / 0.20 |

**Skewness** (real / sim)

All matches (real / sim / theory): -0.23 / -0.16 / -0.16

| Sum \ difference | low [-75 to -11 pts] | mid [-10 to 11 pts] | high [12 to 75 pts] |
| --- | --- | --- | --- |
| high [116 to 180 pts] | 0.31 / 0.20 | -0.01 / -0.19 | -0.31 / -0.47 |
| mid [96 to 115 pts] | -0.27 / 0.21 | -0.10 / -0.17 | -0.23 / -0.49 |
| low [34 to 95 pts] | 0.12 / 0.27 | -0.52 / -0.16 | -0.52 / -0.57 |

The simulated mean, standard deviation and skewness match the theory. The mean follows the real data in most panels, but rises too steeply with the difference in the mid- and low-sum rows (0.68–0.71 against 0.60–0.65 at high difference). The standard deviation is too large in every panel (simulated 0.20–0.23, real 0.12–0.17). By the variance equation, the limited number of shots gives about 0.09 of spread in both, so the excess is in how much $q$ varies between matches: about 0.21 in the model against about 0.14 in the real data. The skewness is negative at high difference in both, but more so in the model.

Verdict: the mean is close with the starting red balls, but the home share varies far too much from match to match, because the probability of winning a shot varies too much between matches.

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
