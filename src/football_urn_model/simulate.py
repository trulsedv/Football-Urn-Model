"""Simulate Premier League seasons with the urn model and compare them with the real 2025/26 season."""

import numpy as np
import pandas as pd

from football_urn_model.data import load_season


def main() -> None:
    settings = model_settings()
    rng = np.random.default_rng(settings["seed"])
    schedule, shots = load_season("2025")  # Understat season 2025 = 2025/26

    # Placeholder skill until the model is fitted: red balls scale linearly with the team's real final points.
    home_team_final_points = (schedule["points_sum"] + schedule["d"]) // 2
    final_points = home_team_final_points.groupby(schedule["home_team"]).first().rename_axis("team")
    scaled = (final_points - final_points.min()) / (final_points.max() - final_points.min())
    red_balls = (settings["red_min"] + scaled * (settings["red_max"] - settings["red_min"])).round().astype(int)

    shots = shots.merge(schedule[["game_id", "home_team_id"]], on="game_id")
    real_shots = pd.DataFrame(
        {
            "game_id": shots["game_id"],
            "is_home": shots["team_id"] == shots["home_team_id"],
            "xg": shots["xg"].astype(float),
            "is_goal": shots["result"] == "Goal",
        },
    )
    real = describe_season(real_shots, schedule)

    simulated = []
    for _ in range(settings["seasons"]):
        simulated_shots, simulated_matches = simulate_season(schedule, red_balls.to_dict(), settings, rng)
        simulated.append(describe_season(simulated_shots, simulated_matches))

    comparison = pd.DataFrame({"real": real, "simulated (mean)": pd.DataFrame(simulated).mean()})
    print(f"Red balls per team (of {settings['skill_pool_size']}):\n{red_balls.sort_values().to_string()}\n")
    print(f"Real 2025/26 vs {settings['seasons']} simulated seasons (real xG is Understat's, uncorrected):")
    print(comparison.to_string(float_format="{:.3f}".format))


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
        "seasons": 20,
        "seed": 1,
    }


