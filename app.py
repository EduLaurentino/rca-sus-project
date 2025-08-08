"""
Streamlit application for RCA SUS Project

This app provides an interactive interface to explore the aggregated SRAG (Síndrome Respiratória
Aguda Grave) datasets made available in this repository. Users can filter data by year,
state and date range, compute incidence rates using population estimates and visualise
temporal trends and spatial patterns via charts and choropleth maps. A dedicated
references page lists the research papers, project documentation and data dictionaries
used throughout the project.

To run the app locally install the dependencies from ``requirements.txt`` and then
execute ``streamlit run app.py`` from the repository root.
"""

import os
import datetime

import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
# Configuration
st.set_page_config(page_title="RCA SUS Data Explorer", layout="wide")


@st.cache_data
def load_aggregated_data(year: int) -> pd.DataFrame | None:
    """Load the aggregated SRAG counts for a given year.

    The data are stored in ``data/SIVEP/<year>/aggregated_sivep_<year>.csv``. If the
    file cannot be loaded or does not exist, this function returns ``None``.

    Parameters
    ----------
    year : int
        Year of the dataset to load (e.g., 2019, 2020).

    Returns
    -------
    pandas.DataFrame or None
        DataFrame with columns ``SG_UF`` (state abbreviation), ``DT_SIN_PRI`` (date)
        and ``COUNT`` (number of cases) or ``None`` if the file cannot be loaded.
    """
    csv_path = os.path.join("data", "SIVEP", str(year), f"aggregated_sivep_{year}.csv")
    if not os.path.exists(csv_path):
        return None
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return None
    # ensure correct types
    if 'DT_SIN_PRI' in df.columns:
        df['DT_SIN_PRI'] = pd.to_datetime(df['DT_SIN_PRI'], errors='coerce')
    return df


@st.cache_data
def load_population() -> pd.DataFrame | None:
    """Load population estimates for Brazilian states.

    Reads the Excel file in ``data/IBGE/population/estimativa_dou_2021.xls`` and
    extracts the 2021 population by state. The resulting DataFrame has two columns:
    ``SIGLA`` (state abbreviation) and ``Population`` (integer).

    Returns ``None`` if the file cannot be read.
    """
    excel_path = os.path.join("data", "IBGE", "population", "estimativa_dou_2021.xls")
    if not os.path.exists(excel_path):
        return None
    try:
        xls = pd.ExcelFile(excel_path)
    except Exception:
        return None
    try:
        df_raw = pd.read_excel(xls, sheet_name="BRASIL E UFs", header=None)
    except Exception:
        return None
    # The first three rows contain headings; data starts from row 3 and includes 27
    # states. Column 0 contains the state names, column 2 the population as string.
    data_rows = df_raw.iloc[3:3 + 27, [0, 2]].copy()
    data_rows.columns = ["UF", "Population"]
    # Clean population numbers: remove dots, commas and any footnote markers
    data_rows['Population'] = (
        data_rows['Population'].astype(str)
        .str.replace(r"\D", "", regex=True)
        .astype(int)
    )
    # Map full state names to abbreviations
    name_to_sigla = {
        "Rondônia": "RO",
        "Acre": "AC",
        "Amazonas": "AM",
        "Roraima": "RR",
        "Pará": "PA",
        "Amapá": "AP",
        "Tocantins": "TO",
        "Maranhão": "MA",
        "Piauí": "PI",
        "Ceará": "CE",
        "Rio Grande do Norte": "RN",
        "Paraíba": "PB",
        "Pernambuco": "PE",
        "Alagoas": "AL",
        "Sergipe": "SE",
        "Bahia": "BA",
        "Minas Gerais": "MG",
        "Espírito Santo": "ES",
        "Rio de Janeiro": "RJ",
        "São Paulo": "SP",
        "Paraná": "PR",
        "Santa Catarina": "SC",
        "Rio Grande do Sul": "RS",
        "Mato Grosso do Sul": "MS",
        "Mato Grosso": "MT",
        "Goiás": "GO",
        "Distrito Federal": "DF",
    }
    data_rows['SIGLA'] = data_rows['UF'].map(name_to_sigla)
    return data_rows[['SIGLA', 'Population']]


