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

This chapter presents the skill update as a forward-only Bayesian calculation. For every candidate pair of skill pools, the model gives the probability of the observed match, shot by shot: which team shot and with what xG. Multiplied by the prior and normalised, this yields the posterior. Because the shots are independent given the match urns, the likelihood is a sum over match urns of products over shots, computed exactly from a lookup table indexed by the two match urns. The chapter also covers matching observed xG to the values the urns can produce, by splitting each shot between its two neighbouring values, the skill drift between matches as a spread around the current count, and the starting prior.

## 6. Fitting method

This chapter sets out how the model's parameters are fitted to real data: the error function, measured on what the model predicts for real matches once the inference has estimated each team's skill, and how it is minimised. Skill is not observed, so the fit has to run through the inference of chapter 5.

## 7. Fitting to real data

This chapter applies the method of chapter 6 to real matches. It opens with a rough fit that matches the mean, variance and skewness of each step to three Premier League seasons, with final points as the skill proxy, as the starting point. The flat relationship between shot count and skill, which motivates the tempo urn, is shown here. The fit against the error function follows, with its results and the places where the structure of chapter 4 cannot match the data, such as the variance of the shot count. It ends with a check of the inference on simulated matches, run with the fitted parameters, where twenty teams' red balls drift along slow curves: the inference should recover the known counts, with honest intervals. The check sets the assumed drift, and says nothing about whether the mechanics match real football.

## 8. Use

This chapter shows what the skill posteriors are for. Match outcome probabilities, including result probabilities derived from a match's xG rather than its scoreline; season simulations for final-table probabilities; and betting as one application, with a note on what calibration the model would need before money depends on it.

## 9. Known limitations

This chapter lists where the model stops, for anyone who wants to build on it. Game-state effects on play; tempo that depends on the teams; per-team finishing quality and xG-provider error; tactical mismatch as a pairwise effect; the circularity and cross-season comparability of the points proxy; the ceiling on variance from single-ball draws; the gaps the fit of chapter 7 finds.
