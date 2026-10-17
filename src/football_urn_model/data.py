"""Load one Premier League season from Understat, and compute final points; shared by the other modules."""

import pandas as pd
import soccerdata as sd


def load_season(season: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fetch matches and shots for one season (Understat season 2025 = 2025/26).

    Returns:
        The schedule with d = home - away final points and points_sum = their sum, and all shots except own goals.

    """
    understat = sd.Understat(leagues="ENG-Premier League", seasons=season)
    schedule = understat.read_schedule().reset_index()
    shots = understat.read_shot_events().reset_index()
    shots = shots[shots["result"] != "Own Goal"]

    points = final_points(schedule)
    home_final_points = points[schedule["home_team"]].to_numpy()
    away_final_points = points[schedule["away_team"]].to_numpy()
    schedule["d"] = home_final_points - away_final_points
    schedule["points_sum"] = home_final_points + away_final_points
    return schedule, shots


def final_points(matches: pd.DataFrame) -> pd.Series:
    """Compute each team's final points from home_team, away_team, home_goals and away_goals.

    Returns:
        Final points per team.

    """
    home_goals, away_goals = matches["home_goals"], matches["away_goals"]
    home_points = 3 * (home_goals > away_goals) + (home_goals == away_goals)
    away_points = 3 * (away_goals > home_goals) + (home_goals == away_goals)
    points_per_venue = [
        home_points.groupby(matches["home_team"]).sum(),
        away_points.groupby(matches["away_team"]).sum(),
    ]
    return pd.concat(points_per_venue).groupby(level=0).sum().rename_axis("team")
