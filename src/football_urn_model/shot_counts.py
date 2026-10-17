"""Analysis 1: how shot counts depend on skill difference d (home - away final points) and on the points sum."""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from football_urn_model.data import load_season


def main() -> None:
    season = "2025"  # Understat season 2025 = 2025/26
    bin_width = 10
    output_dir = Path("output")

    matches = load_matches(season)
    matches["total_shots"] = matches["home_shots"] + matches["away_shots"]
    matches["d_bin"] = (matches["d"] // bin_width) * bin_width

    summary = summarise_bins(matches)
    print(summary.to_string(index=False, float_format="{:.2f}".format))

    output_dir.mkdir(exist_ok=True)
    summary.to_csv(output_dir / "shot_counts_by_d.csv", index=False)
    plot_landscape(matches, bin_width).write_html(output_dir / "shot_counts_by_d.html")
    print(f"\nWrote {output_dir}/shot_counts_by_d.csv and {output_dir}/shot_counts_by_d.html")

    # Does the total depend on how strong the two teams are together, rather than on their difference?
    matches["sum_bin"] = (matches["points_sum"] // bin_width) * bin_width
    total_by_sum = matches.groupby("sum_bin")["total_shots"].agg(["size", "mean", "var"]).reset_index()
    print(f"\nCorrelation of total shots with d: {matches['total_shots'].corr(matches['d']):.3f}")
    print(f"Correlation of total shots with points sum: {matches['total_shots'].corr(matches['points_sum']):.3f}\n")
    print(total_by_sum.to_string(index=False, float_format="{:.2f}".format))
    total_by_sum.to_csv(output_dir / "total_shots_by_points_sum.csv", index=False)
    print(f"\nWrote {output_dir}/total_shots_by_points_sum.csv")


def load_matches(season: str) -> pd.DataFrame:
    schedule, shots = load_season(season)
    shot_counts = shots.groupby(["game_id", "team_id"]).size()

    # Teams without a shot in a match have no rows in the shot data, so they get 0.
    home_keys = pd.MultiIndex.from_arrays([schedule["game_id"], schedule["home_team_id"]])
    away_keys = pd.MultiIndex.from_arrays([schedule["game_id"], schedule["away_team_id"]])
    return pd.DataFrame(
        {
            "home_team": schedule["home_team"],
            "away_team": schedule["away_team"],
            "home_shots": shot_counts.reindex(home_keys, fill_value=0).to_numpy(),
            "away_shots": shot_counts.reindex(away_keys, fill_value=0).to_numpy(),
            "d": schedule["d"],
            "points_sum": schedule["points_sum"],
        },
    )


def summarise_bins(matches: pd.DataFrame) -> pd.DataFrame:
    bins = matches.groupby("d_bin")
    summary = pd.DataFrame({"matches": bins.size()})
    for side in ["home", "away", "total"]:
        summary[f"{side}_mean"] = bins[f"{side}_shots"].mean()
        summary[f"{side}_var"] = bins[f"{side}_shots"].var()
        summary[f"{side}_dispersion"] = summary[f"{side}_var"] / summary[f"{side}_mean"]
    return summary.reset_index()


def plot_landscape(matches: pd.DataFrame, bin_width: int) -> go.Figure:
    """Plot P(k shots | d-bin) for home, away and total shots.

    Returns:
        Side-by-side heatmaps with the bin mean drawn as a line.

    """
    figure = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=["Home shots", "Away shots", "Total shots"],
        shared_yaxes=True,
    )
    for col, side in enumerate(["home", "away", "total"], start=1):
        counts = pd.crosstab(matches[f"{side}_shots"], matches["d_bin"])
        probabilities = counts / counts.sum()
        means = matches.groupby("d_bin")[f"{side}_shots"].mean()
        figure.add_trace(
            go.Heatmap(
                x=probabilities.columns + bin_width / 2,
                y=probabilities.index,
                z=probabilities.to_numpy(),
                coloraxis="coloraxis",
                hovertemplate="d bin centre %{x}<br>k = %{y} shots<br>P = %{z:.2f}<extra></extra>",
            ),
            row=1,
            col=col,
        )
        figure.add_trace(
            go.Scatter(x=means.index + bin_width / 2, y=means.to_numpy(), mode="lines+markers", name=f"{side} mean"),
            row=1,
            col=col,
        )
        figure.update_xaxes(title_text="d = home final points - away final points", row=1, col=col)
    figure.update_yaxes(title_text="shots in match (k)", row=1, col=1)
    figure.update_layout(title="P(k shots | d), Premier League 2025/26", coloraxis={"colorscale": "Viridis"})
    return figure


if __name__ == "__main__":
    main()
