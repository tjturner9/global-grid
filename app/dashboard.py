import streamlit as st
from tools import calculate_spread, load_data, dummy_data_load, pivot_data, region_pivot


@st.cache_data
def import_data(load_type='real'):
    if load_data == 'real':
        data = load_data()

    else:
        data = dummy_data_load()

    return data


def create_import_summary(data):

    st.subheader("Raw data")
    st.dataframe(data)
    st.write(f"Total rows: {len(data)}")


def dashboard_body_app(data):
    # create_import_summary(data)

    st.write('AEMO Vs BMRS')
    data = pivot_data(data,
                      st.session_state['min_date'],
                      st.session_state['max_date']
                      )
    st.line_chart(data)

    st.write('Spread data')
    spread_data = calculate_spread(data)
    st.line_chart(spread_data)


def dashboard_sidebar_app(data):

    with st.sidebar:
        min_date = st.datetime_input(
            label="Minimum date", value=data['timestamp_utc'].min(), key='min_date')

        max_date = st.datetime_input(
            label="Maxmum date", value=data['timestamp_utc'].max(), key='max_date')


def dashboard_sidebar_region(data):
    with st.sidebar:
        min_date = st.datetime_input(
            label="Minimum date", value=data['timestamp_utc'].min(), key='min_date')

        max_date = st.datetime_input(
            label="Maxmum date", value=data['timestamp_utc'].max(), key='max_date')

        regions = ["NSW1", "VIC1", "QLD1", "SA1", "TAS1"]

        select_regions = st.multiselect("Select regions to compare",
                                        regions,
                                        key='selected_regions')

        st.write(st.session_state['selected_regions'])


def dashboard_body_region(data):
    # regions selected size based on st.session_state['selected_regions']
    
    # 0 regions selected = "select a region"

    # 1, 3, 4, 5 region selected = only graph

    # 2 regions selected = graph + spread

    data = region_pivot(data)
    regions = ["NSW1", "VIC1", "QLD1", "SA1", "TAS1"]
    regions_to_keep = st.session_state['selected_regions']
    regions_to_drop = list(set(regions) - set(regions_to_keep))
    data = data.drop(columns=regions_to_drop)
    st.line_chart(data)
