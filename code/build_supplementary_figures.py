"""Create supplementary figures used by the v6 appendix.

All inputs are package-local so the revision folder can be moved and rebuilt.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from config import FIGURES, PACKAGE_ROOT


SUPP_FIG_DIR = FIGURES / "supplement"
TABLE_DIR = PACKAGE_ROOT / "data" / "supplement_reordered"
SOURCE_S1 = (
    FIGURES
    / "source"
    / "extended_data_spatial_typology_under5_lri_2023.png"
)


def setup() -> None:
    SUPP_FIG_DIR.mkdir(parents=True, exist_ok=True)


def copy_s1() -> Path:
    output = SUPP_FIG_DIR / "supplementary_figure_s1_spatial_typology_2023.png"
    if not SOURCE_S1.exists():
        raise FileNotFoundError(SOURCE_S1)
    shutil.copy2(SOURCE_S1, output)
    return output


def save_s2() -> Path:
    data = pd.read_csv(TABLE_DIR / "table_s5_annual_observed_excess_typology_counts_and_group_summaries_1990_2023.csv", encoding="utf-8-sig")
    categories = [
        "High observed + high excess",
        "High observed, not high excess",
        "High excess, not high observed",
        "Neither high observed nor high excess",
    ]
    colors = ["#9A3412", "#D97706", "#2563EB", "#D1D5DB"]
    years = data["Year"].to_numpy()
    values = [data[col].to_numpy() for col in categories]

    fig, ax = plt.subplots(figsize=(9.2, 5.2), dpi=300)
    ax.stackplot(years, values, labels=categories, colors=colors, alpha=0.92, linewidth=0)
    ax.set_xlim(years.min(), years.max())
    ax.set_ylim(0, data["Locations"].max())
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of locations")
    ax.set_title("Annual observed/excess typology counts, 1990-2023", fontweight="bold")
    ax.grid(axis="y", color="#E5E7EB", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False)
    fig.tight_layout()
    output = SUPP_FIG_DIR / "supplementary_figure_s2_annual_typology_counts.png"
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output


def save_s3() -> Path:
    data = pd.read_csv(TABLE_DIR / "table_s18_granular_cross_age_overlap_of_high_observed_high_excess_membership.csv", encoding="utf-8-sig")
    preferred_order = ["u5", "5_14", "15_49", "50_69", "5_69", "70p", "total"]
    pivot = data.pivot(index="age_group_a", columns="age_group_b", values="jaccard").reindex(index=preferred_order, columns=preferred_order)
    labels = ["Under 5", "5-14", "15-49", "50-69", "5-69", "70+", "All ages"]

    fig, ax = plt.subplots(figsize=(6.6, 5.8), dpi=300)
    matrix = pivot.to_numpy(dtype=float)
    im = ax.imshow(matrix, cmap="YlGnBu", vmin=0, vmax=1)
    ax.set_xticks(np.arange(len(labels)), labels=labels, rotation=45, ha="right")
    ax.set_yticks(np.arange(len(labels)), labels=labels)
    ax.set_title("Cross-age overlap of high-observed/high-excess membership", fontweight="bold")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            val = matrix[i, j]
            if np.isfinite(val):
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=8, color="#111827")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Jaccard overlap")
    ax.spines[:].set_visible(False)
    fig.tight_layout()
    output = SUPP_FIG_DIR / "supplementary_figure_s3_age_overlap_heatmap.png"
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output


def main() -> None:
    setup()
    for path in [copy_s1(), save_s2(), save_s3()]:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
