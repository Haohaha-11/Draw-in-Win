"""Visualize the evolution of the 17 bundled SDG scores.

The script reads ``data/Score.csv`` by default and exports a publication-ready
heatmap plus an aggregate trend panel as PNG, SVG, and PDF.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = SCRIPT_DIR / "data" / "Score.csv"


def load_scores(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Load years and the 17 normalized SDG score columns from a CSV file."""

    frame = pd.read_csv(path, encoding="utf-8-sig")
    if frame.shape[1] != 18:
        raise ValueError(
            f"Expected one year column plus 17 SDG columns, found {frame.shape[1]} columns."
        )

    years = frame.iloc[:, 0].astype(str).str.extract(r"(\d{4})", expand=False)
    if years.isna().any():
        raise ValueError("Every row in the first column must contain a four-digit year.")

    scores = frame.iloc[:, 1:].apply(pd.to_numeric, errors="raise").to_numpy(dtype=float)
    return years.astype(int).to_numpy(), scores


def build_figure(years: np.ndarray, scores: np.ndarray) -> plt.Figure:
    """Create the heatmap and aggregate trend figure."""

    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "axes.unicode_minus": False,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )

    palette = LinearSegmentedColormap.from_list(
        "sdg_scores",
        ["#F5F0E8", "#D9E8D5", "#85B8A6", "#397F85", "#20445B"],
    )
    figure = plt.figure(figsize=(12.0, 7.1), constrained_layout=True)
    grid = figure.add_gridspec(2, 1, height_ratios=[3.25, 1.35])
    heatmap_axis = figure.add_subplot(grid[0])
    trend_axis = figure.add_subplot(grid[1])

    image = heatmap_axis.imshow(
        scores,
        aspect="auto",
        interpolation="nearest",
        cmap=palette,
        vmin=0,
        vmax=100,
    )
    heatmap_axis.set_title(
        "SDG Score Evolution, 2015–2024",
        fontsize=18,
        fontweight="bold",
        pad=16,
        loc="left",
    )
    heatmap_axis.set_xlabel("Sustainable Development Goal", fontsize=12, fontweight="bold")
    heatmap_axis.set_ylabel("Year", fontsize=12, fontweight="bold")
    heatmap_axis.set_xticks(np.arange(17), [f"SDG {number}" for number in range(1, 18)])
    heatmap_axis.set_yticks(np.arange(len(years)), years)
    heatmap_axis.tick_params(axis="x", labelrotation=45, labelsize=9)
    heatmap_axis.tick_params(axis="y", labelsize=10)

    heatmap_axis.set_xticks(np.arange(-0.5, 17, 1), minor=True)
    heatmap_axis.set_yticks(np.arange(-0.5, len(years), 1), minor=True)
    heatmap_axis.grid(which="minor", color="white", linewidth=0.7, alpha=0.72)
    heatmap_axis.tick_params(which="minor", bottom=False, left=False)
    for spine in heatmap_axis.spines.values():
        spine.set_color("#69747B")
        spine.set_linewidth(0.8)

    colorbar = figure.colorbar(image, ax=heatmap_axis, pad=0.018, shrink=0.96)
    colorbar.set_label("Normalized score (0–100)", fontsize=10)
    colorbar.ax.tick_params(labelsize=9)

    mean_scores = scores.mean(axis=1)
    lower_quartile = np.quantile(scores, 0.25, axis=1)
    upper_quartile = np.quantile(scores, 0.75, axis=1)

    trend_axis.fill_between(
        years,
        lower_quartile,
        upper_quartile,
        color="#85B8A6",
        alpha=0.30,
        linewidth=0,
        label="Interquartile range",
    )
    trend_axis.plot(
        years,
        mean_scores,
        color="#20445B",
        linewidth=2.4,
        marker="o",
        markersize=5.5,
        markerfacecolor="white",
        markeredgewidth=1.4,
        label="Mean across 17 SDGs",
    )
    trend_axis.set_xlabel("Year", fontsize=11, fontweight="bold")
    trend_axis.set_ylabel("Score", fontsize=11, fontweight="bold")
    trend_axis.set_xticks(years)
    trend_axis.set_xlim(years.min() - 0.2, years.max() + 0.2)
    trend_axis.grid(axis="y", color="#CAD1D3", linestyle="--", linewidth=0.8, alpha=0.8)
    trend_axis.spines[["top", "right"]].set_visible(False)
    trend_axis.legend(loc="upper left", frameon=False, ncol=2, fontsize=9.5)

    latest_index = int(np.argmax(years))
    trend_axis.annotate(
        f"{mean_scores[latest_index]:.1f}",
        xy=(years[latest_index], mean_scores[latest_index]),
        xytext=(-4, 11),
        textcoords="offset points",
        ha="right",
        color="#20445B",
        fontsize=9.5,
        fontweight="bold",
    )

    return figure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Score CSV containing one year column and 17 SDG score columns.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=SCRIPT_DIR,
        help="Directory for PNG, SVG, and PDF outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    years, scores = load_scores(args.input)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    figure = build_figure(years, scores)
    base = args.output_dir / "sdg_score_evolution"
    figure.savefig(base.with_suffix(".png"), dpi=300)
    figure.savefig(base.with_suffix(".svg"))
    figure.savefig(base.with_suffix(".pdf"))
    plt.close(figure)

    print(f"Saved: {base.with_suffix('.png')}")
    print(f"Saved: {base.with_suffix('.svg')}")
    print(f"Saved: {base.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
