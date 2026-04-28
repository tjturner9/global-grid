import os
import streamlit as st
import pandas as pd
from dashboard import body_region, sidebar_region
from tools import import_data
from dotenv import load_dotenv
load_dotenv()

load_type = os.getenv("LOAD_TYPE", "real")

data = import_data(load_type)
data = data[data["source"] == "AEMO"]

if "min_date" not in st.session_state:
        # st.session_state["min_date"] = data_chrono["timestamp_utc"].min()
        st.session_state["min_date"] = pd.Timestamp('2025-11-01', tz='UTC')

if "max_date" not in st.session_state:
    st.session_state["max_date"] = data["timestamp_utc"].max()

if "selected_regions" not in st.session_state:
    st.session_state["selected_regions"] = []

sidebar_region(data)

body_region(data)
