from datetime import timezone
import pandas as pd
import streamlit as st
from tools import (
    calculate_bmrs_aemo_spread,
    calculate_region_spread,
    pivot_data,
    prepare_dispatch_settlement,
    region_pivot,
)


def create_import_summary(data: pd.DataFrame):

    st.subheader("Raw data")
    st.dataframe(data)
    st.write(f"Total rows: {len(data)}")


def body_app(data: pd.DataFrame):
    # create_import_summary(data)

    st.write("AEMO Vs BMRS")
    data = pivot_data(
        data, st.session_state["min_date"], st.session_state["max_date"])
    st.line_chart(data)

    st.write("Spread data")
    spread_data = calculate_bmrs_aemo_spread(data)
    st.line_chart(spread_data)


def sidebar_app(data: pd.DataFrame):

    with st.sidebar:
        min_date = st.datetime_input(
            label="Minimum date", value=data["timestamp_utc"].min(), key="min_date"
        )

        max_date = st.datetime_input(
            label="Maxmum date", value=data["timestamp_utc"].max(), key="max_date"
        )


def sidebar_region(data: pd.DataFrame):
    with st.sidebar:
        min_date = st.datetime_input(
            label="Minimum date",
            value=data["timestamp_utc"].min(),
            key="min_date"
        )

        max_date = st.datetime_input(
            label="Maximum date",
            value=data["timestamp_utc"].max(),
            key="max_date"
        )

        regions = data['region'].unique()

        select_regions = st.multiselect(
            "Select regions to compare", regions, key="selected_regions"
        )

        st.write(st.session_state["selected_regions"])


def body_region(data: pd.DataFrame):
    # regions selected size based on st.session_state['selected_regions']
    selected_region_length = len(st.session_state["selected_regions"])
    data = region_pivot(
        data, st.session_state["min_date"], st.session_state["max_date"]
    )
    regions = ["NSW1", "VIC1", "QLD1", "SA1", "TAS1"]
    regions_to_keep = st.session_state["selected_regions"]
    regions_to_drop = list(set(regions) - set(regions_to_keep))
    data = data.drop(columns=regions_to_drop)

    if selected_region_length == 0:
        st.write(
            "Please start selecting regions to analyse. Select only 2 to analyse price spread."
        )

    elif selected_region_length == 2:
        st.write("Time series of selected regions")
        st.line_chart(data)
        spread = calculate_region_spread(
            data, st.session_state["selected_regions"])
        st.write("Spread of price")
        st.line_chart(spread)

    else:
        data = data.drop(columns=["spread"], errors="ignore")
        st.write("Time series of selected regions")
        st.line_chart(data)


def sidebar_dispatch(data: pd.DataFrame):
    regions = data['region'].unique()
    with st.sidebar:
        selected_regions = st.radio(
            label="Select region to analyse",
            options=regions,
            key='selected_regions',
        )

        min_date = st.datetime_input(
            label="Minimum date",
            value=data["timestamp_utc"].min(),
            key="min_date",
        )
        max_date = st.datetime_input(
            label="Maximum date",
            value=data["timestamp_utc"].max(),
            key="max_date",
        )


def body_dispatch(data: pd.DataFrame):
    st.write(f"Showing data for: {st.session_state['selected_regions']}")
    data = prepare_dispatch_settlement(
        data, st.session_state['selected_regions'], st.session_state["min_date"], st.session_state["max_date"])
    st.line_chart(data)
