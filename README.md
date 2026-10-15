# Football Urn Model

A probabilistic "urn" model of football matches. Each team's skill is a number of red balls in a pool; drawing red balls will create shots with xG and goals. Because every step is an explicit probability, the same model can simulate matches and compute exact likelihoods of how much better one team is than another.

Work in progress: the first step is a data analysis of Premier League shots and xG to guide the model design.
See `Football Urn Model — Design Document.md` for the current (draft) design.

## Running

```bash
uv sync
uv run football-urn-model
```

This fetches the Premier League 2025/26 season from Understat (cached in `~/soccerdata` after the first run), prints
shot-count statistics per bin of d = home final points − away final points, and writes
`output/shot_counts_by_d.csv` and `output/shot_counts_by_d.html` (interactive plotly heatmaps of P(k shots | d)).
