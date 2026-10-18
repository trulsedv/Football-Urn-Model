"""Play one match by hand: one button press per draw, with every model parameter adjustable."""

import numpy as np
import streamlit as st

from football_urn_model.simulate import model_settings, play_match


def main() -> None:
    st.set_page_config(page_title="Football Urn Model", layout="wide")
    st.title("Play a match")
    settings, home_red_balls, away_red_balls, seed = sidebar_settings()

    state = st.session_state
    if st.button("New match") or "steps" not in state:
        rng = np.random.default_rng(seed)
        state["steps"] = play_match(home_red_balls, away_red_balls, settings, rng)
        state.update({"log": [], "round": 0, "score": {True: 0, False: 0}, "is_over": False})

    if st.button("Next draw", type="primary", disabled=state["is_over"]):
        step = next(state["steps"], None)
        if step is None:
            state["is_over"] = True
            state["log"].append("Full time.")
        else:
            state["log"].append(describe(step))
            if step[0] == "tempo":
                state["round"] = step[1]
            if step[0] == "goal" and step[4]:
                state["score"][step[1]] += 1

    score = state["score"]
    st.header(f"Home {score[True]} - {score[False]} Away (round {state['round']} of {settings['rounds']})")
    for line in reversed(state["log"]):
        st.write(line)


def sidebar_settings() -> tuple[dict[str, int], int, int, int]:
    """Show an input for every model parameter, starting from model_settings().

    Returns:
        The model settings, the home and away team's red balls in the skill pool, and the random seed.

    """
    st.sidebar.caption("Changes apply from the next New match.")
    st.sidebar.header("Teams")
    home_red_balls = st.sidebar.number_input("home red balls in skill pool", min_value=0, value=20)
    away_red_balls = st.sidebar.number_input("away red balls in skill pool", min_value=0, value=15)
    seed = st.sidebar.number_input("random seed", min_value=0, value=1)
    st.sidebar.header("Model parameters")
    settings = {
        name: int(st.sidebar.number_input(name, min_value=0, value=value))
        for name, value in model_settings().items()
        if name not in {"red_min", "red_max"}  # only used to give a whole league starting red balls
    }
    return settings, int(home_red_balls), int(away_red_balls), int(seed)


def describe(step: tuple) -> str:
    """Spell out one step of simulate.play_match as what happened at the table.

    Returns:
        One line of text.

    """
    team = {True: "Home", False: "Away"}
    colour = {True: "red", False: "white"}
    texts = {
        "match urn": lambda is_home, size, red, extra: (
            f"Phase 2 · {team[is_home]} draws {size} balls from its skill pool into its match urn: {red} red."
            + (f" It adds {extra} extra red (home advantage)." if extra else "")
        ),
        "tempo": lambda round_number, is_shot: (
            f"Round {round_number}, phase 3 · Tempo urn: {colour[is_shot]}, {'a shot' if is_shot else 'no shot'}."
        ),
        "grab": lambda is_home, draws, red: (
            f"Phase 4 · {team[is_home]} grabs {draws} balls from its match urn: {red} red."
        ),
        "fair draw": lambda is_home: f"Phase 4 · Both urns hold one colour only; a fair draw picks {team[is_home]}.",
        "tie-break": lambda home_is_red, away_is_red, is_put_back: (
            "Phase 4 · Tie. "
            + ("An urn ran empty, so all balls go back. " if is_put_back else "")
            + f"One more ball each: home {colour[home_is_red]}, away {colour[away_is_red]}."
        ),
        "chance balls": lambda is_home, draws, red: f"Phase 5 · {team[is_home]} draws {draws} chance balls: {red} red.",
        "defender balls": lambda is_home, draws, red, cancelled, marked_red, marked_white: (
            f"Phase 5 · {team[is_home]} defends, drawing {draws} balls: {red} red, cancelling {cancelled} red."
            f" Add {marked_red} marked red and {marked_white} marked white to the shot urn."
        ),
        "goal": lambda is_home, is_big_chance, xg, is_goal: (
            f"Phase 6 · {team[is_home]} shoots ({'big chance' if is_big_chance else 'ordinary shot'}, xG {xg:.2f})."
            f" One ball from the shot urn: {'red: GOAL!' if is_goal else 'white: no goal.'}"
        ),
    }
    name, *values = step
    return texts[name](*values)


if __name__ == "__main__":
    main()
