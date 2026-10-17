"""Load one Premier League season from Understat, shared by the analyses."""

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

    draw = schedule["home_goals"] == schedule["away_goals"]
    home_points = 3 * (schedule["home_goals"] > schedule["away_goals"]) + draw
    away_points = 3 * (schedule["away_goals"] > schedule["home_goals"]) + draw
    points_per_venue = [
        home_points.groupby(schedule["home_team"]).sum(),
        away_points.groupby(schedule["away_team"]).sum(),
    ]
    final_points = pd.concat(points_per_venue).groupby(level=0).sum()
    home_final_points = final_points[schedule["home_team"]].to_numpy()
    away_final_points = final_points[schedule["away_team"]].to_numpy()
    schedule["d"] = home_final_points - away_final_points
    schedule["points_sum"] = home_final_points + away_final_points
    return schedule, shots