def simulate_season(
    schedule: pd.DataFrame,
    red_balls: dict[str, int],
    settings: dict[str, int],
    rng: np.random.Generator,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Play every fixture of the schedule; skill pools do not change during the season (phase 1).

    Returns:
        One row per shot (game_id, is_home, xg, is_goal), and the schedule with the simulated goals.

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
    """Play one match, phases 2 to 6.

    Returns:
        One dict per shot: is_home, xg and is_goal.

    """
    # Phase 2: fill the match urns from the skill pools; the home team adds extra red balls. Urns are (red, size).
    pool_size, urn_size = settings["skill_pool_size"], settings["match_urn_size"]
    home_red = rng.hypergeometric(home_red_balls, pool_size - home_red_balls, urn_size) + settings["home_extra_red"]
    away_red = rng.hypergeometric(away_red_balls, pool_size - away_red_balls, urn_size)
    urns = {True: (home_red, urn_size + settings["home_extra_red"]), False: (away_red, urn_size)}

    shots = []
    for _ in range(settings["rounds"]):
        # Phase 3: one draw from the tempo urn decides whether there is a shot this round.
        if rng.integers(settings["tempo_urn_size"]) >= settings["tempo_urn_red"]:
            continue
        is_home, margin = who_shoots(urns[True], urns[False], settings["who_shoots_draws"], rng)
        if margin >= settings["big_chance_margin"]:
            marked_balls = (settings["big_chance_marked_red"], settings["big_chance_marked_white"])
        else:
            marked_balls = (settings["marked_red"], settings["marked_white"])

        xg, is_goal = shoot(urns[is_home], urns[not is_home], marked_balls, settings, rng)
        shots.append({"is_home": is_home, "xg": xg, "is_goal": is_goal})
    return shots


def who_shoots(
    home_urn: tuple[int, int],
    away_urn: tuple[int, int],
    draws: int,
    rng: np.random.Generator,
) -> tuple[bool, int]:
    """Phase 4: both teams grab `draws` balls; more red balls shoots, ties are broken one ball at a time.

    Returns:
        Whether the home team shoots, and the winning margin in red balls (0 when won in a tie-break).

    """
    (home_red, home_size), (away_red, away_size) = home_urn, away_urn
    home_drawn = rng.hypergeometric(home_red, home_size - home_red, draws)
    away_drawn = rng.hypergeometric(away_red, away_size - away_red, draws)
    if home_drawn != away_drawn:
        return bool(home_drawn > away_drawn), abs(int(home_drawn) - int(away_drawn))

    # Tie: draw one ball each from what is left until the colours differ; if a urn runs empty, put all balls back.
    home_left = [home_red - home_drawn, home_size - draws]
    away_left = [away_red - away_drawn, away_size - draws]
    while True:
        if home_left[1] == 0 or away_left[1] == 0:
            home_left, away_left = [home_red, home_size], [away_red, away_size]
        home_is_red = rng.integers(home_left[1]) < home_left[0]
        away_is_red = rng.integers(away_left[1]) < away_left[0]
        if home_is_red != away_is_red:
            return bool(home_is_red), 0
        home_left = [home_left[0] - home_is_red, home_left[1] - 1]
        away_left = [away_left[0] - away_is_red, away_left[1] - 1]


def shoot(
    shooter_urn: tuple[int, int],
    defender_urn: tuple[int, int],
    marked_balls: tuple[int, int],
    settings: dict[str, int],
    rng: np.random.Generator,
) -> tuple[float, bool]:
    """Phases 5 and 6: the defender's red balls cancel red chance balls, marked balls are added, one ball decides.

    Returns:
        The shot's xG (red share of the shot urn) and whether it is a goal.

    """
    (shooter_red, shooter_size), (defender_red, defender_size) = shooter_urn, defender_urn
    chance_red = rng.hypergeometric(shooter_red, shooter_size - shooter_red, settings["chance_draws"])
    defender_drawn = rng.hypergeometric(defender_red, defender_size - defender_red, settings["defender_draws"])
    cancelled = min(chance_red, defender_drawn)
    marked_red, marked_white = marked_balls
    shot_urn_red = chance_red - cancelled + marked_red
    shot_urn_size = settings["chance_draws"] - cancelled + marked_red + marked_white

    # One ball from the shot urn; red is a goal. Unmarked balls then go back into the match urns.
    is_goal = rng.integers(shot_urn_size) < shot_urn_red
    return shot_urn_red / shot_urn_size, bool(is_goal)


def describe_season(shots: pd.DataFrame, matches: pd.DataFrame) -> dict[str, float]:
    """Summary statistics for comparing a simulated season with the real one.

    Returns:
        Statistic name to value.

    """
    shot_counts = pd.crosstab(shots["game_id"], shots["is_home"]).reindex(matches["game_id"], fill_value=0)
    total_shots = shot_counts[True] + shot_counts[False]
    home_goals, away_goals = matches["home_goals"], matches["away_goals"]
    home_points = 3 * (home_goals > away_goals) + (home_goals == away_goals)
    away_points = 3 * (away_goals > home_goals) + (home_goals == away_goals)
    big_chance_xg = 0.3
    final_points = (
        pd
        .concat(
            [home_points.groupby(matches["home_team"]).sum(), away_points.groupby(matches["away_team"]).sum()],
        )
        .groupby(level=0)
        .sum()
    )
    return {
        "shots per match": total_shots.mean(),
        "variance of shots per match": total_shots.var(),
        "home shots per match": shot_counts[True].mean(),
        "away shots per match": shot_counts[False].mean(),
        "goals per match": (home_goals + away_goals).mean(),
        "home win rate": (home_goals > away_goals).mean(),
        "draw rate": (home_goals == away_goals).mean(),
        "0-0 rate": ((home_goals == 0) & (away_goals == 0)).mean(),
        "mean xG per shot": shots["xg"].mean(),
        "sd of xG per shot": shots["xg"].std(),
        "share of shots with xG = 0": (shots["xg"] == 0).mean(),
        "share of shots with xG > 0.3": (shots["xg"] > big_chance_xg).mean(),
        "final points, sd": final_points.std(),
        "final points, max": final_points.max(),
        "final points, min": final_points.min(),
    }
