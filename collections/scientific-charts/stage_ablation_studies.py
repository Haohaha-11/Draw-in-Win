"""Reproduce the stage-necessity and adaptive-stage ablation small multiples.

All values are deterministic visual estimates from the supplied raster.  They
are intended to reproduce the visual design, not to recover source measurements.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


GOLD = "#D39A3D"
GREEN = "#4F8A63"
NAVY = "#455B83"
PALE_GOLD = "#F5DDA9"
GRID = "#D9DEE5"
METRICS = ("POPE", "GQA", "TextVQA", "MME")


NECESSITY_STAR = {
    "POPE": [87.8, 87.2, 86.5],
    "GQA": [61.0, 59.2, 57.3],
    "TextVQA": [57.0, 56.1, 54.8],
    "MME": [1440, 1418, 1385],
}
NECESSITY_PROGRESSIVE = {
    "POPE": [87.4, 86.0, 84.0],
    "GQA": [60.2, 58.0, 55.7],
    "TextVQA": [56.9, 55.9, 54.6],
    "MME": [1422, 1392, 1360],
}
NECESSITY_ADAPTIVE = {
    "POPE": [57, 14, 24],
    "GQA": [51, 42, 40],
    "TextVQA": [51, 45, 43],
    "MME": [1060, 730, 700],
}
NECESSITY_LIMITS = {
    "POPE": ((82.0, 89.0), (0, 62)),
    "GQA": ((54.5, 62.0), (38, 53)),
    "TextVQA": ((53.5, 57.5), (42, 52)),
    "MME": ((1340, 1455), (650, 1100)),
}


ALPHA_VALUES = np.array([1.5, 2.0, 2.5, 3.0, 4.0])
ALPHA_SERIES = {
    "POPE": ([87.0, 88.0, 84.0, 83.0, 73.0],
             [86.0, 87.0, 82.0, 82.0, 72.0],
             [85.0, 86.0, 78.0, 78.0, 65.0]),
    "GQA": ([60.0, 60.5, 58.5, 57.0, 54.5],
            [58.5, 58.2, 57.0, 56.0, 53.5],
            [56.8, 57.2, 52.5, 52.5, 50.0]),
    "TextVQA": ([57.6, 57.5, 57.0, 57.2, 54.6],
                [56.8, 56.6, 56.0, 55.5, 52.5],
                [55.0, 54.8, 53.0, 53.2, 50.4]),
    "MME": ([1430, 1420, 1360, 1375, 1330],
            [1400, 1400, 1340, 1360, 1290],
            [1350, 1380, 1310, 1290, 1180]),
}
ALPHA_LIMITS = {
    "POPE": (64, 90),
    "GQA": (49, 62),
    "TextVQA": (50, 58.3),
    "MME": (1160, 1450),
}


def paper_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif", "STIXGeneral"],
            "mathtext.fontset": "stix",
            "font.size": 10,
            "axes.titlesize": 12.5,
            "axes.titleweight": "bold",
            "axes.linewidth": 0.9,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def quiet_axes(ax: plt.Axes) -> None:
    ax.grid(axis="y", color=GRID, linewidth=0.65, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#A8AFB7")
    ax.spines["bottom"].set_color("#A8AFB7")
    ax.tick_params(labelsize=8.5, colors="#59616B", pad=2)


def create_figure() -> plt.Figure:
    paper_style()
    fig = plt.figure(figsize=(12.6, 7.7), dpi=180)
    outer = fig.add_gridspec(
        2,
        1,
        height_ratios=[1.12, 1.0],
        hspace=0.48,
        left=0.075,
        right=0.985,
        top=0.895,
        bottom=0.105,
    )
    top = outer[0].subgridspec(2, 4, hspace=0.12, wspace=0.28)
    bottom = outer[1].subgridspec(1, 4, wspace=0.28)

    budgets = np.array([128, 64, 32])
    for col, metric in enumerate(METRICS):
        upper = fig.add_subplot(top[0, col])
        lower = fig.add_subplot(top[1, col])
        upper.plot(
            budgets,
            NECESSITY_STAR[metric],
            color=GOLD,
            lw=2.0,
            marker="o",
            markersize=5,
            markerfacecolor="white",
            markeredgewidth=1.4,
            zorder=3,
        )
        upper.plot(
            budgets,
            NECESSITY_PROGRESSIVE[metric],
            color=NAVY,
            lw=2.0,
            ls="--",
            marker="s",
            markersize=5,
            markerfacecolor="white",
            markeredgewidth=1.4,
            zorder=3,
        )
        lower.plot(
            budgets,
            NECESSITY_ADAPTIVE[metric],
            color=GREEN,
            lw=2.2,
            marker="^",
            markersize=6,
            markerfacecolor="white",
            markeredgewidth=1.4,
            zorder=3,
        )
        upper.set_title(metric, pad=5)
        upper.set_ylim(*NECESSITY_LIMITS[metric][0])
        lower.set_ylim(*NECESSITY_LIMITS[metric][1])
        upper.set_xlim(134, 26)
        lower.set_xlim(134, 26)
        upper.set_xticks([])
        lower.set_xticks(budgets, ["128", "64", "32"])
        quiet_axes(upper)
        quiet_axes(lower)

    necessity_handles = [
        Line2D([], [], color=GOLD, lw=2, marker="o", markersize=5,
               markerfacecolor="white", label="STAR-Pro"),
        Line2D([], [], color=GREEN, lw=2, marker="^", markersize=6,
               markerfacecolor="white", label="w/o Adaptive"),
        Line2D([], [], color=NAVY, lw=2, ls="--", marker="s", markersize=5,
               markerfacecolor="white", label="w/o Progressive"),
    ]
    fig.text(0.04, 0.935, "(a) Stage Necessity", fontsize=12.5,
             fontweight="bold", ha="left", va="center")
    fig.legend(
        handles=necessity_handles,
        loc="upper center",
        bbox_to_anchor=(0.64, 0.947),
        ncol=3,
        frameon=False,
        fontsize=10,
        handlelength=1.7,
        columnspacing=1.25,
        handletextpad=0.45,
    )
    fig.text(0.025, 0.73, "Score", rotation=90, ha="center", va="center",
             fontsize=11.5)
    fig.text(0.53, 0.515, r"retained-token budget  $T$", ha="center",
             va="center", fontsize=11.5)

    for col, metric in enumerate(METRICS):
        ax = fig.add_subplot(bottom[0, col])
        ax.axvspan(1.86, 2.14, color=PALE_GOLD, alpha=0.45, linewidth=0, zorder=0)
        t128, t64, t32 = ALPHA_SERIES[metric]
        ax.plot(ALPHA_VALUES, t128, color=GOLD, lw=2.4, marker="o",
                markersize=5, label=r"$T=128$", zorder=3)
        ax.plot(ALPHA_VALUES, t64, color=NAVY, lw=2.2, marker="s",
                markersize=5, markerfacecolor="white", label=r"$T=64$", zorder=3)
        ax.plot(ALPHA_VALUES, t32, color=GREEN, lw=2.2, marker="^",
                markersize=6, markerfacecolor="white", label=r"$T=32$", zorder=3)
        ax.set_title(metric, pad=5)
        ax.set_xlim(1.38, 4.12)
        ax.set_ylim(*ALPHA_LIMITS[metric])
        ax.set_xticks(ALPHA_VALUES, ["1.5", "2", "2.5", "3", "4"])
        quiet_axes(ax)

    alpha_handles = [
        PatchProxy(PALE_GOLD, r"STAR-Pro: $\alpha=2$"),
        Line2D([], [], color=GOLD, lw=2.4, marker="o", markersize=5,
               label=r"$T=128$"),
        Line2D([], [], color=NAVY, lw=2.2, marker="s", markersize=5,
               markerfacecolor="white", label=r"$T=64$"),
        Line2D([], [], color=GREEN, lw=2.2, marker="^", markersize=6,
               markerfacecolor="white", label=r"$T=32$"),
    ]
    fig.text(0.04, 0.455, r"(b) Adaptive Stage: $\alpha$", fontsize=12.5,
             fontweight="bold", ha="left", va="center")
    fig.legend(
        handles=alpha_handles,
        loc="upper center",
        bbox_to_anchor=(0.66, 0.469),
        ncol=4,
        frameon=False,
        fontsize=9.5,
        handlelength=1.7,
        columnspacing=1.05,
        handletextpad=0.45,
    )
    fig.text(0.025, 0.285, "Score", rotation=90, ha="center", va="center",
             fontsize=11.5)
    fig.text(0.53, 0.035, r"$\alpha$", ha="center", va="center", fontsize=13)
    return fig


def PatchProxy(color: str, label: str) -> Line2D:
    """Create a legend-only thick translucent segment for the alpha band."""
    return Line2D([], [], color=color, alpha=0.65, lw=8, label=label)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parent)
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    fig = create_figure()
    stem = "stage_ablation_studies"
    fig.savefig(args.output_dir / f"{stem}.png", dpi=args.dpi)
    fig.savefig(args.output_dir / f"{stem}.svg")
    fig.savefig(args.output_dir / f"{stem}.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
