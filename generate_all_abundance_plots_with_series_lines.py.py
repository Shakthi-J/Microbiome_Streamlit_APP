import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ================= CONFIG =================
TOP_N = 10
OUTPUT_DIR = "abundance_plots_with_lines"

LEVEL_FILES = {
    "Domain": "domain_table.csv",
    "Phylum": "phylum_table.csv",
    "Class": "class_table.csv",
    "Order": "order_table.csv",
    "Family": "family_table.csv",
    "Genus": "genus_table.csv",
    "Species": "species_table.csv"
}
# =========================================

# High-quality color palette
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

def plot_stacked_bar_with_lines(df, level, output_png):
    sample_cols = df.columns[1:]

    # Ensure numeric
    df[sample_cols] = df[sample_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    # Compute totals
    df["Total"] = df[sample_cols].sum(axis=1)
    df = df.sort_values("Total", ascending=False)

    # Top N taxa
    df_top = df.head(TOP_N)

    # Others
    others_sum = df.iloc[TOP_N:][sample_cols].sum()
    others_row = pd.DataFrame(
        [["Others"] + others_sum.tolist() + [others_sum.sum()]],
        columns=df.columns
    )

    df_plot = pd.concat([df_top, others_row], ignore_index=True)

    # Convert to relative abundance (%)
    df_plot[sample_cols] = (
        df_plot[sample_cols]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
    )

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
    x_pos = np.arange(len(sample_cols))
    bottom = np.zeros(len(sample_cols), dtype=float)

    y_positions = {}

    for i, row in df_plot.iterrows():
        values = row[sample_cols].astype(float).values

        ax.bar(
            x_pos,
            values,
            bottom=bottom,
            label=row["Legend"],
            color=COLORS_20[i % len(COLORS_20)],
            edgecolor="white",
            linewidth=0.5,
            width=0.8
        )

        # Midpoints for connecting lines
        y_positions[row[level]] = bottom + values / 2
        bottom += values

    # Draw connecting lines
    for y_vals in y_positions.values():
        ax.plot(
            x_pos,
            y_vals,
            color="black",
            linestyle="-",
            linewidth=1,
            marker="o",
            markersize=4,
            alpha=0.7
        )

    # Formatting
    ax.set_title(f"Top {TOP_N} {level}", fontsize=16, weight="bold", pad=20)
    ax.set_ylabel("Relative Abundance (%)", fontsize=12)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(sample_cols, rotation=45, ha="right")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    ax.legend(
        loc="upper left",
        bbox_to_anchor=(1, 1),
        title=f"{level} (Total %)",
        fontsize=9
    )

    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    plt.close()



def main():
    print("📊 Generating abundance plots (with series lines) for all taxonomic levels...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for level, file in LEVEL_FILES.items():
        if not os.path.exists(file):
            print(f"⚠️ Skipping {level}: {file} not found")
            continue

        print(f"🔹 Processing {level}...")
        df = pd.read_csv(file)

        output_png = os.path.join(
            OUTPUT_DIR,
            f"top10_{level.lower()}_with_lines.png"
        )

        plot_stacked_bar_with_lines(df, level, output_png)
        print(f"✅ Saved {output_png}")

    print("🎉 All plots generated successfully!")


if __name__ == "__main__":
    main()

