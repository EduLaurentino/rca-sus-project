# CausalRCA@4SUS Project

This repository contains datasets, exploratory analysis notebooks and a Streamlit application developed for a Ph.D. project on automated root cause analysis (RCA) in epidemiology using public health data from Brazil. The goal is to integrate data from multiple sources—such as SIVEP‑Gripe, IBGE, INMET, MapBiomas and others—to explore causal relationships and support analyses using causal inference and machine learning. It serves as a central place to store data, code, documentation and references used in the project.

## Contents

- **data/SIVEP/2019/** – Contains aggregated counts and raw microdata for the year 2019:
  - `aggregated_sivep_2019.csv` – Aggregated counts of SRAG cases by Brazilian state (`SG_UF`) and date of symptom onset (`DT_SIN_PRI`) for 2019.
  - `INFLUD19-26-06-2025.zip` – Compressed SIVEP‑Gripe microdata for 2019 (single ZIP file).

- **data/SIVEP/2020/** – Contains aggregated counts and raw microdata for the year 2020:
  - `aggregated_sivep_2020.csv` – Aggregated counts of SRAG cases by state and date of symptom onset for 2020.
  - `INFLUD20-26-06-2025.zip` and `INFLUD20-26-06-2025.z01.part00`–`part10` – Segmented ZIP archive of the original SIVEP‑Gripe microdata for 2020. Because the dataset is too large to upload in a single file via GitHub, it is split into a main `.zip` file and multiple `.part` files.

- **data/IBGE/shapefiles/** – Shapefiles from IBGE for territorial boundaries:
  - `BR_UF_2022.zip` – Shapefile of Brazil’s 27 states (Unidades Federativas) for 2022.
  - `BR_Pais_2022.zip` – Shapefile of the national territory of Brazil for 2022.

- **data/IBGE/population/** – Population estimates from IBGE:
  - `estimativa_dou_2021.xls` – Excel file with 2021 population estimates for Brazil and each state.

- **analises/** – Jupyter notebooks and supporting files for exploratory data analysis:
  - `eda_sivep.ipynb` – Exploratory analysis of SRAG data and calculation of incidence rates.
  - `eda_sivep_spatial.ipynb` – Spatial analysis of SRAG using IBGE shapefiles.
  - `requirements.txt` – List of Python dependencies required to run the notebooks and the Streamlit app.

- **app.py** – Streamlit application for exploring the aggregated datasets and documenting the project’s objectives and data sources.

- **referencias/** – Reference materials and documentation:
  - `origem_dados.md` – Summary document describing each dataset and its download source.
  - `origem_dados_hyperlinks.pdf` – PDF version of the data source summary with clickable hyperlinks.
  - `Ph.D in Causal Inference.pdf`, `BRACIS2025rca_Springer.pdf`, `Estimating Categorical Counterfactuals via Deep Twin Networks.pdf`, `Dicionario_de_Dados_SRAG_Hospitalizado_23.03.2021.pdf` – Research papers and official data dictionary used as references.

## Reconstructing the SIVEP‑Gripe Datasets

The original SIVEP‑Gripe CSV files (`INFLUD19-26-06-2025.csv` for 2019 and `INFLUD20-26-06-2025.csv` for 2020) are much larger than GitHub’s upload limit. For 2020, the ZIP archive has been split into a main `.zip` file and multiple `.part` files. To reconstruct the full ZIP and extract the CSV on your local machine, install the `zip` utility and run:

```bash
# Combine the parts into a single ZIP file (requires `zip` >= 3.0):
zip -s 0 INFLUD20-26-06-2025.zip --out INFLUD20-26-06-2025-combined.zip

# Unzip the combined archive to obtain the CSV:
unzip INFLUD20-26-06-2025-combined.zip
```

Alternatively, if `zip` with split support is not available, you can concatenate the parts manually and then unzip:

```bash
# Concatenate all part files (ensure correct order) and the main zip:
cat INFLUD20-26-06-2025.z01.part* INFLUD20-26-06-2025.zip > INFLUD20-26-06-2025-complete.zip
unzip INFLUD20-26-06-2025-complete.zip
```

Either method will produce the original `INFLUD20-26-06-2025.csv` used to generate the aggregated dataset. For 2019, simply unzip `INFLUD19-26-06-2025.zip` to obtain `INFLUD19-26-06-2025.csv`.

## Running the Streamlit Application

To run the app locally, clone this repository and install the required dependencies (see `analises/requirements.txt`). A minimal example:

```bash
pip install -r analises/requirements.txt
streamlit run app.py
```

The Streamlit application provides an interactive interface to explore the aggregated SRAG datasets. On the **Data Explorer** page you can filter records by year, state (UF) and date range, view the filtered table, compute incidence rates by combining case counts with population estimates, and visualize trends via line charts. A **Map Visualisation** page displays choropleth maps of total cases or incidence rates by state using the IBGE shapefiles. A **References** page lists key research papers, data dictionaries and other documentation consulted in this project.


## Exploratory Analysis

The notebooks in the `analises` directory demonstrate how to load and analyze the aggregated datasets, calculate incidence rates using population data, and visualize spatial patterns using the shapefiles. They serve as templates for further analyses.

## References

The `referencias` directory contains the research proposal for this Ph.D. project, key papers on causal inference (including those on deep twin networks), official data dictionaries for SIVEP‑Gripe, and a summary of the data sources with links.

---

We welcome contributions! Please open issues or pull requests if you have suggestions or wish to collaborate.
