# The urn model of football

*Theory, mechanics and inference*

This document is a complete account of one football model: what it assumes about the game, how it simplifies those assumptions into a lottery of red and white balls, how team skill is inferred from observed matches, and how the result is used. It is meant to be read once and to stand on its own. Each chapter below has a short note on what it covers.

This file is the outline only. The reasoning behind each chapter is in [discussion-notes-2026-11-12.md](discussion-notes-2026-11-12.md).

## 1. Introduction

This chapter states what the model is for and how to read the document. The purpose is to estimate each team's underlying skill, with uncertainty, from match data, and to turn those estimates into probabilities for future matches and season outcomes. The chapter also sets expectations: the model is deliberately simple, every simplification is stated, and the final chapter lists where it stops.

## 2. A theory of football

This chapter describes how football is assumed to work before any modelling. Randomness enters in three layers: slow drift in true skill between games (injuries, form), a match-day draw of form around that skill, and chance within the game itself. The chapter explains why a good team can look bad on a given day without being bad, and notes that tactical mismatch between two specific teams is real but will be treated as noise.

## 3. From theory to model

This chapter records the simplifications and the reasons for them. Key choices: xG rather than goals is the observable, because finishing is treated as random; measured xG is taken as true xG in this version; teams do not change behaviour with the score; tempo is independent of skill. Each choice is stated as an assumption so a reader can judge its cost.

## 4. Model mechanics

This chapter specifies the urn chain exactly. A team's skill pool is drawn into a match urn, with marked home-advantage balls added for the home side. Each round a neutral urn decides whether a shot occurs; the match urns decide who gets it; an attack-versus-defence draw sets whether it is a big or normal chance and how many attacker balls survive; the resulting shot urn's red-to-white ratio is the shot's xG; a final draw decides the goal. The chapter closes with the resolution-versus-variance tension: ball counts set xG resolution, the number drawn sets variance, and the two must be tuned separately.

## 5. Fitting the structure

This chapter shows how real data shaped the mechanics, one section per phase. For each observable (shots per game, home/away shot share, xG per shot) it reports mean, variance and skew across a grid of skill levels, using three Premier League seasons with final points as the skill proxy. The flat relationship between shot count and skill is what motivates the neutral urn. The chapter is explicit that this exercise fixed structure only, not final parameter values.

## 6. Inference

This chapter presents the skill update as a forward-only Bayesian calculation. For every candidate pair of red-ball counts, the model gives the probability of the observed match (shot share and each team's xG, by total or shot by shot); multiplied by the prior and normalised, this yields the posterior. Because rounds are identical and independent, every cell can be computed exactly and stored in a lookup table. One worked cell (six versus six) is shown to make the method concrete; full tables are left to chapter 7.

## 7. Validation

This chapter tests the inference on synthetic data where the truth is known. Twenty artificial teams play thousands of matches while their red-ball counts drift along slow curves of differing period, amplitude and phase; the inference is run on the results and judged by how well it recovers the known counts. A full example table appears here. The chapter is clear about what this does and does not establish: it tunes the inference under a correct forward model, and says nothing about whether the mechanics match real football.

## 8. Use

This chapter shows what the skill posteriors are for. Match outcome probabilities, including result probabilities derived from a match's xG rather than its scoreline; season simulations for final-table probabilities; and betting as one application, with a note on what calibration the model would need before money depends on it.

## 9. Known limitations

This chapter lists where the model stops, for anyone who wants to build on it. Game-state effects on play; tempo that depends on the teams; per-team finishing quality and xG-provider error; tactical mismatch as a pairwise effect; the circularity and cross-season comparability of the points proxy; the ceiling on variance from single-ball draws.
