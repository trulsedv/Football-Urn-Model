# Football Urn Model — Design

Oct 15, 2026 · @Truls Edvardsen Aarønes

This document describes the model as it is. Why it looks this way, open questions and future ideas are in
[considerations.md](considerations.md); the data behind it is in [data-analysis.md](data-analysis.md).

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

## Model structure

A simulation is a series of matches. Each match runs through six phases:

For each match:

1. **Skill change** (skill pool: M balls, R red): the number of red balls in each team's skill pool may change, as
   set by whoever runs the simulation.
2. **Match urn** (m balls): each team fills its match urn with m balls drawn from its skill pool (+ h extra red
   balls for the home team).
   - The home team gets x red balls extra to add to its match urn.

Then, for each of the n rounds in the match:

3. **Shot or not** (tempo urn: N balls, s red): one draw decides whether there is a shot this round.

   If there is a shot:

4. **Who shoots:** both teams draw from their match urns, which decides who shoots.
5. **xG** (c chance balls): the shooting team draws c balls from its match urn; their red share is the shot's xG. The balls are then placed in a shot urn.
6. **Goal or not:** one ball is drawn from the c chance balls; red is a goal.

Observed: for each shot, the round, the shooting team (home or away), its xG and whether it was a goal.

## Equations for probabilites in each phase

When the model is complete this chapter can be written.

## Training and validation

Training means choosing the parameters so that simulated seasons look like real ones. When the model is complete this chapter can be written.

Simulate whole seasons with the trained parameters and compare against real data:

- Distribution of shots and xG per team per match
- Goals per match, 0–0 rate, draw rate, common scorelines
- Spread of final league points
- Etc.

## Relation to real world xG data

In this model, a shot's xG is exactly the probability that it becomes a goal. Real-world xG data does not account for all of a team's skill. Therefore some teams can outperform xG data from, for example, Understat, and the xG data may in general overestimate or underestimate the number of goals scored.

If this model is used to estimate teams' skill from xG data from, for example, Understat, the inaccuracy above could be accounted for before inference is done (inference: it is p likely that team A has x red balls in its skill pool, given the xG data and the previous likelihoods of all possible numbers of red balls in its skill pool).
