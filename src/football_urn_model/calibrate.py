"""Calibrate the urn model: fit each parameter against the real statistic it changes, then compare all statistics."""

import numpy as np
import pandas as pd

from football_urn_model.data import final_points, load_season
from football_urn_model.simulate import model_settings, simulate_season, starting_red_balls


def main() -> None:
    settings = model_settings()
    schedule, shots = load_season("2025")  # Understat season 2025 = 2025/26
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
    real_shares = team_shot_shares(real_shots, schedule)

    # 1. Tempo urn: set directly from the real mean number of shots per match.
    settings["tempo_urn_size"] = settings["rounds"]
    settings["tempo_urn_red"] = round(real["shots per match"])
    print(f"Tempo urn: {settings['tempo_urn_red']} red of {settings['tempo_urn_size']}, {settings['rounds']} rounds\n")

    # 2. Team red balls against each team's share of shots, then 3-5 one parameter at a time, then red balls again,
    # since the other parameters also move the shares.
    red_balls = fit_red_balls(schedule, starting_red_balls(final_points(schedule), settings), real_shares, settings)
    for step in fitting_plan():
        parameter, _, statistic = step
        settings[parameter] = best_value(schedule, red_balls, settings, step, real[statistic])
    red_balls = fit_red_balls(schedule, red_balls, real_shares, settings)

    simulated, simulated_shares = evaluate(schedule, red_balls, settings)
    teams = pd.DataFrame({"red balls": red_balls, "real shot share": real_shares, "simulated": simulated_shares})
    teams["real points"] = final_points(schedule)
    print(teams.sort_values("red balls", ascending=False).to_string(float_format="{:.3f}".format))
    print(f"\nFitted settings: {settings}\n")
    seasons = calibration_settings()["seasons"]
    comparison = pd.DataFrame({"real": real, f"simulated (mean of {seasons} seasons)": simulated})
    print("Real 2025/26 vs the calibrated model (real xG is Understat's, uncorrected; xG is not fitted):")
    print(comparison.to_string(float_format="{:.3f}".format))


def calibration_settings() -> dict[str, int]:
    """Return how much simulation each evaluation uses.

    Returns:
        Setting name to value.

    """
    return {
        "seasons": 10,  # simulated seasons per evaluation
        "seed": 1,  # the same seed for every evaluation, so parameter values are compared on the same draws
        "red_ball_iterations": 6,
    }


def fitting_plan() -> list[tuple[str, list[int], str]]:
    """List the parameters fitted one at a time: (parameter, candidate values, statistic it is fitted against).

    Returns:
        The fitting steps, in order.

    """
    return [
        ("home_extra_red", [0, 1, 2, 3, 4], "home shots per match"),
        ("match_urn_size", [8, 10, 15, 20, 30, 50], "sd of home shot share per match"),
        ("marked_white", [5, 10, 15, 20, 25, 30, 40], "goals per match"),
    ]


def fit_red_balls(
    schedule: pd.DataFrame,
    red_balls: dict[str, int],
    real_shares: pd.Series,
    settings: dict[str, int],
) -> dict[str, int]:
    """Adjust each team's red balls until its simulated share of shots matches the real share.

    Returns:
        Red balls in the skill pool per team.

    """
    for iteration in range(calibration_settings()["red_ball_iterations"]):
        _, shares = evaluate(schedule, red_balls, settings)
        error = (shares - real_shares).abs().max()
        print(f"Red balls, iteration {iteration + 1}: largest shot share error {error:.3f}")
        # A team with too small a share gets more red balls, in proportion to how far off it is.
        adjusted = pd.Series(red_balls) * real_shares / shares
        red_balls = adjusted.round().clip(1, settings["skill_pool_size"] - 1).astype(int).to_dict()
    print()
    return red_balls


def best_value(
    schedule: pd.DataFrame,
    red_balls: dict[str, int],
    settings: dict[str, int],
    step: tuple[str, list[int], str],
    target: float,
) -> int:
    """Try each candidate value of one parameter and keep the one whose statistic is closest to the real one.

    Returns:
        The best value.

    """
    parameter, values, statistic = step
    results = {}
    for value in values:
        simulated, _ = evaluate(schedule, red_balls, {**settings, parameter: value})
        results[value] = simulated[statistic]
    best = min(results, key=lambda value: abs(results[value] - target))
    tried = ", ".join(f"{value}: {result:.3f}" for value, result in results.items())
    print(f"{parameter} against {statistic} (real {target:.3f}). Tried {tried}. Best: {best}\n")
    return best


def evaluate(
    schedule: pd.DataFrame,
    red_balls: dict[str, int],
    settings: dict[str, int],
) -> tuple[pd.Series, pd.Series]:
    """Simulate several seasons and average their statistics.

    Returns:
        The mean of each statistic, and the mean share of shots per team.

    """
    calibration = calibration_settings()
    rng = np.random.default_rng(calibration["seed"])
    statistics, shares = [], []
    for _ in range(calibration["seasons"]):
        shots, matches = simulate_season(schedule, red_balls, settings, rng)
        statistics.append(describe_season(shots, matches))
        shares.append(team_shot_shares(shots, matches))
    return pd.DataFrame(statistics).mean(), pd.concat(shares, axis=1).mean(axis=1)


def describe_season(shots: pd.DataFrame, matches: pd.DataFrame) -> dict[str, float]:
    """Summary statistics for comparing a simulated season with the real one.

    Returns:
        Statistic name to value.

    """
    shot_counts = pd.crosstab(shots["game_id"], shots["is_home"]).reindex(matches["game_id"], fill_value=0)
    total_shots = shot_counts[True] + shot_counts[False]
    home_goals, away_goals = matches["home_goals"], matches["away_goals"]
    points = final_points(matches)
    big_chance_xg = 0.3
    return {
        "shots per match": total_shots.mean(),
        "variance of shots per match": total_shots.var(),
        "home shots per match": shot_counts[True].mean(),
        "away shots per match": shot_counts[False].mean(),
        "sd of home shot share per match": (shot_counts[True] / total_shots).std(),
        "goals per match": (home_goals + away_goals).mean(),
        "home win rate": (home_goals > away_goals).mean(),
        "draw rate": (home_goals == away_goals).mean(),
        "0-0 rate": ((home_goals == 0) & (away_goals == 0)).mean(),
        "mean xG per shot": shots["xg"].mean(),
        "sd of xG per shot": shots["xg"].std(),
        "share of shots with xG > 0.3": (shots["xg"] > big_chance_xg).mean(),
        "final points, sd": points.std(),
        "final points, max": points.max(),
        "final points, min": points.min(),
    }


def team_shot_shares(shots: pd.DataFrame, matches: pd.DataFrame) -> pd.Series:
    """Compute each team's share of all shots in its matches over the season.

    Returns:
        Share of shots per team.

    """
    shot_counts = pd.crosstab(shots["game_id"], shots["is_home"]).reindex(matches["game_id"], fill_value=0)
    home, away = shot_counts[True].to_numpy(), shot_counts[False].to_numpy()
    per_team = (
        pd
        .concat(
            [
                pd.DataFrame({"team": matches["home_team"].to_numpy(), "own": home, "against": away}),
                pd.DataFrame({"team": matches["away_team"].to_numpy(), "own": away, "against": home}),
            ],
        )
        .groupby("team")[["own", "against"]]
        .sum()
    )
    return per_team["own"] / (per_team["own"] + per_team["against"])
