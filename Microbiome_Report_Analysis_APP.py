import streamlit as st
import os
from pathlib import Path
from PIL import Image

import clean_input_microbiome_taxonomy
import generate_all_abundance_plots
import generate_all_abundance_plots_with_series_lines
import generate_all_heatmaps


# ================= CONFIG =================
TABLE_DIR = Path("tables")
TABLE_DIR.mkdir(exist_ok=True)

LEVELS = ["domain", "phylum", "class", "order", "family", "genus", "species"]
# =========================================

st.set_page_config(
    page_title="Microbiome Report Analysis Dashboard",
    layout="wide"
)

st.title("🧬 Microbiome Report Analysis Dashboard")
st.caption(
    "A reproducible, GUI-based workflow for cleaning, analyzing, and visualizing Kraken2-style microbiome taxonomy data."
)

st.info(
    "🚧 **Demo Version**: This application is an active prototype. "
    "Development is ongoing to evolve it into a full-scale microbiome analysis platform, "
    "including AI-driven insights and advanced analytics."
)

# ======================================================
# STEP 1: UPLOAD
# ======================================================
st.header("1️⃣ Upload Taxonomy File")
st.caption(
    "Upload a Kraken2-style taxonomy report (.txt) to initiate downstream microbiome analysis."
)

uploaded_file = st.file_uploader(
    "Upload input_taxonomy.txt",
    type=["txt"]
)

if uploaded_file:
    input_path = Path("input_taxonomy.txt")
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully!")

# ======================================================
# STEP 2: CLEAN TAXONOMY
# ======================================================
st.header("2️⃣ Clean & Generate Taxonomy Tables")
st.caption(
    "Cleans raw taxonomy output and generates structured abundance tables across standard taxonomic levels."
)

if st.button("Run Taxonomy Cleaning"):
    with st.spinner("Running taxonomy cleaning..."):
        clean_input_microbiome_taxonomy.main()

    st.success("Cleaning completed!")

    for level in LEVELS:
        file = f"{level}_table.csv"
        if os.path.exists(file):
            os.rename(file, TABLE_DIR / file)

# Show tables
if TABLE_DIR.exists():
    st.subheader("📄 Generated Taxonomy Tables")
    st.caption(
        "Download cleaned abundance tables for each taxonomic rank (Domain to Species)."
    )

    for file in TABLE_DIR.glob("*.csv"):
        with open(file, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {file.name}",
                data=f,
                file_name=file.name
            )

# ======================================================
# STEP 3: ABUNDANCE PLOTS (CHOICE BASED)
# ======================================================
st.header("3️⃣ Abundance Plots (Top 10)")
st.caption(
    "Visualize the top 10 most abundant taxa across samples using composition-based plots."
)

plot_mode = st.radio(
    "Choose plot style",
    options=[
        "Stacked bar plots",
        "Stacked bar plots + series lines"
    ]
)

st.caption(
    "Select plots with series lines to observe abundance trends alongside taxonomic composition."
)

if st.button("Generate Abundance Plots"):
    with st.spinner("Generating abundance plots..."):

        if plot_mode == "Stacked bar plots":
            generate_all_abundance_plots.main()
            output_folder = "abundance_plots"
        else:
            generate_all_abundance_plots_with_series_lines.main()
            output_folder = "abundance_plots_with_lines"

    st.success("Abundance plots generated successfully!")

# ======================================================
# VIEW + DOWNLOAD PLOTS
# ======================================================
plot_dir = Path(output_folder) if "output_folder" in locals() else None

if plot_dir and plot_dir.exists():
    st.subheader("📊 View Abundance Plots")
    st.caption("Preview and download publication-ready abundance plots.")

    for img_path in sorted(plot_dir.glob("*.png")):
        st.image(img_path, caption=img_path.name, use_container_width=True)

        with open(img_path, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {img_path.name}",
                data=f,
                file_name=img_path.name
            )

# ======================================================
# STEP 4: HEATMAPS
# ======================================================
st.header("4️⃣ Heatmaps (Top-10 taxa)")
st.caption(
    "Generate heatmaps to explore abundance patterns and clustering across samples."
)

HEATMAP_DIR = Path("heatmaps")
HEATMAP_DIR.mkdir(exist_ok=True)

if st.button("Generate Heatmaps"):
    with st.spinner("Generating heatmaps..."):
        generate_all_heatmaps.main()

    st.success("✅ Heatmaps generated!")

# ------------------------------------------------------
# VIEW + DOWNLOAD HEATMAPS
# ------------------------------------------------------
if any(HEATMAP_DIR.glob("*.png")):
    st.subheader("🔥 View Heatmaps")
    st.caption("High-resolution heatmaps highlighting dominant taxa distributions.")

    for img in sorted(HEATMAP_DIR.glob("*.png")):
        st.image(Image.open(img), caption=img.name, width="stretch")
        with open(img, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {img.name}",
                data=f,
                file_name=img.name
            )

# ======================================================
# DOWNLOAD ALL RESULTS
# ======================================================
import zipfile
import io

st.markdown("---")
st.subheader("⬇️ Download Analysis Results")

st.caption(
    "Download all generated tables, plots, and cleaned files as a single ZIP archive."
)

def collect_result_files():
    files = []

    folders = [
        Path("tables"),
        Path("abundance_plots"),
        Path("abundance_plots_with_lines"),
        Path("heatmaps"),
    ]

    for folder in folders:
        if folder.exists():
            files.extend(folder.glob("*"))

    extra_files = [
        Path("cleaned_taxonomy.csv"),
        Path("input_taxonomy.txt"),
    ]

    for f in extra_files:
        if f.exists():
            files.append(f)

    return files


result_files = collect_result_files()

if result_files:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in result_files:
            zipf.write(file, arcname=file.as_posix())

    zip_buffer.seek(0)

    st.download_button(
        label="📦 Download all results (ZIP)",
        data=zip_buffer,
        file_name="microbiome_analysis_results.zip",
        mime="application/zip"
    )
else:
    st.info("No results available yet. Run the analysis to enable download.")

# ======================================================
# CLEAR PREVIOUS RUN
# ======================================================
st.markdown("---")
st.subheader("🧹 Clear Previous Analysis")

st.caption(
    "Remove all generated tables, plots, and uploaded files to start a fresh analysis run."
)

if st.button("Clear all results and reset"):
    paths_to_clear = [
        Path("tables"),
        Path("abundance_plots"),
        Path("abundance_plots_with_lines"),
        Path("heatmaps"),
        Path("input_taxonomy.txt"),
        Path("cleaned_taxonomy.csv")
    ]

    for path in paths_to_clear:
        if path.exists():
            if path.is_dir():
                for f in path.glob("*"):
                    f.unlink()
            else:
                path.unlink()

    st.success("Previous analysis cleared. You can refresh the page, then upload a new file and rerun the pipeline.")


st.markdown("---")
st.caption("Designed for fast, reproducible, and user-friendly microbiome analysis.")
