# Appendix B. Starting point and checks on simulated data

This appendix holds the work that supports the fit without being part of it: the rough fit that gives the starting
point, and two checks on simulated data. Simulated matches come from the model itself, so they cannot fit it to real
football. They can show what the method recovers when the model is right by construction.

Not written yet. The plan for each section is below, and the to-dos are in `docs/book/README.md`.

## B.1 The rough fit

The starting point of the search of section 7.8. Each step of chapter 4 is matched to three Premier League seasons by
its mean, variance and skewness, one parameter at a time, with each team's final points as the skill proxy. This is
what `uv run calibrate` does now (`src/football_urn_model/calibrate.py`). Its values also generate the simulated data
of B.2.

The values the model uses now are in `model_settings()` in `src/football_urn_model/simulate.py`. They were not
fitted by the method of chapter 7; B.1 is to rerun the rough fit and replace them, with the table of values produced
by a command rather than typed in.

## B.2 Which parameters the fit can recover

A test of how much the data can tell about each parameter. Matches are simulated with the values of B.1 as the true
parameters, as many matches as the real data has, with each team's skill drifting slowly. The fit of chapter 7 is
then run on the simulated shots from several random starting points.

Measured: for each parameter, how close the fits come to its true value, and how widely they spread; and whether the
searches from different starts end in the same place, or stop in valleys and local minima. A parameter the fit
cannot recover is fixed by design in section 7.7.

Trainability can depend on where in parameter space the true values lie, so B.2 is rerun with the fitted values of
chapter 8, to check that its conclusions still hold.

## B.3 The check of the inference

A test of the inference of chapter 5, run with the parameters and $\sigma$ fitted in chapter 8. About twenty teams
play thousands of matches by chapter 4's rules, each team's skill pool changing slowly along its own curve, for
example a sine wave with its own period, amplitude and phase. The inference is run on the simulated shots alone.

Measured: how far the centre of each team's distribution lags behind its true red balls; whether an 80% interval
holds the truth in about 80% of matches; and how many matches a team needs before its distribution stops narrowing.
It verifies the fitted $\sigma$ and tests the assumption of independent skills of section 5.6. It cannot show whether
the model describes real football. The earlier text of this check is in commit `3c787bf`.
