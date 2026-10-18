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

Each chapter below has three parts: what the data shows (with the skill proxy), the model and its equations, and how the model fits the data. Phase 1 (skill change) is an input to the simulation and has no chapter.

## Phase 2: Match urn

### Analysis of data

The match urn has no observable of its own. It shows up as extra spread between matches in the later phases, for
example in the share of shots per team (phase 4).

### Modelling and constraining equations

Each team draws $M_u$ balls from its skill pool of $M_s$ balls, $m_s$ of them red; the home team adds $m_h$ red balls.

- The distribution of red balls in the match urn will be:
  [eq]

## Phase 3: Total number of shots (both teams)

### Analysis of data

- The mean does not depend on:
  - skill proxy difference, see analysis 1
  - skill proxy sum, see analysis 1
- The variance does depend on:
  - (not confirmed) skill proxy difference, see analysis result X
  - (not confirmed) skill proxy sum, see analysis result X

#### Shape of the data

The distribution looks like X.

### Modelling and constraining equations

The number of shots is modelled by drawing from a tempo urn with $M_t$ balls and $m_t$ red balls, once in each of the n
rounds. With $p = m_t / M_t$:

- The mean of the total number of shots will be:
  $\mu = n p$
- The variance of the total number of shots will be:
  $n p (1 - p) = \mu - \mu^2 / n$
- The total number of shots is binomially distributed. Its variance is always below its mean, and grows towards
  the mean as n grows.

#### Model vs data

[how does this fit the data]

## Phase 4: Share of shots per team

### Analysis of data

- The mean does depend on:
  - skill proxy difference, see analysis 1
  - (not confirmed) skill proxy sum, see analysis X
- The variance does depend on:
  - (not confirmed) skill proxy difference, see analysis result X
  - (not confirmed) skill proxy sum, see analysis result X

#### Shape of the data

The mean goes from X to Y rather linearly with changing skill proxy difference.
For a given set of skills the distribution looks like X.

### Modelling and constraining equations

The share of shots per team is modelled by the two teams drawing $k_w$ balls from their match urns; the one with the
most red balls gets the shot. If they have equal red balls, they draw one more ball each until one gets red and the
other white.

- The mean for a team will be:
  [eq]
- The variance for a team will be:
  [eq]

$k_w$ and the difference in red balls between teams both set how uneven the split of shots is. A larger $k_w$ gives
the better team a bigger share, and more so when $M_u$ is small, since grabbing $k_w$ of a small match urn reveals
more of it. Example share of shots for A, $M_u$ = 20:

| A red share | B red share | $k_w$ = 1 | $k_w$ = 3 | $k_w$ = 5 | $k_w$ = 10 |
| --- | --- | --- | --- | --- | --- |
| 0.55 | 0.45 | 0.60 | 0.64 | 0.67 | 0.77 |
| 0.60 | 0.40 | 0.70 | 0.76 | 0.81 | 0.93 |
| 0.30 | 0.20 | 0.64 | 0.67 | 0.71 | 0.82 |
| 0.15 | 0.10 | 0.62 | 0.64 | 0.66 | 0.76 |

#### Model vs data

[how does this fit the data]

## Phase 5: xG value of shots

### Analysis of data

- The mean does depend on:
  - skill proxy difference, see analysis 2
  - (not confirmed) skill proxy sum, see analysis result X
- The variance does depend on:
  - (not confirmed) skill proxy difference, see analysis result X
  - (not confirmed) skill proxy sum, see analysis result X

#### Shape of the data

The distribution looks like X.

### Modelling and constraining equations

The xG is modelled in two ways: ordinary chance and big chance. If the team won the shot (phase 4) by $b$ (the big-chance margin)
or more red balls, it is a big chance. A shot urn is filled with balls:

- x-marked balls: $M_x$ of them, $m_x$ red. $M_x$, $m_x$ = $M_{xb}$, $m_{xb}$ for a big chance and $M_{xo}$, $m_{xo}$ for an ordinary chance.
- The attacking team draws $k_c$ balls from its match urn and gets $R_1$ red balls.
- The defending team draws $k_d$ balls from its match urn and gets $R_2$ red balls.
- The defender's red balls cancel the attacker's red balls: $c = \min(R_1, R_2)$ red balls are removed.
- The remaining $k_c - c$ drawn balls are placed in the shot urn together with the marked balls.

$$\text{xG} = \frac{m_x + R_1 - c}{M_x + k_c - c}$$

#### Big chance constraining equations

- The mean of the xG will be:
  [eq]
- The variance of the xG will be:
  [eq]

#### Ordinary chance constraining equations

- The mean of the xG will be:
  [eq]
- The variance of the xG will be:
  [eq]

#### Model vs data

[how does this fit the data]

## Phase 6: Goals

### Analysis of data

- The mean does depend on:
  - (not confirmed) skill proxy difference, see analysis result X
  - (not confirmed) skill proxy sum, see analysis result X
- The variance does depend on:
  - (not confirmed) skill proxy difference, see analysis result X
  - (not confirmed) skill proxy sum, see analysis result X

#### Shape of the data

The distribution looks like X.

### Modelling and constraining equations

One ball is drawn from the shot urn; red (or marked red) is a goal. A shot's xG is therefore exactly the probability
that it becomes a goal.

- The mean number of goals will be:
  [eq]
- The variance of the number of goals will be:
  [eq]

#### Model vs data

[how does this fit the data]

## Outcomes

The outcomes follow from the phases above. Each is written as an equation given the outcome of the phases, and
compared with simulated seasons.

### Results

#### Analysis of data

- The home win, draw and away win rates depend on:
  - (not confirmed) skill proxy difference, see analysis result X
  - (not confirmed) skill proxy sum, see analysis result X

#### Modelling and equations

[eq]

#### Model vs data

[how does this fit the data]

### Final points of the season

#### Analysis of data

The final points are the skill proxy for the data analyses. Their spread over the teams is: X.

#### Modelling and equations

[eq]

#### Model vs data

[how does this fit the data]

## Parameters

The current values are in `model_settings()` in `src/football_urn_model/simulate.py`.

| Parameter | Symbol | Chapters, and what it changes |
| --- | --- | --- |
| Red balls in a team's skill pool | $m_s$ | Phase 2: red balls in the match urn; through it, phases 4, 5 and the outcomes |
| Balls in the skill pool | $M_s$ | Phase 2: spread of red balls in the match urn (form) |
| Balls in the match urn | $M_u$ | Phase 2: form; phase 4: share of shots; phase 5: xG |
| Extra red balls for the home team | $m_h$ | Phase 2: home match urn; phase 4: home share of shots; phase 5: home xG |
| Rounds per match | n | Phase 3: mean and variance of total shots |
| Balls and red balls in the tempo urn | $M_t$, $m_t$ | Phase 3: mean and variance of total shots |
| Balls grabbed to decide who shoots | $k_w$ | Phase 4: share of shots; phase 5: share of big chances |
| Big-chance margin | $b$ | Phase 5: share of big chances |
| Chance balls drawn by the shooting team | $k_c$ | Phase 5: xG |
| Balls drawn by the defending team | $k_d$ | Phase 5: xG |
| x-marked balls and red x-marked balls, ordinary shot | $M_{xo}$, $m_{xo}$ | Phase 5: xG of ordinary shots; phase 6: goals |
| x-marked balls and red x-marked balls, big chance | $M_{xb}$, $m_{xb}$ | Phase 5: xG of big chances; phase 6: goals |
