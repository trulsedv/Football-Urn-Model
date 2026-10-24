"""Shot chapter (phase 3): how total shots per match depend on skill, and real against simulated data."""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from football_urn_model.data import final_points, load_season
from football_urn_model.simulate import model_settings, simulate_season, starting_red_balls


def main() -> None:
    seasons = 100  # simulated seasons; enough for the simulated statistics to match the theory
    observable = "total_shots"
    output_dir = Path("output")

    schedule, shots = load_season("2025")  # Understat season 2025 = 2025/26
    settings = model_settings()
    real = per_match(schedule, shots, final_points(schedule))
    simulated = simulate_seasons(schedule, settings, seasons)
    ranges = add_terciles(real, simulated)

    # The tempo urn makes the total shots binomial (see the Shot chapter of docs/design.md).
    p, rounds = settings["tempo_urn_red"] / settings["tempo_urn_size"], settings["rounds"]
    sd = np.sqrt(rounds * p * (1 - p))
    theory = {"Mean": rounds * p, "Standard deviation": sd, "Skewness": (1 - 2 * p) / sd}

    tables = panel_tables(real, simulated, observable, ranges, theory)
    print(tables)
    output_dir.mkdir(exist_ok=True)
    (output_dir / "shot_chapter_tables.md").write_text(tables)
    simulation = (
        f"simulated: {seasons} seasons, n = {rounds}, m_t = {settings['tempo_urn_red']}, "
        f"M_t = {settings['tempo_urn_size']} (p = {p:.2f})"
    )
    plot_grid(real, simulated, observable, ranges, simulation).write_html(output_dir / "shot_chapter_grid.html")
    print(f"Wrote {output_dir}/shot_chapter_tables.md and {output_dir}/shot_chapter_grid.html")


def simulate_seasons(schedule: pd.DataFrame, settings: dict[str, int], seasons: int) -> pd.DataFrame:
    """Simulate the real fixture list several times, with red balls from the real final points.

    Returns:
        One row per simulated match, with the simulated final points as the skill proxy.

    """
    rng = np.random.default_rng(1)
    red_balls = starting_red_balls(final_points(schedule), settings)
    simulated = []
    for _ in range(seasons):
        shots, matches = simulate_season(schedule, red_balls, settings, rng)
        simulated.append(per_match(matches, shots, final_points(matches)))
    return pd.concat(simulated, ignore_index=True)


def add_terciles(real: pd.DataFrame, simulated: pd.DataFrame) -> dict[tuple[str, str], str]:
    """Bin the matches into terciles of the real skill proxy; the simulated matches use the same edges.

    Returns:
        The range of the skill proxy in each tercile of the real matches, e.g. "[-65 to -8 pts]".

    """
    for proxy in ["difference", "sum"]:
        low, high = real[proxy].quantile([1 / 3, 2 / 3])
        for matches in [real, simulated]:
            matches[f"{proxy}_bin"] = pd.cut(
                matches[proxy],
                [-np.inf, low, high, np.inf],
                labels=["low", "mid", "high"],
            )
    return {
        (proxy, str(tercile)): f"[{values.min():.0f} to {values.max():.0f} pts]"
        for proxy in ["sum", "difference"]
        for tercile, values in real.groupby(f"{proxy}_bin", observed=True)[proxy]
    }


def per_match(matches: pd.DataFrame, shots: pd.DataFrame, points: pd.Series) -> pd.DataFrame:
    """Put the skill proxy and the total shots side by side, one row per match.

    Returns:
        Skill proxy difference (home - away final points), skill proxy sum, and total shots.

    """
    home_points = points[matches["home_team"]].to_numpy()
    away_points = points[matches["away_team"]].to_numpy()
    return pd.DataFrame(
        {
            "difference": home_points - away_points,
            "sum": home_points + away_points,
            # Matches without a shot have no rows in the shot data, so they get 0.
            "total_shots": shots.groupby("game_id").size().reindex(matches["game_id"], fill_value=0).to_numpy(),
        },
    )


