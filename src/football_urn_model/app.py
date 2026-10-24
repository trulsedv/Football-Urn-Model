"""Play one match by hand: one button press per draw, one table row per round, every model parameter adjustable."""

import numpy as np
import pandas as pd
import streamlit as st

from football_urn_model.simulate import model_settings, play_match


def main() -> None:
    st.set_page_config(page_title="Football Urn Model", layout="wide")
    st.title("Play a match")
    settings, home_red_balls, away_red_balls, seed = sidebar_settings()

    state = st.session_state
    # A new match gets the next seed; the button's callback runs before the sidebar reads the seed.
    if st.button("New match", on_click=lambda: state.update(seed=state["seed"] + 1)) or "steps" not in state:
        rng = np.random.default_rng(seed)
        state["steps"] = play_match(home_red_balls, away_red_balls, settings, rng)
        state.update({"urns": {}, "rows": [], "score": {True: 0, False: 0}, "is_over": False})
        state["rounds"] = settings["rounds"]

    columns = st.columns([1, 1, 1, 5])
    if columns[0].button("Next draw", type="primary", disabled=state["is_over"]):
        advance(0)
    if columns[1].button("Next round", disabled=state["is_over"]):
        advance(1)
    if columns[2].button("Next 5 rounds", disabled=state["is_over"]):
        advance(5)

    score = state["score"]
    played = len(state["rows"])
    full_time = " · full time" if state["is_over"] else ""
    st.header(f"Home {score[True]} - {score[False]} Away (round {played} of {state['rounds']}{full_time})")
    for is_home, (size, red, extra) in state["urns"].items():
        h_marked = f", plus {extra} h-marked red" if extra else ""
        st.write(f"{'Home' if is_home else 'Away'} match urn: {red} red of {size} from the skill pool{h_marked}")
    show_rounds(state["rows"])


def sidebar_settings() -> tuple[dict[str, int], int, int, int]:
    """Show an input for every model parameter, starting from model_settings().

    Returns:
        The model settings, the home and away team's red balls in the skill pool, and the random seed.

    """
    st.sidebar.caption("Changes apply from the next New match.")
    st.sidebar.header("Teams")
    home_red_balls = st.sidebar.number_input("home red balls in skill pool", min_value=0, value=20)
    away_red_balls = st.sidebar.number_input("away red balls in skill pool", min_value=0, value=15)
    st.session_state.setdefault("seed", 1)
    seed = st.sidebar.number_input("random seed", min_value=0, key="seed")
    st.sidebar.header("Model parameters")
    settings = {
        name: int(st.sidebar.number_input(name, min_value=0, value=value))
        for name, value in model_settings().items()
        if name not in {"red_min", "red_max"}  # only used to give a whole league starting red balls
    }
    return settings, int(home_red_balls), int(away_red_balls), int(seed)


def advance(rounds: int) -> None:
    """Make the next draw (rounds = 0), or keep drawing until `rounds` more rounds have ended."""
    state = st.session_state
    rounds_ended = 0
    while True:
        step = next(state["steps"], None)
        if step is None:
            state["is_over"] = True
            return
        record(step)
        # A round ends with a white ball from the tempo urn, or with the draw from the shot urn.
        is_round_over = step[0] == "goal" or (step[0] == "tempo" and not step[2])
        state["is_over"] = is_round_over and len(state["rows"]) == state["rounds"]
        rounds_ended += is_round_over
        if state["is_over"] or rounds_ended >= rounds:
            return


def record(step: tuple) -> None:
    """Write one step of simulate.play_match into the match: the match urns, or a cell of the current round's row."""
    state = st.session_state
    name, *values = step
    row = state["rows"][-1] if state["rows"] else {}
    if name == "match urn":
        state["urns"][values[0]] = values[1:]
    elif name == "tempo":
        state["rows"].append(
            {
                "shot": balls(values[1], 1),
                "grab": {True: "", False: ""},
                "chance": {True: "", False: ""},
                "xg": "",
                "kind": "",
                "goal": "",
            },
        )
    elif name == "grab":
        is_home, draws, red = values
        row["grab"][is_home] = balls(red, draws)
    elif name == "tie-break":
        home_is_red, away_is_red, is_put_back = values
        # ↺: an urn ran empty, so all balls went back first.
        row["grab"][True] += f"{' ↺' if is_put_back else ''} {balls(home_is_red, 1)}"
        row["grab"][False] += f"{' ↺' if is_put_back else ''} {balls(away_is_red, 1)}"
    elif name == "fair draw":
        row["grab"][values[0]] += " (fair draw)"
    elif name == "chance balls":
        is_home, draws, red, is_big_chance = values
        row["chance"][is_home] = balls(red, draws)
        row["kind"] = "<b>big chance</b>" if is_big_chance else ""
    elif name == "defender balls":
        is_home, draws, red, shot_urn_red, shot_urn_size = values
        row["chance"][is_home] = balls(red, draws)
        row["xg"] = f"{shot_urn_red / shot_urn_size:.2f} ({shot_urn_red}/{shot_urn_size})"
    elif name == "goal":
        is_home, _, _, is_goal = values
        row["goal"] = "GOAL" if is_goal else "-"
        state["score"][is_home] += is_goal


def show_rounds(rows: list[dict]) -> None:
    """Show one row per round, newest first; phases 4 and 5 show the home team's balls above the away team's."""
    table = pd.DataFrame(
        {
            "Round": range(1, len(rows) + 1),
            "Shot": [row["shot"] for row in rows],
            "Home/Away": [both_teams(row["grab"]) for row in rows],
            "Chance": [both_teams(row["chance"]) for row in rows],
            "xG": ["<br>".join(filter(None, [row["xg"], row["kind"]])) for row in rows],
            "Goal": [row["goal"] for row in rows],
        },
    ).iloc[::-1]
    st.markdown(table.to_html(index=False, escape=False), unsafe_allow_html=True)


def balls(red: int, total: int) -> str:
    """Write drawn balls as letters, red first: two red of three is RRW, with R in red.

    Returns:
        HTML for the balls.

    """
    red_balls = f'<span style="color: #d62728">{"R" * red}</span>'
    return f'<span style="font-family: monospace">{red_balls}{"W" * (total - red)}</span>'


def both_teams(cell: dict[bool, str]) -> str:
    """Put the home team's balls above the away team's, or nothing if neither team drew.

    Returns:
        HTML for one table cell.

    """
    return f"<i>H</i> {cell[True]}<br><i>A</i> {cell[False]}" if cell[True] or cell[False] else ""


if __name__ == "__main__":
    main()
