# 🧬 Microbiome Report Analysis Dashboard

🚧 **Demo Version (v0.1)**  
This repository hosts an evolving Streamlit-based microbiome analysis platform.  
Development is ongoing to expand it into a full-featured microbiome analysis software with AI-driven insights.
🔹 Overview

This dashboard provides an end-to-end microbiome analysis workflow starting from raw Kraken2-style taxonomy output to publication-ready visualizations.
It is designed to be reproducible, modular, and user-friendly, especially for researchers with limited command-line experience.

1️⃣ Taxonomy File Upload

Why this step?
Microbiome classifiers such as Kraken2 generate taxonomy reports in text format. This raw output is not directly suitable for downstream analysis or visualization.

What this step does:

Accepts a Kraken2-style input_taxonomy.txt file

Standardizes the input for downstream processing

Enables non-technical users to start analysis via a GUI instead of command line

Tool used:

Streamlit file uploader – simplifies user interaction and ensures reproducibility

2️⃣ Taxonomy Cleaning & Table Generation

Why this step?
Raw taxonomy outputs often contain:

Redundant classifications

Unassigned or low-confidence taxa

Mixed taxonomic ranks

Cleaning is essential for accurate abundance estimation.

What this step does:

Parses taxonomy strings

Separates data into standard taxonomic levels:

Domain

Phylum

Class

Order

Family

Genus

Species

Generates clean .csv abundance tables for each level

Tool / Script used:

clean_input_microbiome_taxonomy.py

Python (pandas, pathlib) for structured data processing

Output:

Individual CSV files per taxonomic rank

Stored systematically in a tables/ directory

3️⃣ Abundance Visualization (Top 10 Taxa)

Why this step?
Visualizing dominant taxa helps identify:

Microbial community composition

Shifts in abundance across samples

Potential biomarkers

Visualization options provided:

Stacked Bar Plots

Ideal for comparing relative abundance across samples

Stacked Bar Plots with Series Lines

Combines composition + trend visualization

Helps observe consistency or variation of taxa

Tools / Scripts used:

generate_all_abundance_plots.py

generate_all_abundance_plots_with_series_lines.py

Matplotlib for high-quality static plots

Output:

PNG plots saved in organized output folders

Ready for reports, posters, or publications

4️⃣ Heatmap Analysis (Top 10 Taxa)

Why this step?
Heatmaps are powerful for:

Identifying clustering patterns

Comparing taxa abundance across multiple samples

Detecting outliers and sample similarity

What this step does:

Selects top 10 abundant taxa per level

Generates heatmaps for visual comparison

Tool / Script used:

generate_all_heatmaps.py

Seaborn + Matplotlib for intuitive color scaling

Output:

High-resolution heatmap images

Downloadable for further analysis or presentations

🔁 Reproducibility & Design Philosophy

Modular Python scripts → easy to extend

GUI-based execution → accessible to wet-lab researchers

Clear directory structure → reproducible research

Downloadable outputs → publication-ready

🧪 Ideal Use Cases

16S rRNA microbiome studies

Gut microbiome comparison (healthy vs disease)

Educational demonstrations

Rapid exploratory microbiome analysis

---
