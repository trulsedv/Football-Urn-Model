# Football Urn Model

A probabilistic "urn" model of football matches. Each team's skill is a number of red balls in a pool; drawing red balls will create shots with xG and goals. This project designs and calibrates the model so that simulated seasons look like real Premier League seasons. Using it to infer how much better one team is than another is for later.

Work in progress: a data analysis of Premier League shots and xG guided the model design, and a first simulator
plays seasons with untrained starting parameters.
See `docs/`: `design.md` (why the model is the way it is, with equations and parameters), `considerations.md`
(alternatives considered, open questions, future ideas) and `data-analysis.md` (the data and figures behind it).

## How to play

Each team has a skill pool of balls; its skill is the number of red balls in it. The symbols in brackets are the
ones used in `docs/design.md`. A season is a series of matches. For each match:

1. **Skill change** (skill pool: M\_s balls, m\_s red): whoever runs the simulation may change the number of red
   balls in each team's skill pool.
2. **Match urn** (M\_u balls): each team fills its match urn with M\_u balls drawn from its skill pool. The home
   team adds m\_h extra red balls to its match urn.

Then play n rounds. In each round:

3. **Shot or not** (tempo urn: M\_t balls, m\_t red): draw one ball from the tempo urn. Red is a shot; white ends
   the round.
4. **Who shoots:** each team grabs k\_w balls from its match urn. The team with more red balls shoots. If equal,
   each team draws one more ball at a time until one draws red and the other white. If the shooting team won by at
   least the big-chance margin, the shot is a big chance (a tie-break win never is). Put all balls back.
5. **Shot urn:** the shooting team draws k\_c balls and the defending team k\_d balls from their match urns. The
   shooting team removes as many red balls as the defender drew (at most all its own red balls) and puts the rest of
   its balls in a shot urn, together with the marked balls for its kind of shot (ordinary or big chance). A marked
   red ball counts as red. The shot urn's red share is the shot's xG.
6. **Goal or not:** draw one ball from the shot urn; red is a goal. Take the marked balls out and put the rest back
   into the match urns.

Record for each shot: the round, the shooting team, its xG and whether it was a goal.

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
