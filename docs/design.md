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

## Notation

- M = total number of balls in a container, m = number of red balls in it. The subscript names the container:
  s = skill pool, u = match urn, t = tempo urn.
- k = number of balls drawn: k\_w to decide who shoots, k\_c chance balls drawn by the shooting team, k\_d balls
  drawn by the defending team.
- n = rounds per match, m\_h = extra red balls for the home team, μ = average number of shots per match.
- Marked balls: extra balls added to the shot urn, separate numbers of marked red and marked white for ordinary
  shots and for big chances. A marked red ball counts as red.

## Model structure

A simulation is a series of matches. Each match runs through six phases:

For each match:

1. **Skill change** (skill pool: M\_s balls, m\_s red): the number of red balls in each team's skill pool may
   change, as set by whoever runs the simulation.
2. **Match urn** (M\_u balls): each team fills its match urn with M\_u balls drawn from its skill pool. The home
   team adds m\_h extra red balls to its match urn.

Then, for each of the n rounds in the match:

3. **Shot or not** (tempo urn: M\_t balls, m\_t red): one draw decides whether there is a shot this round.

   If there is a shot:

4. **Who shoots:** each team grabs k\_w balls from its match urn (without replacement). The team with more red
   balls shoots. If equal, each team draws one more ball at a time until one draws red and the other white. If the
   shooting team won by at least a set number of red balls (the big-chance margin), the shot is a big chance. A
   tie-break win is never a big chance. All balls then go back into the match urns.
5. **xG** (k\_c and k\_d balls, k\_d < k\_c): the shooting team draws k\_c balls and the defending team k\_d
   balls from their match urns (without replacement). The shooting team removes as many red balls as the defender
   drew (at most all its own red balls) and places the rest of its balls in a shot urn, together with the marked
   balls for its kind of shot (ordinary or big chance). The shot urn's red share, counting marked red as red, is the
   shot's xG.
6. **Goal or not:** one ball is drawn from the shot urn; red (or marked red) is a goal. The marked balls are taken
   out, and the rest go back into the match urns.

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

**Who shoots (phase 4):** k\_w and the difference in red balls between teams both set how uneven the split of
shots is. A larger k\_w gives the better team a bigger share, and more so when M\_u is small, since grabbing k\_w
of a small match urn reveals more of it. One of them has to be fixed before the other can be trained. Example
share of shots for A, M\_u = 20:

| A red share | B red share | k\_w = 1 | k\_w = 3 | k\_w = 5 | k\_w = 10 |
| --- | --- | --- | --- | --- | --- |
| 0.55 | 0.45 | 0.60 | 0.64 | 0.67 | 0.77 |
| 0.60 | 0.40 | 0.70 | 0.76 | 0.81 | 0.93 |
| 0.30 | 0.20 | 0.64 | 0.67 | 0.71 | 0.82 |
| 0.15 | 0.10 | 0.62 | 0.64 | 0.66 | 0.76 |

## Relation to real world xG data

In this model, a shot's xG is exactly the probability that it becomes a goal. Real-world xG data does not account for all of a team's skill. Therefore some teams can outperform xG data from, for example, Understat, and the xG data may in general overestimate or underestimate the number of goals scored.

If this model is used to estimate teams' skill from xG data from, for example, Understat, the inaccuracy above could be accounted for before inference is done (inference: it is p likely that team A has x red balls in its skill pool, given the xG data and the previous likelihoods of all possible numbers of red balls in its skill pool).
