# 7. Fitting to real data

Not written yet. The plan is in `docs/report-outline.md` and the to-dos in `docs/book/README.md`.

## Starting values

These are the parameter values the model uses now. They were not fitted; the fit of this chapter replaces them. They
were moved here from section 4.1, so that chapters 4 to 6 hold no values. The code holds the same values in
`model_settings()` in `src/football_urn_model/simulate.py`.

| Symbol | Meaning | Starting value |
| --- | --- | --- |
| $M_s$, $m_s$ | Balls and red balls in a skill pool | 100; $m_s$ from 10 to 25 by team |
| $M_u$ | Balls drawn from the skill pool into a match urn | 20 |
| $M_t$, $m_t$ | Balls and red balls in the tempo urn | 4 and 1 |
| $n$ | Rounds per match | 100 |
| $K_s$ | Balls each team draws to decide who shoots | 3 |
| $b$ | Big-chance margin | 2 |
| $K_a$ | Balls drawn by the attacking team | 5 |
| $K_d$ | Balls drawn by the defending team | 1 |
| $x_H$ | Red h-marked balls in the home team's match urn | 1 |
| $X_o$, $x_o$ | x-marked balls and red x-marked balls for an ordinary chance | 21 and 1 |
| $X_b$, $x_b$ | x-marked balls and red x-marked balls for a big chance | 20 and 8 |
