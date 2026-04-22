from tools import load_data
import streamlit as st

from dashboard import dashboard_body_app, dashboard_sidebar_app


def create_dashboard_app(load_type):

    data = load_data()
    # data = dummy_data_load()
    data_chrono = data.sort_values(by="timestamp_utc")

    if "min_date" not in st.session_state:
        st.session_state["min_date"] = data_chrono["timestamp_utc"].min()

    if "max_date" not in st.session_state:
        st.session_state["max_date"] = data_chrono["timestamp_utc"].max()

    dashboard_sidebar_app(data_chrono)
    dashboard_body_app(data)


if __name__ == "__main__":
    create_dashboard_app("real")
