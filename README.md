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
uv run simulate       # simulate one season with the starting parameters and print the league table
uv run calibrate      # fit the parameters to the real season and compare all statistics (~1 minute)
uv run streamlit run src/football_urn_model/app.py   # play one match by hand in the browser
```

The scripts fetch the Premier League 2025/26 season from Understat (cached in `~/soccerdata` after the first run), print a
summary table. The analyses also write a CSV and an interactive plotly HTML page to `output/`. The model's
starting parameters are in `model_settings()` in `src/football_urn_model/simulate.py`; what is fitted, and
against which statistic, is in `fitting_plan()` in `src/football_urn_model/calibrate.py`. Skill difference is measured as
d = final points of one team − final points of the other.

The app plays one match by hand: each press of "Next draw" makes one draw (a number of balls from one urn), the
same steps as playing with real urns. Every model parameter and both teams' red balls are adjustable in the sidebar.
