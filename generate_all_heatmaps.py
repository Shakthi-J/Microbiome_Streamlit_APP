import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ================= CONFIG =================
TOP_N = 10
OUTPUT_DIR = Path("heatmaps")

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

def plot_heatmap(df, level, output_png):
    sample_cols = df.columns[1:]

    # Ensure numeric
    df[sample_cols] = df[sample_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    # Select top N taxa
    df["Total"] = df[sample_cols].sum(axis=1)
    df = df.sort_values("Total", ascending=False).head(TOP_N)

    # Convert to relative abundance (%)
    df[sample_cols] = (
        df[sample_cols]
        .div(df[sample_cols].sum(axis=0), axis=1)
        * 100
    )

    # Prepare matrix
    heatmap_df = df.set_index(level)[sample_cols]

    # Plot
    plt.figure(figsize=(10, max(6, TOP_N * 0.6)))
    sns.heatmap(
        heatmap_df,
        cmap="viridis",
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "Relative Abundance (%)"}
    )

    plt.title(f"Top {TOP_N} {level} – Relative Abundance", fontsize=14, weight="bold")
    plt.xlabel("Samples")
    plt.ylabel(level)
    plt.tight_layout()
    plt.savefig(output_png, dpi=300, bbox_inches="tight")
    plt.close()


def main():
    """
    Generates heatmaps for the top 10 taxa
    across all taxonomic levels.
    """

    OUTPUT_DIR.mkdir(exist_ok=True)

    for level, file_path in LEVEL_FILES.items():
        if not file_path.exists():
            continue

        df = pd.read_csv(file_path)

        output_png = OUTPUT_DIR / f"heatmap_{level.lower()}_top{TOP_N}.png"
        plot_heatmap(df, level, output_png)


if __name__ == "__main__":
    main()
