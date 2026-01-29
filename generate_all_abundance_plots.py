import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

# ================= CONFIG =================
TOP_N = 10
OUTPUT_DIR = Path("abundance_plots")

LEVEL_FILES = {
    "Domain": Path("tables/domain_table.csv"),
    "Phylum": Path("tables/phylum_table.csv"),
    "Class": Path("tables/class_table.csv"),
    "Order": Path("tables/order_table.csv"),
    "Family": Path("tables/family_table.csv"),
    "Genus": Path("tables/genus_table.csv"),
    "Species": Path("tables/species_table.csv")
}
# =========================================

# Publication-quality color palette
COLORS_20 = [
    (0.121, 0.466, 0.705, 1.0),
    (1.000, 0.498, 0.054, 1.0),
    (0.172, 0.627, 0.172, 1.0),
    (0.839, 0.153, 0.157, 1.0),
    (0.580, 0.403, 0.741, 1.0),
    (0.549, 0.337, 0.294, 1.0),
    (0.890, 0.466, 0.760, 1.0),
    (0.737, 0.741, 0.133, 1.0),
    (0.090, 0.745, 0.811, 1.0),
    (0.682, 0.780, 0.909, 1.0),
    (0.498, 0.498, 0.498, 1.0)  # Others
]

# =========================================

def plot_top10_stacked(df, level):
    sample_cols = df.columns[1:]

    # Compute totals
    df["Total"] = df[sample_cols].sum(axis=1)
    df = df.sort_values("Total", ascending=False)

    # Top N
    df_top = df.head(TOP_N)

    # Others
    others_sum = df.iloc[TOP_N:][sample_cols].sum()
    others_row = pd.DataFrame(
        [["Others"] + others_sum.tolist() + [others_sum.sum()]],
        columns=df.columns
    )

    df_plot = pd.concat([df_top, others_row], ignore_index=True)

    # Convert to relative abundance
    df_plot[sample_cols] = (
        df_plot[sample_cols]
        .div(df_plot[sample_cols].sum(axis=0), axis=1)
        * 100
    )

    # Legend labels
    total_sum = df_plot["Total"].sum()
    df_plot["Legend"] = df_plot.apply(
        lambda r: f"{r[level]} ({r['Total'] / total_sum * 100:.1f}%)",
        axis=1
    )

    # Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    bottom = np.zeros(len(sample_cols))

    for i, row in df_plot.iterrows():
        ax.bar(
            sample_cols,
            row[sample_cols],
            bottom=bottom,
            label=row["Legend"],
            color=COLORS_20[i % len(COLORS_20)],
            edgecolor="white",
            linewidth=0.5
        )
        bottom += row[sample_cols]

    ax.set_title(f"Top {TOP_N} {level}", fontsize=16, weight="bold", pad=20)
    ax.set_ylabel("Relative Abundance (%)", fontsize=12)
    ax.set_ylim(0, 100)

    ax.legend(
        loc="upper left",
        bbox_to_anchor=(1, 1),
        title=f"{level} (Total %)",
        fontsize=9
    )

    plt.tight_layout()
    return fig


def main():
    """
    Generates stacked bar plots for the top 10 taxa
    across all taxonomic levels.
    """

    OUTPUT_DIR.mkdir(exist_ok=True)

    for level, file_path in LEVEL_FILES.items():
        if not file_path.exists():
            continue

        df = pd.read_csv(file_path)
        fig = plot_top10_stacked(df, level)

        output_path = OUTPUT_DIR / f"top10_{level.lower()}.png"
        fig.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close(fig)


if __name__ == "__main__":
    main()
