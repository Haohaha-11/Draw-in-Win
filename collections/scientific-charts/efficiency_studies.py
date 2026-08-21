"""Reproduce the two-row efficiency-study bar-chart matrix.

The source is a raster reference rather than a data table.  Values below were
transcribed where readable and visually estimated otherwise; replace them with
the original benchmark results before quantitative use.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator


@dataclass(frozen=True)
class Metric:
    title: str
    baseline: float
    groups: tuple[tuple[float, float, float, float], ...]
    ylim: tuple[float, float]
    decimals: int = 1


METHODS = ("FastV", "CDPruner", "VScan", "STAR-Pro (Ours)")
FACES = ("#F2AAA0", "#CDD9EC", "#D8EBDD", "#F8DEAA")
EDGES = ("#C64F3D", "#4A628A", "#518263", "#C58B2A")
BASE_FACE = "#F4F3EE"
BASE_EDGE = "#6B7076"
GRID = "#D9DEE5"


NEXT_METRICS = (
    Metric("Latency (ms) ↓", 285.7, ((86.4, 100.7, 94.5, 184.0), (77.2, 86.1, 80.3, 125.7)), (0, 330)),
    Metric("Compute (TFLOPs) ↓", 41.0, ((7.2, 7.2, 5.7, 3.8), (5.2, 5.1, 4.3, 3.3)), (0, 45)),
    Metric("Peak GPU Memory (GB) ↓", 15.4, ((15.6, 14.0, 17.3, 14.0), (15.6, 14.0, 15.5, 14.0)), (0, 21)),
    Metric("Speedup (×) ↑", 1.00, ((3.31, 2.84, 3.02, 1.55), (3.70, 3.32, 3.56, 2.27)), (0, 4.25), 2),
    Metric("Performance (Rel. %) ↑", 100.0, ((80.4, 98.5, 96.2, 99.2), (56.8, 96.6, 90.3, 97.0)), (50, 105)),
)


VIDEO_METRICS = (
    Metric("Latency (ms) ↓", 1799.2, ((976.0, 878.3, 1074.6, 925.4), (896.2, 776.6, 908.5, 802.8)), (0, 2050)),
    Metric("Compute (TFLOPs) ↓", 197.1, ((73.7, 73.1, 88.6, 71.3), (59.3, 58.6, 66.3, 57.9)), (0, 220)),
    Metric("Peak GPU Memory (GB) ↓", 25.6, ((41.4, 48.6, 20.2, 22.6), (41.4, 48.6, 20.2, 22.6)), (0, 55)),
    Metric("Speedup (×) ↑", 1.00, ((1.84, 2.05, 1.70, 1.94), (2.01, 2.32, 2.01, 2.24)), (0, 2.7), 2),
    Metric("Performance (Rel. %) ↑", 100.0, ((87.7, 94.6, 95.2, 96.7), (78.5, 88.8, 90.0, 92.7)), (50, 105)),
)


def paper_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif", "STIXGeneral"],
            "mathtext.fontset": "stix",
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.linewidth": 0.9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 8,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def value_text(value: float, decimals: int) -> str:
    if decimals == 2:
        return f"{value:.2f}"
    return f"{value:.1f}"


def draw_panel(
    ax: plt.Axes,
    metric: Metric,
    group_labels: tuple[str, str, str],
    row_label: str | None,
) -> None:
    width = 0.155
    offsets = np.array([-1.5, -0.5, 0.5, 1.5]) * width

    baseline_bar = ax.bar(
        [0],
        [metric.baseline],
        width=0.24,
        color=BASE_FACE,
        edgecolor=BASE_EDGE,
        linewidth=1.4,
        zorder=3,
    )[0]
    for group_index, values in enumerate(metric.groups, start=1):
        for method_index, value in enumerate(values):
            ax.bar(
                group_index + offsets[method_index],
                value,
                width=width,
                color=FACES[method_index],
                edgecolor=EDGES[method_index],
                linewidth=1.25,
                zorder=3,
            )
            ax.annotate(
                value_text(value, metric.decimals),
                xy=(group_index + offsets[method_index], value),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                rotation=90,
                fontsize=7.2,
                color=EDGES[method_index],
                fontweight="bold" if method_index == 3 else "normal",
                clip_on=False,
                zorder=5,
            )

    ax.annotate(
        value_text(metric.baseline, metric.decimals),
        xy=(baseline_bar.get_x() + baseline_bar.get_width() / 2, metric.baseline),
        xytext=(0, 3),
        textcoords="offset points",
        ha="center",
        va="bottom",
        rotation=90,
        fontsize=7.2,
        color=BASE_EDGE,
        clip_on=False,
    )

    ax.set_title(metric.title, pad=8)
    ax.set_xlim(-0.35, 2.45)
    ax.set_ylim(*metric.ylim)
    ax.set_xticks([0, 1, 2], group_labels)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.grid(axis="y", color=GRID, linewidth=0.75, alpha=0.9)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#A8AFB7")
    ax.spines["bottom"].set_color("#A8AFB7")
    ax.tick_params(colors="#5E6670", pad=2)

    if row_label:
        ax.text(
            -0.24,
            0.50,
            row_label,
            transform=ax.transAxes,
            rotation=90,
            ha="center",
            va="center",
            fontsize=13,
            fontweight="bold",
            color="#3F454C",
        )


def create_figure() -> plt.Figure:
    paper_style()
    fig, axes = plt.subplots(2, 5, figsize=(15.8, 6.9), dpi=170)
    fig.subplots_adjust(left=0.068, right=0.992, top=0.945, bottom=0.225,
                        wspace=0.13, hspace=0.47)

    next_labels = ("Baseline\n2,880", "320", "160")
    video_labels = ("Baseline\n10,816", "2,048", "1,024")
    for col, metric in enumerate(NEXT_METRICS):
        draw_panel(axes[0, col], metric, next_labels,
                   "LLaVA-NeXT-7B" if col == 0 else None)
    for col, metric in enumerate(VIDEO_METRICS):
        draw_panel(axes[1, col], metric, video_labels,
                   "LLaVA-Video-7B" if col == 0 else None)

    legend_handles = [
        Patch(facecolor=BASE_FACE, edgecolor=BASE_EDGE, linewidth=1.4, label="Baseline"),
        *[
            Patch(facecolor=face, edgecolor=edge, linewidth=1.4, label=method)
            for face, edge, method in zip(FACES, EDGES, METHODS)
        ],
    ]
    legend = fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.135),
        ncol=5,
        frameon=False,
        fontsize=11,
        handlelength=1.5,
        columnspacing=1.25,
    )
    legend.get_texts()[-1].set_color(EDGES[-1])
    legend.get_texts()[-1].set_fontweight("bold")

    fig.text(
        0.5,
        0.045,
        "Efficiency Studies — latency, compute, peak GPU memory, speedup, and relative performance",
        ha="center",
        va="center",
        fontsize=13.5,
        fontweight="bold",
    )
    fig.text(
        0.5,
        0.018,
        "LLaVA-NeXT-7B uses retained-token budgets; LLaVA-Video-7B uses tokens per frame over 64 frames.",
        ha="center",
        va="center",
        fontsize=10.5,
        color="#555B62",
    )
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parent)
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    fig = create_figure()
    stem = "efficiency_studies"
    fig.savefig(args.output_dir / f"{stem}.png", dpi=args.dpi)
    fig.savefig(args.output_dir / f"{stem}.svg")
    fig.savefig(args.output_dir / f"{stem}.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