def panel_tables(
    real: pd.DataFrame,
    simulated: pd.DataFrame,
    observable: str,
    ranges: dict[tuple[str, str], str],
    theory: dict[str, float],
) -> str:
    """Write the matches, mean, sd and skewness of each panel of the 3x3 grid as Markdown tables.

    Returns:
        Four tables, rows skill proxy sum (high first) and columns skill proxy difference, each cell "real / sim",
        each with all matches above it (and the theoretical value, where there is one).

    """
    terciles = ["low", "mid", "high"]
    statistics = {"Matches": "count", "Mean": "mean", "Standard deviation": "std", "Skewness": "skew"}
    header = "| Sum \\ difference | " + " | ".join(f"{t} {ranges['difference', t]}" for t in terciles) + " |"
    tables = []
    for title, statistic in statistics.items():
        number = "{:.0f}" if statistic == "count" else "{:.2f}"
        all_matches = [number.format(getattr(data[observable], statistic)()) for data in [real, simulated]]
        if title in theory:
            all_matches.append(f"{theory[title]:.2f}")
        names = " / ".join(["real", "sim", "theory"][: len(all_matches)])
        lines = [f"**{title}** (real / sim)", "", f"All matches ({names}): {' / '.join(all_matches)}", "", header]
        lines.append("| --- | --- | --- | --- |")
        for sum_tercile in reversed(terciles):
            cells = []
            for difference_tercile in terciles:
                values = [
                    data.loc[
                        (data["sum_bin"] == sum_tercile) & (data["difference_bin"] == difference_tercile),
                        observable,
                    ]
                    for data in [real, simulated]
                ]
                cells.append(" / ".join(number.format(getattr(value, statistic)()) for value in values))
            lines.append(f"| {sum_tercile} {ranges['sum', sum_tercile]} | " + " | ".join(cells) + " |")
        tables.append("\n".join(lines))
    return "\n\n".join(tables) + "\n"


def plot_grid(
    real: pd.DataFrame,
    simulated: pd.DataFrame,
    observable: str,
    ranges: dict[tuple[str, str], str],
    simulation: str,
) -> go.Figure:
    """Plot the distribution of an observable per tercile of skill proxy sum (rows) and difference (columns).

    Returns:
        A 3x3 grid; each panel has the real (bars) and the simulated (line) share of matches per value.

    """
    terciles = ["low", "mid", "high"]
    few_matches = 20  # panels with fewer real matches are faded
    colours = {"real": "#2a78d6", "simulated": "#eb6834"}
    titles = []
    for sum_tercile in reversed(terciles):
        for difference_tercile in terciles:
            real_values = real.loc[
                (real["sum_bin"] == sum_tercile) & (real["difference_bin"] == difference_tercile),
                observable,
            ]
            simulated_values = simulated.loc[
                (simulated["sum_bin"] == sum_tercile) & (simulated["difference_bin"] == difference_tercile),
                observable,
            ]
            titles.append(
                f"sum {sum_tercile} {ranges['sum', sum_tercile]}<br>"
                f"difference {difference_tercile} {ranges['difference', difference_tercile]}<br>"
                f"matches: {len(real_values)} real, {len(simulated_values)} sim.<br>"
                f"mean (sd): {real_values.mean():.1f} ({real_values.std():.1f}) real, "
                f"{simulated_values.mean():.1f} ({simulated_values.std():.1f}) sim.",
            )

    figure = make_subplots(
        rows=3,
        cols=3,
        subplot_titles=titles,
        shared_xaxes=True,
        shared_yaxes=True,
        vertical_spacing=0.16,
    )
    for row, sum_tercile in enumerate(reversed(terciles), start=1):
        for col, difference_tercile in enumerate(terciles, start=1):
            for name, data in [("real", real), ("simulated", simulated)]:
                values = data.loc[
                    (data["sum_bin"] == sum_tercile) & (data["difference_bin"] == difference_tercile),
                    observable,
                ]
                is_faded = (
                    (real["sum_bin"] == sum_tercile) & (real["difference_bin"] == difference_tercile)
                ).sum() < few_matches
                shares = values.value_counts(normalize=True).sort_index()
                # Real data as bars; simulated data, with ten times the matches, as a line.
                trace = go.Bar if name == "real" else go.Scatter
                figure.add_trace(
                    trace(
                        x=shares.index,
                        y=shares.to_numpy(),
                        name=name,
                        marker_color=colours[name],
                        opacity=0.3 if is_faded else 1.0,
                        showlegend=row == 1 and col == 1,
                        hovertemplate=f"{name}: %{{x}} shots, share %{{y:.3f}}<extra></extra>",
                    ),
                    row=row,
                    col=col,
                )
    figure.update_layout(
        title=f"Total shots per match, by skill proxy sum (rows) and difference (columns); {simulation}",
        height=1200,
        margin={"t": 200},
    )
    figure.update_annotations(font_size=13)
    figure.update_xaxes(title_text="total shots", row=3)
    figure.update_yaxes(title_text="share of matches", col=1)
    return figure
