"""
Streamlit application for exploring aggregated SRAG (Severe Acute Respiratory Syndrome) data.

This app was created as part of a research project on automated root cause analysis (RCA) and
causal inference in epidemiology. The goal is to provide a simple interface for exploring
aggregated counts of SRAG cases by state and date and to serve as a foundation for more
advanced analyses and visualizations. Additional pages and features can be added as the
project evolves.

To run the application, install the required dependencies (streamlit and pandas) and run:

    streamlit run app.py

The aggregated dataset `aggregated_sivep_2020.csv` should be placed in the same directory
as this script. The app will load it and allow filtering by state and date range.
"""

import streamlit as st
import pandas as pd


def home_page() -> None:
    """Render the Home page with an overview of the project."""
    st.title("Root Cause Analysis on SRAG Data")
    st.write(
        """
        This Streamlit app is part of a research project exploring causal relationships
        in epidemiological data (SRAG) from Brazil. Use the sidebar to navigate
        through pages, explore data, and read about project objectives and data sources.
        """
    )
    st.header("Project Overview")
    st.markdown(
        """
        This application was built for a Ph.D. project on causal inference in epidemiology.
        It aims to facilitate data exploration and provide a foundation for root cause
        analysis (RCA) using public datasets provided by SUS, IBGE, INMET and others.
        """
    )
    st.header("Dataset Summary")
    st.markdown(
        """
        The dataset used in this demo consists of aggregated counts of SRAG cases by
        Brazilian state (``SG_UF``) and date of symptom onset (``DT_SIN_PRI``). The counts
        were generated from the SIVEP‑Gripe surveillance system for 2020. The aggregated
        data has far fewer rows than the full microdata, making it suitable for quick
        exploration and visualisation in a web app.
        """
    )


def data_page() -> None:
    """Render the Data page with filters and visualizations."""
    st.title("SRAG Aggregated Data Explorer")

    @st.cache_data
    def load_data() -> pd.DataFrame:
        """Load the aggregated data from CSV. Cached for performance."""
        return pd.read_csv("aggregated_sivep_2020.csv")

    df = load_data()

    st.write("Use the filters below to explore the data.")

    # Convert date column to datetime
    df["DT_SIN_PRI"] = pd.to_datetime(df["DT_SIN_PRI"])

    # State filter
    states = st.multiselect(
        "Select state(s) (SG_UF)",
        options=sorted(df["SG_UF"].unique()),
        default=sorted(df["SG_UF"].unique()),
    )

    # Date range filter
    min_date = df["DT_SIN_PRI"].min()
    max_date = df["DT_SIN_PRI"].max()
    date_range = st.slider(
        "Select date range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD",
    )

    # Apply filters
    filtered_df = df[
        (df["SG_UF"].isin(states))
        & (df["DT_SIN_PRI"] >= date_range[0])
        & (df["DT_SIN_PRI"] <= date_range[1])
    ]

    # Display filtered data
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Aggregate for chart: sum cases by date
    df_chart = (
        filtered_df.groupby("DT_SIN_PRI")["cases"].sum().reset_index()
        .rename(columns={"DT_SIN_PRI": "Date", "cases": "Total cases"})
    )

    st.subheader("Total Cases Over Time")
    st.line_chart(df_chart.set_index("Date"))
    st.caption(
        "The line chart shows the total number of SRAG cases per day across the selected states."
    )


def sources_page() -> None:
    """Render the Sources page with data source descriptions."""
    st.title("Data Sources and References")
    st.write(
        """
        **Data Sources**

        - **SIVEP‑Gripe**: The Brazilian surveillance system for severe acute respiratory syndrome (SRAG), providing case‑level data.
        - **IBGE**: Demographic and socioeconomic data used to contextualize epidemiological factors (population, income, education, etc.).
        - **INMET**: Meteorological data, such as temperature and precipitation, used to incorporate climate variables into analysis.
        - **MapBiomas/INPE**: Environmental and deforestation data for contextualizing land use and environmental exposures.

        **Project Objectives**

        This project aims to integrate data from multiple sources to perform automated root cause analysis of SRAG cases in Brazil using causal
        inference methods. The Streamlit app serves as an interactive exploration tool to inspect the aggregated dataset and to document the
        goals and sources underlying the research. As more data are collected and models are developed, the app will evolve to include
        model outputs, causal effect estimates and interactive dashboards.
        """
    )


def main() -> None:
    """Main function to run the Streamlit app with navigation."""
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Home", "Data", "Sources"))
    if page == "Home":
        home_page()
    elif page == "Data":
        data_page()
    else:
        sources_page()


if __name__ == "__main__":
    main()