import streamlit as st

from dashboard import dashboard_body_app, dashboard_sidebar_app, import_data


def create_dashboard_app(load_type):

    data = import_data(load_type)
    data_chrono = data.sort_values(by='timestamp_utc')

    if 'min_date' not in st.session_state:
        st.session_state['min_date'] = data_chrono['timestamp_utc'].min()

    if 'max_date' not in st.session_state:
        st.session_state['max_date'] = data_chrono['timestamp_utc'].max()

    dashboard_sidebar_app(data_chrono)
    dashboard_body_app(data)


if __name__ == "__main__":
    create_dashboard_app(load_type='dummy')
