# 7. Fitting to real data

Not written yet. This chapter runs the method of chapter 6 on real matches and reports the numbers. The plan is in
`docs/report-outline.md` and the to-dos in `docs/book/README.md`.

Planned sections:

- **The data.** The seasons used, their split into training, tuning and test sets (section 6.9), and the matches
  left out at the start (section 6.6).
- **The values fixed by design.** The rounds $n$ (100), the skill pool $M_s$, the tempo urn $M_t$, the xG bins
  (section 6.3), and any parameter appendix B.2 finds the data cannot pin down.
- **The fit.** The search of section 6.8 from the rough fit of appendix B.1: the fitted parameters, $\sigma$ and
  $\lambda$, and whether the restarts agree.
- **Resolution against variance.** The design trade-off between the number of balls and the spread they give.
- **Where the structure cannot match the data.** For example the shot-count variance, which feeds chapter 9.
- **The test on results.** The held-out matches against bookmaker odds and league averages (section 6.9).

The parameter values the model uses now are in appendix B.1.
