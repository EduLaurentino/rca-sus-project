# RCA SUS Project

This repository contains datasets and a Streamlit application developed for a Ph.D. project on automated root cause analysis (RCA) in
epidemiology using public health data from Brazil. The goal is to integrate data from multiple sources — including SIVEP‑Gripe, IBGE,
INMET and MapBiomas — to explore causal relationships and support analyses using causal inference and machine learning.  
It serves as a central place to store data, code and documentation used in the project.

## Contents

- **`aggregated_sivep_2020.csv`** – Aggregated counts of SRAG cases by Brazilian state (`SG_UF`) and date of symptom onset (`DT_SIN_PRI`).
  This file was generated from the SIVEP‑Gripe microdata for the year 2020. It contains one row per state per date with a
  `cases` column representing the number of cases.
- **`INFLUD20-26-06-2025.zip`** and **`INFLUD20-26-06-2025.z01.part00`–`part10`** – Segmented ZIP archive of the original SIVEP‑Gripe
  dataset. The dataset is too large to upload in a single file via GitHub, so it has been split into a main `.zip` file and
  multiple `.part` files, each smaller than 25 MB.
- **`app.py`** – Streamlit application for exploring the aggregated dataset and documenting the project’s objectives and data sources.
- **Research papers and documentation** – The repository also contains PDF files such as *Ph.D in Causal Inference*,
  *BRACIS2025rca_Springer*, and *Estimating Categorical Counterfactuals via Deep Twin Networks*. These provide theoretical
  background on causal inference and root cause analysis and are included as reference material.

## Reconstructing the Full SIVEP Dataset

The original SIVEP‑Gripe CSV (`INFLUD20-26-06-2025.csv`) is much larger than GitHub’s upload limit. It has been split into a main ZIP
file and several part files. To reconstruct the full ZIP and extract the CSV on your local machine, install the `zip` utility and run:

```bash
# Combine the parts into a single ZIP file (requires `zip` >= 3.0):
zip -s 0 INFLUD20-26-06-2025.zip --out INFLUD20-26-06-2025-combined.zip

# Unzip the combined archive to obtain the CSV:
unzip INFLUD20-26-06-2025-combined.zip
```

Alternatively, if `zip` with split support is not available, you can concatenate the parts manually and then unzip:

```bash
# Concatenate all part files (ensure correct order) and the main zip:
cat INFLUD20-26-06-2025.z01.part* > INFLUD20-26-06-2025.zip
unzip INFLUD20-26-06-2025.zip
```

Either method will produce the original `INFLUD20-26-06-2025.csv` used to generate the aggregated dataset.

## Running the Streamlit Application

To run the app locally, clone this repository and install the required dependencies:

```bash
pip install streamlit pandas
streamlit run app.py
```

The application provides a simple interface to explore the aggregated SRAG dataset. It includes filters for states and date range,
displays a table of the filtered data, and shows a line chart of total cases over time. As the project progresses, additional pages
and interactive visualizations can be added.

## Next Steps

- **Data integration** – Expand the dataset by integrating demographic, socioeconomic, environmental and climatic variables at
  municipal or regional levels (e.g. IBGE census data, INMET weather data, MapBiomas land use data).
- **Causal modeling** – Implement causal inference methods (DoWhy, Pyro, CausalML, EconML) to estimate causal effects and
  perform root cause analysis on the integrated dataset.
- **App expansion** – Enhance the Streamlit app to include model outputs, dashboards, maps and interactive tools for exploring
  heterogeneous causal effects.

## Contributing

This repository is private and intended for collaborators within the research group. If you wish to contribute, fork the repository,
create a feature branch, make your changes and open a pull request for review. Please adhere to best practices for data privacy and
keep any sensitive information secure.

## License

The data contained in this repository originates from public sources (SIVEP‑Gripe, IBGE, INMET, MapBiomas, etc.) and is subject to
their respective licenses and usage restrictions. This repository itself is shared under an academic use agreement for research
purposes only. No warranty is expressed or implied; use it at your own risk.