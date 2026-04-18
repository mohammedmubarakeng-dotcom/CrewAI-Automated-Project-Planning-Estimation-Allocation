from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from src.models import ProjectPlan


_MILESTONE_COLORS = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52",
    "#8172B3", "#937860", "#DA8BC3", "#8C8C8C",
]


def generate_gantt_chart(plan: ProjectPlan, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    task_names = [t.task_name for t in plan.tasks]
    durations = [t.estimated_time_hours for t in plan.tasks]

    milestone_map: dict[str, str] = {}
    for m in plan.milestones:
        for task_name in m.tasks:
            milestone_map[task_name] = m.milestone_name

    unique_milestones = list(dict.fromkeys(
        milestone_map.get(t, "Unassigned") for t in task_names
    ))
    color_map = {
        ms: _MILESTONE_COLORS[i % len(_MILESTONE_COLORS)]
        for i, ms in enumerate(unique_milestones)
    }

    starts: list[float] = []
    current = 0.0
    for d in durations:
        starts.append(current)
        current += d

    fig_height = max(4, len(task_names) * 0.55 + 2)
    fig, ax = plt.subplots(figsize=(14, fig_height))

    y_positions = range(len(task_names) - 1, -1, -1)
    for y, task_name, start, duration in zip(
        y_positions, task_names, starts, durations
    ):
        milestone = milestone_map.get(task_name, "Unassigned")
        color = color_map[milestone]
        ax.barh(
            y,
            duration,
            left=start,
            height=0.5,
            color=color,
            edgecolor="white",
            linewidth=0.8,
        )
        ax.text(
            start + duration / 2,
            y,
            f"{duration:.1f}h",
            ha="center",
            va="center",
            fontsize=7,
            color="white",
            fontweight="bold",
        )

    ax.set_yticks(list(y_positions))
    ax.set_yticklabels(task_names, fontsize=9)
    ax.set_xlabel("Cumulative Hours", fontsize=10)
    ax.set_title("Project Gantt Chart — Task Schedule", fontsize=13, fontweight="bold", pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    legend_patches = [
        mpatches.Patch(color=color_map[ms], label=ms) for ms in unique_milestones
    ]
    ax.legend(
        handles=legend_patches,
        title="Milestones",
        loc="lower right",
        fontsize=8,
        title_fontsize=9,
        framealpha=0.9,
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return output_path
