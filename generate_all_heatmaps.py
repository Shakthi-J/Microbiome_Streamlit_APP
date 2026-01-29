import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ================= CONFIG =================
TOP_N = 10
OUTPUT_DIR = "heatmaps"

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

def plot_heatmap(df, level, output_png):
    sample_cols = df.columns[1:]

    # Ensure numeric
    df[sample_cols] = df[sample_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    # Select top N taxa
    df["Total"] = df[sample_cols].sum(axis=1)
    df = df.sort_values("Total", ascending=False).head(TOP_N)

    # Convert to relative abundance (%)
    df[sample_cols] = df[sample_cols].div(
        df[sample_cols].sum(axis=0), axis=1
    ) * 100

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
    plt.savefig(output_png, dpi=300)
    plt.close()


def main():
    print("🔥 Generating heatmaps for all taxonomic levels...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for level, file in LEVEL_FILES.items():
        if not os.path.exists(file):
            print(f"⚠️ Skipping {level}: {file} not found")
            continue

        print(f"🔹 Processing {level}...")
        df = pd.read_csv(file)

        output_png = os.path.join(
            OUTPUT_DIR,
            f"heatmap_{level.lower()}_top{TOP_N}.png"
        )

        plot_heatmap(df, level, output_png)
        print(f"✅ Saved {output_png}")

    print("🎉 All heatmaps generated successfully!")


if __name__ == "__main__":
    main()

