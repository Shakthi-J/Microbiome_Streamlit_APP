import streamlit as st
import subprocess
import os
from pathlib import Path
from PIL import Image

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
        subprocess.run(
            ["python", "clean_input_microbiome_taxonomy.py"],
            check=True
        )
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
            script = "generate_all_abundance_plots.py"
            output_folder = "abundance_plots"

        else:
            script = "generate_all_abundance_plots_with_series_lines.py"
            output_folder = "abundance_plots_with_lines"

        subprocess.run(
            ["python", script],
            check=True
        )

    st.success("Abundance plots generated successfully!")

# ======================================================
# VIEW + DOWNLOAD PLOTS
# ======================================================
plot_dir = Path(output_folder) if 'output_folder' in locals() else None

if plot_dir and plot_dir.exists():
    st.subheader("📊 View Abundance Plots")
    st.caption(
        "Preview and download publication-ready abundance plots."
    )

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
        subprocess.run(
            ["python", "generate_all_heatmaps.py"],
            check=True
        )
    st.success("✅ Heatmaps generated!")

# ------------------------------------------------------
# VIEW + DOWNLOAD HEATMAPS
# ------------------------------------------------------
if any(HEATMAP_DIR.glob("*.png")):
    st.subheader("🔥 View Heatmaps")
    st.caption(
        "High-resolution heatmaps highlighting dominant taxa distributions."
    )

    for img in sorted(HEATMAP_DIR.glob("*.png")):
        st.image(Image.open(img), caption=img.name, width="stretch")
        with open(img, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {img.name}",
                data=f,
                file_name=img.name
            )

st.markdown("---")
st.caption(
    "Designed for fast, reproducible, and user-friendly microbiome analysis."
)

