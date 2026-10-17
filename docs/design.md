# Football Urn Model — Design

Oct 15, 2026 · @Truls Edvardsen Aarønes

This document describes the model as it is. Why it looks this way, open questions and future ideas are in
[considerations.md](considerations.md); the data behind it is in [data-analysis.md](data-analysis.md).

## Purpose and goals

The model treats a football match as a lottery: each team's skill is a count of red balls, red draws decide who
gets the shots, and drawn balls decide each shot's xG and whether it becomes a goal. Because every step is
an explicit probability, the model can simulate matches and stays usable for exact inference later.

The model must:

1. Simulate realistic match results and xG data (number of shots, xG values, result).
2. Stay usable for inference later (not part of this project): from observed xG data it should be possible to
   compute, with a clear probabilistic meaning, how likely it is that team A has N more red balls than team B.
3. Keep underlying skill slow-moving, with match-to-match form as a separate, faster source of randomness.
4. Stay simple enough that every probability can be written down and computed exactly on a grid.
5. Be physically playable: every random step is a draw of balls from an urn, so a match could be played with real
   urns and balls. No step may use a fitted function or continuous distribution.

## Model structure

A match is played in six phases, simulated from phase 1 to phase 6.

1. **Skill change** (skill pool: M balls, R red): the number of red balls, set by whoever runs the simulation.
2. **Match urn** (m balls): filled from the skill pool before each match.
3. **Shot or not** (tempo urn: N balls, s red): one draw decides if there is a shot this round. Phases 3–6 are
   repeated for each of the n rounds in a match; phases 4–6 only when there is a shot.
4. **Who shoots**: both teams draw from their match urns.
5. **xG** (o balls): the shooting team draws o balls from its match urn; the red share is the shot's xG.
6. **Goal or not**: one ball is drawn from the o balls; red is a goal.

Observed: number of shots, xG values, result.

Real data is compared with simulated data after a correction step: data source → correction → comparison.

## Mathematical specification

Each phase is a standard distribution, so every probability can be written down (goal 4).

**Phase 1 — Skill change.** Team i has a skill pool of M balls, of which R\_i are red; skill is θ\_i = R\_i / M.
R\_i is an input to the simulation, not a random draw of the model: whoever runs the simulation decides whether
and how it changes between matches (not at all, randomly, or by a rule), typically by small steps. The true R\_i is
hidden from anyone who only sees the simulated shots, xG values and goals.

**Phase 2 — Match urn.** Before each match, team i fills its match urn with m balls drawn from its skill pool
without replacement. The number of red match balls is hypergeometric:

```latex
k_i \sim \mathrm{Hypergeometric}(M,\ R_i,\ m), \qquad p_i = k_i / m
```

p\_i is the team's strength on the day. Smaller m means more matchday variation. The home team gets h extra red
match balls.

**Phase 3 — Shot or not.** The match has n rounds. In each round, one ball is drawn (with replacement) from a tempo
urn of N balls, s of them red. A red ball means there is a shot this round. The tempo urn is independent of the
match urns. With μ the average number of shots per match, the tempo urn has s = μN/n red balls (N and n chosen so
that s is a whole number; n ≥ μ).

**Phase 4 — Who shoots.** Both teams draw one ball (with replacement) from their match urns. A red, B white → A
shoots; B red, A white → B shoots. Same colour: redraw or flip a coin (not decided yet).

Over a match, the total number of shots T and A's shots S\_A are therefore:

```latex
T \sim \mathrm{Binomial}(n,\ s/N), \qquad S_A \mid T \sim \mathrm{Binomial}(T,\ q_A), \qquad S_B = T - S_A
```

where q\_A is the probability that A shoots: q\_A = p\_A(1−p\_B) / [p\_A(1−p\_B) + p\_B(1−p\_A)] with redraw, or
q\_A = ½ + ½(p\_A − p\_B) with a coin flip.

**Phase 5 — xG.** The shooting team draws o balls (e.g. o = 10) from its match urn without replacement. The share of
red balls among them is the shot's xG:

```latex
r_j \sim \mathrm{Hypergeometric}(m,\ k_i,\ o), \qquad x_j = r_j / o
```

xG can therefore only take the values 0, 1/o, …, 1. A better team gets better chances, and finishing is part of
skill.

**Phase 6 — Goal or not.** One ball is drawn from the o balls; red is a goal. Afterwards all o balls go back into
the match urn.

```latex
G_j \sim \mathrm{Bernoulli}(x_j)
```

## Correcting the xG data

The correction is not part of the model. It is a transformation step between a data source and the model:

data source → correction → comparison with simulated data (calibration, validation)

In the model, xG is the red share of the o balls drawn in phase 5. A data source's xG comes from its own model, so each
data source has its own correction that turns its xG into model xG. Since the correction is outside the model, it
does not have to be playable and may use fitted functions. Its form is not decided yet.

## Calibration

Calibration means choosing the parameters so that simulated seasons look like real ones. These parameters need
fixing:

| Parameter | What it controls | Matched against | Method |
| --- | --- | --- | --- |
| M (pool size) | Resolution of the skill scale | Not identifiable from data | Choose it (e.g. 100); it only sets the units of "one ball" |
| n (match rounds), N and s (tempo urn) | Total shot volume | Mean total shots per match, μ ≈ 25 | s = μN/n |
| o (xG balls) | Distribution of xG per shot | All shots in the league, after correction | Match simulated to real |
| R\_i (red balls per team) | Spread of skill across teams | Spread of shot shares and final points over a season | Match simulated to real |
| m (match balls) | Size of matchday form swings | Variation in a team's shot share between matches beyond binomial | Match simulated to real |
| h (home balls) | Extra red match balls for the home team | Home vs away difference in shots and xG | Match simulated to real |

**Procedure:**

1. Fix M, and set n, N and s from μ.
2. Correct the data source's xG, then choose o so that simulated xG per shot matches the real distribution.
3. Choose the teams' red balls, m and h so that simulated shot shares, their variation between matches, the home vs
   away difference and the spread of final points match the real season.
4. Validate (next section). Recalibrate if checks fail.

The key identification point: m is set by how much a team's shot share varies between matches *more than* binomial
noise alone would cause. Without matchday form, simulated shot shares would vary too little between matches.

## Validation

Simulate whole seasons with the calibrated parameters and compare against real data:

- Distribution of shots and xG per team per match
- Goals per match, 0–0 rate, draw rate, common scorelines
- Spread of final league points
