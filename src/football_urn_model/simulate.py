"""The urn model: simulate a Premier League season, phase by phase (see docs/design.md)."""

from collections.abc import Generator

import numpy as np
import pandas as pd

from football_urn_model.data import final_points, load_season


def main() -> None:
    settings = model_settings()
    rng = np.random.default_rng(1)
    schedule, _ = load_season("2025")  # the real 2025/26 fixture list; Understat season 2025 = 2025/26
    real_points = final_points(schedule)
    red_balls = starting_red_balls(real_points, settings)

    shots, matches = simulate_season(schedule, red_balls, settings, rng)
    table = pd.DataFrame(
        {"red balls": red_balls, "real points": real_points, "simulated points": final_points(matches)},
    ).sort_values("simulated points", ascending=False)
    print(f"One simulated season with the starting settings (red balls of {settings['skill_pool_size']}):\n")
    print(table.to_string())
    goals_per_match = (matches["home_goals"] + matches["away_goals"]).mean()
    print(f"\nShots per match: {len(shots) / len(matches):.2f}, goals per match: {goals_per_match:.2f}")


def model_settings() -> dict[str, int]:
    """Return starting values for every model parameter; none of them is decided yet.

    Returns:
        Parameter name to value. Comments give the notation in docs/design.md.

    """
    return {
        "skill_pool_size": 100,  # M_s
        "red_min": 10,  # red balls in the skill pool of the weakest team
        "red_max": 25,  # ... and of the strongest team
        "match_urn_size": 20,  # M_u
        "home_extra_red": 1,  # m_h
        "rounds": 100,  # n
        "tempo_urn_size": 4,  # M_t
        "tempo_urn_red": 1,  # m_t; average shots per match = rounds * tempo_urn_red / tempo_urn_size
        "who_shoots_draws": 3,  # k_w
        "chance_draws": 5,  # k_c
        "defender_draws": 1,  # k_d
        "big_chance_margin": 2,  # winning phase 4 by at least this many red balls makes the shot a big chance
        "marked_red": 1,  # marked balls added to the shot urn of an ordinary shot; marked red counts as red
        "marked_white": 20,
        "big_chance_marked_red": 8,  # ... and of a big chance
        "big_chance_marked_white": 12,
    }


def starting_red_balls(points: pd.Series, settings: dict[str, int]) -> dict[str, int]:
    """Give each team red balls scaling linearly with its final points, from red_min to red_max.

    Returns:
        Red balls in the skill pool per team; a starting point for calibration.

    """
    scaled = (points - points.min()) / (points.max() - points.min())
    red_balls = settings["red_min"] + scaled * (settings["red_max"] - settings["red_min"])
    return red_balls.round().astype(int).to_dict()