@st.cache_data
def load_shapefile() -> gpd.GeoDataFrame | None:
    """Load Brazil's state boundaries shapefile.

    Reads the shapefile archive ``data/IBGE/shapefiles/BR_UF_2022.zip`` using
    ``geopandas``. The returned GeoDataFrame includes columns ``SIGLA_UF`` (state
    abbreviation), ``NM_UF`` (state name), ``NM_REGIAO`` (region), ``AREA_KM2`` and
    the geometry. Returns ``None`` if the file is missing or cannot be read.
    """
    shp_zip = os.path.join("data", "IBGE", "shapefiles", "BR_UF_2022.zip")
    if not os.path.exists(shp_zip):
        return None
    try:
        gdf = gpd.read_file(f"zip://{shp_zip}")
    except Exception:
        return None
    return gdf


def home_page() -> None:
    """Display the home page with project overview."""
    st.title("RCA SUS Project")
    st.markdown(
        """
        ### Automated Root Cause Analysis in Epidemiology

        This project aims to develop a reproducible pipeline for automated root cause analysis (RCA)
        applied to respiratory syndromes in Brazil. Using public health data from SIVEP‑Gripe, socio‑
        demographic data from IBGE and environmental data (e.g., shapefiles), we explore causal
        relationships and estimate incidence rates, leveraging causal inference and machine learning
        techniques. The goal is to provide interactive tools for data exploration and to support
        epidemiological studies using open datasets from the SUS.

        Use the navigation menu on the left to explore the data, visualise spatial patterns, or
        consult the references underpinning this work.
        """
    )


def data_explorer_page() -> None:
    """Interactive page for exploring aggregated SRAG counts and incidence."""
    st.header("Data Explorer")
    # Determine available years by inspecting the data directory
    available_years = []
    for year_dir in os.listdir(os.path.join("data", "SIVEP")):
        if year_dir.isdigit():
            df_test = load_aggregated_data(int(year_dir))
            if df_test is not None:
                available_years.append(int(year_dir))
    available_years.sort()
    if not available_years:
        st.warning("No aggregated datasets are available.")
        return
    selected_year = st.selectbox("Select year", available_years, index=0)
    df = load_aggregated_data(selected_year)
    if df is None or df.empty:
        st.warning(f"Aggregated data for {selected_year} could not be loaded.")
        return
    # Convert dates to pandas datetime
    df = df.dropna(subset=['DT_SIN_PRI'])
    # Determine date range for slider
    min_date = df['DT_SIN_PRI'].min().date()
    max_date = df['DT_SIN_PRI'].max().date()
    date_range = st.slider(
        "Date range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD",
    )
    start_date, end_date = [datetime.date.fromisoformat(str(d)) for d in date_range]
    unique_states = sorted(df['SG_UF'].dropna().unique().tolist())
    default_states = unique_states  # show all by default
    selected_states = st.multiselect(
        "Select states", unique_states, default=default_states, key="states_select"
    )
    # Filter data
    mask = (
        (df['DT_SIN_PRI'].dt.date >= start_date)
        & (df['DT_SIN_PRI'].dt.date <= end_date)
        & (df['SG_UF'].isin(selected_states))
    )
    filtered_df = df.loc[mask].copy()
    if filtered_df.empty:
        st.info("No data match the selected filters.")
        return
    # Show raw data table
    st.subheader("Filtered aggregated data")
    st.dataframe(filtered_df.sort_values(['DT_SIN_PRI', 'SG_UF']))
    # Display daily total counts across selected states
    daily_counts = (
        filtered_df.groupby('DT_SIN_PRI')['COUNT'].sum().rename('Total Cases').reset_index()
    )
    st.subheader("Temporal trend across selected states")
    st.line_chart(daily_counts.set_index('DT_SIN_PRI'))
    # Compute incidence per state if population is available
    pop_df = load_population()
    if pop_df is not None:
        state_counts = (
            filtered_df.groupby('SG_UF')['COUNT'].sum().reset_index()
        )
        merged = state_counts.merge(pop_df, left_on='SG_UF', right_on='SIGLA', how='left')
        merged['incidence'] = merged.apply(
            lambda row: (row['COUNT'] / row['Population'] * 100000)
            if pd.notnull(row['Population']) else None,
            axis=1,
        )
        merged = merged.sort_values('incidence', ascending=False)
        st.subheader("Incidence rates per 100k inhabitants")
        st.table(merged[['SG_UF', 'COUNT', 'Population', 'incidence']])
        # Bar chart for counts and incidence
        bar_data = merged.set_index('SG_UF')[['COUNT', 'incidence']]
        st.bar_chart(bar_data)
    else:
        st.info("Population data not available; incidence rates cannot be computed.")


