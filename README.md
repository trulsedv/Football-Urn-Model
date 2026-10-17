# Football Urn Model

A probabilistic "urn" model of football matches. Each team's skill is a number of red balls in a pool; drawing red balls will create shots with xG and goals. This project designs and calibrates the model so that simulated seasons look like real Premier League seasons. Using it to infer how much better one team is than another is for later.

Work in progress: a data analysis of Premier League shots and xG guided the model design, and a first simulator
plays seasons with untrained starting parameters.
See `docs/`: `design.md` (the model), `considerations.md` (why, open questions, future ideas) and
`data-analysis.md` (the data behind it).

## Running

```bash
uv sync
uv run shot-counts    # analysis 1: shots per match vs skill difference
uv run shot-quality   # analysis 2: xG per shot vs skill difference
uv run simulate       # simulate seasons with the urn model and compare with the real season
```

All three fetch the Premier League 2025/26 season from Understat (cached in `~/soccerdata` after the first run), print a
summary table. The analyses also write a CSV and an interactive plotly HTML page to `output/`. The model's
parameters are set in `model_settings()` in `src/football_urn_model/simulate.py`. Skill difference is measured as
d = final points of one team − final points of the other.