def simulate_season(
    schedule: pd.DataFrame,
    red_balls: dict[str, int],
    settings: dict[str, int],
    rng: np.random.Generator,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Play every fixture of the schedule; skill pools do not change during the season (phase 1).

    Returns:
        One row per shot (game_id, is_home, is_big_chance, xg, is_goal), and the schedule with the simulated goals.

    """
    rows = []
    for game_id, home_team, away_team in schedule[["game_id", "home_team", "away_team"]].itertuples(index=False):
        match_shots = simulate_match(red_balls[home_team], red_balls[away_team], settings, rng)
        rows.extend({"game_id": game_id, **shot} for shot in match_shots)

    shots = pd.DataFrame(rows)
    goals = shots[shots["is_goal"]].groupby(["game_id", "is_home"]).size()
    matches = schedule[["game_id", "home_team", "away_team"]].copy()
    matches["home_goals"] = [goals.get((game_id, True), 0) for game_id in matches["game_id"]]
    matches["away_goals"] = [goals.get((game_id, False), 0) for game_id in matches["game_id"]]
    return shots, matches


def simulate_match(
    home_red_balls: int,
    away_red_balls: int,
    settings: dict[str, int],
    rng: np.random.Generator,
) -> list[dict[str, bool | float]]:
    """Play one match, phases 2 to 6, keeping only the shots.

    Returns:
        One dict per shot: is_home, is_big_chance, xg and is_goal.

    """
    steps = play_match(home_red_balls, away_red_balls, settings, rng)
    keys = ["is_home", "is_big_chance", "xg", "is_goal"]
    return [dict(zip(keys, values, strict=True)) for step, *values in steps if step == "goal"]


def play_match(
    home_red_balls: int,
    away_red_balls: int,
    settings: dict[str, int],
    rng: np.random.Generator,
) -> Generator[tuple]:
    """Play one match, phases 2 to 6, one physical step (a draw of one or more balls) at a time.

    Yields:
        One tuple per step: its name, then what was drawn. The steps are spelled out in app.py.

    """
    # Phase 2: fill the match urns from the skill pools; the home team adds extra red balls. Urns are (red, size).
    pool_size, urn_size, home_extra = (
        settings["skill_pool_size"],
        settings["match_urn_size"],
        settings["home_extra_red"],
    )
    home_red = int(rng.hypergeometric(home_red_balls, pool_size - home_red_balls, urn_size))
    yield ("match urn", True, urn_size, home_red, home_extra)
    away_red = int(rng.hypergeometric(away_red_balls, pool_size - away_red_balls, urn_size))
    yield ("match urn", False, urn_size, away_red, 0)
    urns = {True: (home_red + home_extra, urn_size + home_extra), False: (away_red, urn_size)}

    for round_number in range(1, settings["rounds"] + 1):
        # Phase 3: one draw from the tempo urn decides whether there is a shot this round.
        is_shot = bool(rng.integers(settings["tempo_urn_size"]) < settings["tempo_urn_red"])
        yield ("tempo", round_number, is_shot)
        if not is_shot:
            continue
        is_home, margin = yield from who_shoots(urns[True], urns[False], settings["who_shoots_draws"], rng)
        is_big_chance = margin >= settings["big_chance_margin"]
        if is_big_chance:
            marked_balls = (settings["big_chance_marked_red"], settings["big_chance_marked_white"])
        else:
            marked_balls = (settings["marked_red"], settings["marked_white"])

        shot_urn_red, shot_urn_size = yield from build_shot_urn(urns, is_home, marked_balls, settings, rng)
        # Phase 6: one ball from the shot urn; red is a goal. Unmarked balls then go back into the match urns.
        is_goal = bool(rng.integers(shot_urn_size) < shot_urn_red)
        yield ("goal", is_home, is_big_chance, shot_urn_red / shot_urn_size, is_goal)


def who_shoots(
    home_urn: tuple[int, int],
    away_urn: tuple[int, int],
    draws: int,
    rng: np.random.Generator,
) -> Generator[tuple, None, tuple[bool, int]]:
    """Phase 4: both teams grab `draws` balls; more red balls shoots, ties are broken one ball at a time.

    Yields:
        Each draw: the grabs, then one tuple per tie-break draw.

    Returns:
        Whether the home team shoots, and the winning margin in red balls (0 when won in a tie-break).

    """
    (home_red, home_size), (away_red, away_size) = home_urn, away_urn
    home_drawn = int(rng.hypergeometric(home_red, home_size - home_red, draws))
    yield ("grab", True, draws, home_drawn)
    away_drawn = int(rng.hypergeometric(away_red, away_size - away_red, draws))
    yield ("grab", False, draws, away_drawn)
    if home_drawn != away_drawn:
        return home_drawn > away_drawn, abs(home_drawn - away_drawn)

    if home_red in {0, home_size} and away_red in {0, away_size}:
        # Both urns hold one colour only, so the tie can never be broken: a fair draw decides (an open question).
        is_home = bool(rng.integers(2) == 0)
        yield ("fair draw", is_home)
        return is_home, 0

    # Tie: draw one ball each from what is left until the colours differ; if a urn runs empty, put all balls back.
    home_left = [home_red - home_drawn, home_size - draws]
    away_left = [away_red - away_drawn, away_size - draws]
    while True:
        is_put_back = home_left[1] == 0 or away_left[1] == 0
        if is_put_back:
            home_left, away_left = [home_red, home_size], [away_red, away_size]
        home_is_red = bool(rng.integers(home_left[1]) < home_left[0])
        away_is_red = bool(rng.integers(away_left[1]) < away_left[0])
        yield ("tie-break", home_is_red, away_is_red, is_put_back)
        if home_is_red != away_is_red:
            return home_is_red, 0  # ruff: ignore[return-in-generator] - read by play_match with yield from
        home_left = [home_left[0] - home_is_red, home_left[1] - 1]
        away_left = [away_left[0] - away_is_red, away_left[1] - 1]


def build_shot_urn(
    urns: dict[bool, tuple[int, int]],
    is_home: bool,  # ruff: ignore[boolean-type-hint-positional-argument] - which team shoots, not a mode switch
    marked_balls: tuple[int, int],
    settings: dict[str, int],
    rng: np.random.Generator,
) -> Generator[tuple, None, tuple[int, int]]:
    """Phase 5: the defender's red balls cancel red chance balls, and the marked balls are added.

    Yields:
        The shooter's draw of chance balls, then the defender's draw (with the shot urn it leaves).

    Returns:
        The shot urn as (red, size); its red share is the shot's xG.

    """
    (shooter_red, shooter_size), (defender_red, defender_size) = urns[is_home], urns[not is_home]
    chance_red = int(rng.hypergeometric(shooter_red, shooter_size - shooter_red, settings["chance_draws"]))
    yield ("chance balls", is_home, settings["chance_draws"], chance_red)
    defender_drawn = int(rng.hypergeometric(defender_red, defender_size - defender_red, settings["defender_draws"]))
    cancelled = min(chance_red, defender_drawn)
    marked_red, marked_white = marked_balls
    shot_urn_red = chance_red - cancelled + marked_red
    shot_urn_size = settings["chance_draws"] - cancelled + marked_red + marked_white
    yield (
        "defender balls",
        not is_home,
        settings["defender_draws"],
        defender_drawn,
        cancelled,
        marked_red,
        marked_white,
    )
    return shot_urn_red, shot_urn_size  # ruff: ignore[return-in-generator] - read by play_match with yield from