def maps_page() -> None:
    """Display choropleth maps of SRAG counts or incidence by state."""
    st.header("Map Visualisation")
    # Determine available years
    available_years = []
    for year_dir in os.listdir(os.path.join("data", "SIVEP")):
        if year_dir.isdigit():
            df_test = load_aggregated_data(int(year_dir))
            if df_test is not None and not df_test.empty:
                available_years.append(int(year_dir))
    available_years.sort()
    if not available_years:
        st.warning("No aggregated datasets are available for mapping.")
        return
    year = st.selectbox("Select year", available_years, index=0)
    agg_df = load_aggregated_data(year)
    if agg_df is None or agg_df.empty:
        st.warning(f"Aggregated data for {year} could not be loaded.")
        return
    shapefile = load_shapefile()
    if shapefile is None:
        st.warning("Shapefile for Brazil could not be loaded.")
        return
    # Aggregate counts by state
    state_counts = agg_df.groupby('SG_UF')['COUNT'].sum().reset_index(name='cases')
    gdf = shapefile.merge(state_counts, left_on='SIGLA_UF', right_on='SG_UF', how='left')
    gdf['cases'] = gdf['cases'].fillna(0)
    pop_df = load_population()
    if pop_df is not None:
        gdf = gdf.merge(pop_df, left_on='SIGLA_UF', right_on='SIGLA', how='left')
        gdf['incidence'] = gdf.apply(
            lambda row: (row['cases'] / row['Population'] * 100000)
            if pd.notnull(row['Population']) and row['Population'] > 0 else None,
            axis=1,
        )
    # Choose metric to display
    metrics = {'Total Cases': 'cases'}
    if 'incidence' in gdf.columns:
        metrics['Incidence (per 100k)'] = 'incidence'
    metric_label = st.selectbox("Metric", list(metrics.keys()), index=0)
    metric = metrics[metric_label]
    # Plot choropleth using matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))
    # Set NaN values to zero for plotting
    plot_gdf = gdf.copy()
    plot_gdf[metric] = plot_gdf[metric].fillna(0)
    # Determine a colour map based on metric
    cmap = 'OrRd' if metric == 'cases' else 'Blues'
    plot_gdf.plot(
        column=metric,
        cmap=cmap,
        linewidth=0.8,
        edgecolor='0.8',
        legend=True,
        ax=ax,
    )
    ax.set_title(f"{metric_label} by State – {year}")
    ax.axis('off')
    st.pyplot(fig)


def references_page() -> None:
    """Display a list of references and data sources."""
    st.header("References")
    st.markdown(
        """
        The **referencias** directory of this repository contains the core references for
        this project, including:

        - **origem_dados.md** – Markdown document describing the origin and download link
          for each dataset used in this repository.
        - **origem_dados_hyperlinks.pdf** – PDF version of the above document with
          clickable hyperlinks for convenience.
        - **Ph.D in Causal Inference.pdf**, **BRACIS2025rca_Springer.pdf** and
          **Estimating Categorical Counterfactuals via Deep Twin Networks.pdf** –
          Key research papers underpinning the causal inference approaches adopted here.
        - **Dicionario_de_Dados_SRAG_Hospitalizado_23.03.2021.pdf** – Official data
          dictionary for the SIVEP‑Gripe SRAG hospitalised cases dataset.

        To view these documents, navigate to the ``referencias`` folder in the repository.
        """
    )


def main() -> None:
    """Main entry point of the Streamlit application."""
    pages = {
        "Home": home_page,
        "Data Explorer": data_explorer_page,
        "Map Visualisation": maps_page,
        "References": references_page,
    }
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", list(pages.keys()))
    pages[choice]()


if __name__ == "__main__":
    main()