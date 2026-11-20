# The urn model of football

*Theory, mechanics and inference*

This document is a complete account of one football model: what it assumes about the game, how it simplifies those assumptions into a lottery of red and white balls, how team skill is inferred from observed matches, and how the result is used. It is meant to be read once and to stand on its own. Each chapter below has a short note on what it covers.

This file is the outline only. The reasoning behind each chapter is in [discussion-notes-2026-11-12.md](discussion-notes-2026-11-12.md).

## 1. Introduction

This chapter states what the model is for and how to read the document. The purpose is to estimate each team's underlying skill, with uncertainty, from match data, and to turn those estimates into probabilities for future matches and season outcomes. The chapter also sets expectations: the model is deliberately simple, every simplification is stated, and the final chapter lists where it stops.

## 2. A theory of football

This chapter describes how football is assumed to work before any modelling. Randomness enters in three layers: slow drift in true skill between games (injuries, form), a match-day draw of form around that skill, and chance within the game itself. The chapter explains why a good team can look bad on a given day without being bad, and notes that tactical mismatch between two specific teams is real but will be treated as noise.

## 3. From theory to model

This chapter records the simplifications and the reasons for them. Key choices: xG rather than goals is the observable, because finishing is treated as random; measured xG is taken as true xG in this version; teams do not change behaviour with the score, so every round of a match is identical and independent given the two match urns; tempo is independent of skill. It also maps the urn chain onto chapter 2's three layers of randomness. Each choice is stated as an assumption so a reader can judge its cost.

## 4. Model mechanics

This chapter specifies the urn chain exactly. A team's skill pool is drawn into a match urn, with marked home-advantage balls added for the home side. Each round the tempo urn decides whether a shot occurs; the match urns decide who gets it; an attack-versus-defence draw sets whether it is a big or normal chance and how many attacker balls survive; the resulting shot urn's red-to-white ratio is the shot's xG; a final draw decides the goal. For each step the chapter gives the mean, variance and skewness given the outcome of the step before. It does not combine the steps, and it has no worked example.

## 5. Inference

This chapter presents the skill update as a forward-only Bayesian calculation. For every candidate pair of skill pools, the model gives the probability of the observed match, shot by shot: which team shot and with what xG. Multiplied by the prior and normalised, this yields the posterior. Because the shots are independent given the match urns, the likelihood is a sum over match urns of products over shots, computed exactly from chapter 4's equations, without simulation; appendix A shows how. The chapter also covers matching observed xG to the values the urns can produce, by splitting each shot between its two neighbouring values, the skill drift between matches as a spread around the current count, and the starting prior. Each assumption is stated once, in a marked paragraph.

## 6. Fitting method

This chapter sets out how the model's parameters are fitted to real data: the error function, measured on what the model predicts for real matches once the inference has estimated each team's skill, and how it is minimised. Skill is not observed, so the fit has to run through the inference of chapter 5. Each match is predicted from the skills just before it; each team's shot count and each shot's xG are scored by the ranked probability score on fixed bins, with a weight between the two tuned on results. The chapter says which parameters are trained, as shares where that separates their effects, and which are fixed by design, such as the rounds and the skill pool size; the drift spread is trained with the rest. The error is minimised by a search over one-ball steps from the rough fit, with restarts. Results are kept for tuning and for a held-out test against bookmaker odds and league averages.

## 7. Fitting to real data

This chapter runs the method of chapter 6 on real matches and reports the numbers. It states the values fixed by design, starts the search from the rough fit of appendix B.1, and gives the fitted parameters, the drift spread and the weight. The flat relationship between shot count and skill, which motivates the tempo urn, is shown here. It covers resolution against variance, the places where the structure of chapter 4 cannot match the data, such as the variance of the shot count, and the held-out test on results.

## 8. Use

This chapter shows what the skill posteriors are for. Match outcome probabilities, including result probabilities derived from a match's xG rather than its scoreline; season simulations for final-table probabilities; and betting as one application, with a note on what calibration the model would need before money depends on it.

## 9. Known limitations

This chapter lists where the model stops, for anyone who wants to build on it. Game-state effects on play; tempo that depends on the teams; per-team finishing quality and xG-provider error; tactical mismatch as a pairwise effect; the circularity and cross-season comparability of the points proxy; the ceiling on variance from single-ball draws; the fixed tempo urn, which cannot give a shot-count variance above its mean, with a tempo pool as the fix; the gaps the fit of chapter 7 finds.

## Appendix A. Computation

How the likelihood of chapter 5 is computed exactly and cheaply: the lookup table indexed by the two match urns, the matrix form of the sum over match urns, log-scaling, and the cost of larger urns and skill pools.

## Appendix B. Starting point and checks on simulated data

B.1, the rough fit: the mean, variance and skewness of each step matched to three Premier League seasons, with final points as the skill proxy; the starting point of the search. B.2, which parameters the fit can recover: data simulated from B.1's values and fitted from random starts. B.3, the check of the inference: twenty teams' red balls drift along slow curves, and the inference, with the fitted parameters, should follow them with honest intervals. It verifies the drift spread and says nothing about whether the mechanics match real football.
