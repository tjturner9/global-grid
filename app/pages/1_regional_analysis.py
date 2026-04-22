import streamlit as st
from dashboard import dashboard_body_region, dashboard_sidebar_region
from tools import load_data, dummy_data_load

data = load_data()
# data = dummy_data_load()
data = data[data["source"] == "AEMO"]

if "min_date" not in st.session_state:
    st.session_state["min_date"] = data["timestamp_utc"].min()

if "max_date" not in st.session_state:
    st.session_state["max_date"] = data["timestamp_utc"].max()

if "selected_regions" not in st.session_state:
    st.session_state["selected_regions"] = []

dashboard_sidebar_region(data)

st.write(st.session_state["min_date"])
st.write(st.session_state["max_date"])
dashboard_body_region(data)
