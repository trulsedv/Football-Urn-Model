"""Analysis 2: how the per-shot xG distribution depends on the shooting team's points advantage."""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from football_urn_model.data import load_season


def main() -> None:
    season = "2025"  # Understat season 2025 = 2025/26
    output_dir = Path("output")

    shots = load_shots(season)
    print(f"Excluded {shots['is_penalty'].sum()} penalties (fixed xG, not open chance creation).\n")
    shots = shots[~shots["is_penalty"]]

    summary = summarise_bins(shots)
    print(summary.to_string(index=False, float_format="{:.3f}".format))

    output_dir.mkdir(exist_ok=True)
    summary.to_csv(output_dir / "shot_quality_by_d.csv", index=False)
    plot_cumulative(shots).write_html(output_dir / "shot_quality_by_d.html")
    print(f"\nWrote {output_dir}/shot_quality_by_d.csv and {output_dir}/shot_quality_by_d.html")


def load_shots(season: str) -> pd.DataFrame:
    """Attach the shooting team's points advantage and a coarse bin of it to every shot.

    Returns:
        One row per shot with xG, shooter_d (shooting team - opponent final points) and its bin.

    """
    schedule, shots = load_season(season)
    shots = shots.merge(schedule[["game_id", "home_team_id", "d"]], on="game_id")
    is_home = shots["team_id"] == shots["home_team_id"]
    shooter_d = shots["d"].where(is_home, -shots["d"])

    # Wide bins, open at the ends, so every curve has a few hundred shots.
    edges = [-np.inf, -30, -10, 10, 30, np.inf]
    labels = ["< -30", "-30 to -10", "-10 to 10", "10 to 30", "> 30"]
    return pd.DataFrame(
        {
            "xg": shots["xg"].astype(float),
            "is_goal": shots["result"] == "Goal",
            # soccerdata leaves Understat's "Penalty" situation unmapped, so penalties have no situation.
            "is_penalty": shots["situation"].isna(),
            "shooter_d": shooter_d,
            "d_bin": pd.cut(shooter_d, bins=edges, labels=labels),
        },
    )


def summarise_bins(shots: pd.DataFrame) -> pd.DataFrame:
    """Quantiles of xG per bin: if all quantiles move together, the whole distribution shifts.

    Returns:
        One row per bin of shooter_d.

    """
    bins = shots.groupby("d_bin", observed=True)
    summary = pd.DataFrame(
        {
            "shots": bins.size(),
            "mean_xg": bins["xg"].mean(),
            "goals_per_shot": bins["is_goal"].mean(),
        },
    )
    for quantile in [0.25, 0.5, 0.75, 0.9]:
        summary[f"q{round(quantile * 100)}"] = bins["xg"].quantile(quantile)
    big_chance_xg = 0.3
    summary[f"share_xg_above_{big_chance_xg}"] = bins["xg"].apply(lambda xg: (xg > big_chance_xg).mean())
    return summary.reset_index()


def plot_cumulative(shots: pd.DataFrame) -> go.Figure:
    """Plot the cumulative xG distribution per bin of shooter_d, on a log xG axis since most shots are < 0.1.

    Returns:
        One line per bin; a curve to the right means better chances.

    """
    # Diverging: red = weaker shooting team, gray = even, blue = stronger.
    colors = ["#c0392b", "#f0a3a2", "#a3a29c", "#86b6ef", "#184f95"]
    figure = go.Figure()
    for (label, group), color in zip(shots.groupby("d_bin", observed=True), colors, strict=True):
        xg = np.sort(group["xg"].to_numpy())
        share = np.arange(1, len(xg) + 1) / len(xg)
        figure.add_trace(
            go.Scatter(
                x=xg,
                y=share,
                mode="lines",
                line={"color": color, "width": 2},
                name=f"{label} ({len(xg)} shots)",
                hovertemplate="xG ≤ %{x:.3f}: %{y:.0%} of shots<extra>" + str(label) + "</extra>",
            ),
        )
    figure.update_xaxes(type="log", title_text="xG per shot (log scale)")
    figure.update_yaxes(title_text="share of shots with xG ≤ x", tickformat=".0%")
    figure.update_layout(
        title="Cumulative xG per shot by shooting team's points advantage, Premier League 2025/26 (no penalties)",
        legend_title_text="shooter - opponent final points",
        hovermode="x unified",
        template="plotly_white",
    )
    return figure
