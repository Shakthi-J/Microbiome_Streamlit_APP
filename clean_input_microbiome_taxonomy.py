import pandas as pd

# ================= CONFIG =================
INPUT_FILE = "input_taxonomy.txt"
OUTPUT_CLEANED = "cleaned_taxonomy.csv"

OUTPUT_PREFIX = "taxonomy_level_"

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

        print(f"📄 Created {output_file}")


def main():
    print("📥 Reading input file...")
    raw_df = pd.read_csv(INPUT_FILE, sep="\t")

    print("🧹 Cleaning taxonomy...")
    cleaned_df = clean_taxonomy_table(raw_df)

    print("💾 Saving cleaned full table...")
    cleaned_df.to_csv(OUTPUT_CLEANED, index=False)

    print("📊 Creating taxonomic-level tables...")
    create_level_tables(cleaned_df)

    print("✅ All files generated successfully!")


if __name__ == "__main__":
    main()

