import os
import streamlit as st
from dashboard import body_dispatch, sidebar_dispatch
from tools import import_data
from dotenv import load_dotenv
load_dotenv()

load_type = os.getenv("LOAD_TYPE", "real")

data = import_data(load_type)
data = data[data["source"] == "AEMO"]

if "min_date" not in st.session_state:
    st.session_state["min_date"] = data["timestamp_utc"].min()

if "max_date" not in st.session_state:
    st.session_state["max_date"] = data["timestamp_utc"].max()

if "selected_regions" not in st.session_state:
    st.session_state["selected_regions"] = 'NSW1'

sidebar_dispatch(data)

body_dispatch(data)