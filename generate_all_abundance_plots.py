import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ================= CONFIG =================
TOP_N = 10
OUTPUT_DIR = "abundance_plots"

LEVEL_FILES = {
    "Domain": "tables/domain_table.csv",
    "Phylum": "tables/phylum_table.csv",
    "Class": "tables/class_table.csv",
    "Order": "tables/order_table.csv",
    "Family": "tables/family_table.csv",
    "Genus": "tables/genus_table.csv",
    "Species": "tables/species_table.csv"
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
    (0.498, 0.498, 0.498, 1.0)  # Others (gray)
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
    df_plot[sample_cols] = df_plot[sample_cols].div(
        df_plot[sample_cols].sum(axis=0), axis=1
    ) * 100

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
    print("📊 Generating abundance plots for all taxonomic levels...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for level, file in LEVEL_FILES.items():
        if not os.path.exists(file):
            print(f"⚠️ Skipping {level}: {file} not found")
            continue

        print(f"🔹 Processing {level}...")
        df = pd.read_csv(file)

        fig = plot_top10_stacked(df, level)

        output_path = os.path.join(OUTPUT_DIR, f"top10_{level.lower()}.png")
        fig.savefig(output_path, dpi=300)
        plt.close(fig)

        print(f"✅ Saved {output_path}")

    print("🎉 All abundance plots generated successfully!")


if __name__ == "__main__":
    main()

