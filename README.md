# Football Urn Model

**This project is a work in progress.**

A probabilistic "urn" model of football matches. Each team's skill is a number of red balls in a pool; drawing red balls will create shots with xG and goals. This project designs and calibrates the model so that simulated seasons look like real Premier League seasons.

See `docs/`: `design.md` (why the model is the way it is, with equations and parameters), `considerations.md`
(alternatives considered, open questions, future ideas) and `data-analysis.md` (the data and figures behind it).

## How to play

Each team has a skill pool of balls; its skill is the number of red balls in it. The symbols in brackets are the
ones used in `docs/design.md`. A season is a series of matches. For each match:

1. **Skill change** (skill pool: $M_s$ balls, $m_s$ red): whoever runs the simulation may change the number of red
   balls in each team's skill pool.
2. **Match urn** ($M_u$ balls): each team fills its match urn with $M_u$ balls drawn from its skill pool. The home
   team adds $m_h$ extra red h-marked balls to its match urn.

Then play n rounds. In each round:

3. **Shot or not** (tempo urn: $M_t$ balls, $m_t$ red): draw one ball from the tempo urn. Red is a shot; white ends
   the round.
4. **Who shoots:** each team grabs $k_w$ balls from its match urn. The team with more red balls shoots. If equal,
   each team draws one more ball at a time until one draws red and the other white. If the shooting team had at
   least $b$ more red balls in its grab, the shot is a big chance; a team that wins in the tie-break never has a
   big chance. Put all balls back in the match urn.
5. **Shot urn:** the shooting team draws $k_c$ balls and the defending team $k_d$ balls from their match urns. The
   shooting team removes as many red balls as the defender drew (at most all its own red balls) and puts the rest of
   its balls in a shot urn. If a big chance, $M_{xb}$ x-marked balls are also placed in the shot urn, $m_{xb}$ of them red. If not a big chance, $M_{xo}$ x-marked balls are placed in the shot urn, $m_{xo}$ of them red. The shot urn's red share is the shot's xG. The defender puts its ball back in its match urn.
6. **Goal or not:** draw one ball from the shot urn; red is a goal. Take the marked balls out and put the rest back
   into the match urns.

Record for each shot: the round, the shooting team, its xG and whether it was a goal.

After the match the red h-marked balls are removed and the rest of the balls are placed back in the skill pool.

## Running

### Prerequisites

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then install the dependencies:

```bash
uv sync
```

### Run a match

```bash
uv run streamlit run src/football_urn_model/app.py   # play one match by hand in the browser
```

The app plays one match by hand: each press of "Next draw" makes one draw (a number of balls from one urn), the
same steps as playing with real urns. Every model parameter and both teams' red balls are adjustable in the sidebar.

### Run a season

```bash
uv run simulate       # simulate one season with the starting parameters and print the league table
```

The script simulates the Premier League 2025/26 fixture list once and prints the league table: each team's red
balls, its real final points and its simulated points, followed by the shots and goals per match. The red balls
scale linearly with the real final points, from 10 for the weakest team to 25 for the strongest (`red_min` and
`red_max`). The season is fetched from Understat on the first run and cached in `~/soccerdata`. All parameters are in
`model_settings()` in `src/football_urn_model/simulate.py`.
