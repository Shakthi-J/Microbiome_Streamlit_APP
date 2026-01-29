import pandas as pd
from pathlib import Path

# ================= CONFIG =================
INPUT_FILE = Path("input_taxonomy.txt")
OUTPUT_CLEANED = "cleaned_taxonomy.csv"

TAX_LEVELS = ["Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species"]

PREFIX_MAP = {
    "d__": "Domain",
    "p__": "Phylum",
    "c__": "Class",
    "o__": "Order",
    "f__": "Family",
    "g__": "Genus",
    "s__": "Species"
}
# =========================================


def clean_name(name):
    if name is None:
        return None
    name = name.strip()
    if "uncultured" in name.lower():
        return None
    return name


def parse_taxonomy(taxon_string):
    taxonomy = {level: None for level in TAX_LEVELS}
    parts = taxon_string.split("; ")

    for part in parts:
        part = part.strip()
        for prefix, level in PREFIX_MAP.items():
            if part.startswith(prefix):
                value = part.replace(prefix, "").strip()
                taxonomy[level] = clean_name(value)

    return taxonomy


def fill_unidentified(taxonomy):
    unidentified_used = False

    for i, level in enumerate(TAX_LEVELS):
        if taxonomy[level] is None:
            parent = taxonomy[TAX_LEVELS[i - 1]] if i > 0 else None
            if parent and not unidentified_used:
                taxonomy[level] = f"unidentified ({parent})"
                unidentified_used = True
            else:
                taxonomy[level] = parent

    return taxonomy


def clean_taxonomy_table(df):
    cleaned_rows = []

    for _, row in df.iterrows():
        taxon_info = parse_taxonomy(row["Taxon"])
        taxon_info = fill_unidentified(taxon_info)

        new_row = taxon_info.copy()
        for col in df.columns[1:]:
            new_row[col] = row[col]

        cleaned_rows.append(new_row)

    return pd.DataFrame(cleaned_rows)


def create_level_tables(df):
    sample_cols = [c for c in df.columns if c not in TAX_LEVELS]

    for level in TAX_LEVELS:
        level_df = (
            df.groupby(level)[sample_cols]
            .sum()
            .reset_index()
        )

        output_file = f"{level.lower()}_table.csv"
        level_df.to_csv(output_file, index=False)


def main():
    """
    Cleans raw Kraken2-style taxonomy output
    and generates abundance tables for each taxonomic level.
    """

    if not INPUT_FILE.exists():
        raise FileNotFoundError("input_taxonomy.txt not found")

    # 🔹 Load input
    raw_df = pd.read_csv(INPUT_FILE, sep="\t")

    # 🔹 Expect taxonomy column to be named 'Taxon'
    if "Taxon" not in raw_df.columns:
        raw_df.columns = ["Taxon"] + list(raw_df.columns[1:])

    # 🔹 Clean taxonomy
    cleaned_df = clean_taxonomy_table(raw_df)

    # 🔹 Save full cleaned table
    cleaned_df.to_csv(OUTPUT_CLEANED, index=False)

    # 🔹 Generate level-wise tables
    create_level_tables(cleaned_df)


if __name__ == "__main__":
    main()
