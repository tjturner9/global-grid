import os
from tools import import_data
import streamlit as st
from dotenv import load_dotenv
from dashboard import body_app, sidebar_app

load_dotenv()
load_type = os.getenv("LOAD_TYPE", "real")

def create_app(load_type):

    data = import_data(load_type)
    data_chrono = data.sort_values(by="timestamp_utc")

    if "min_date" not in st.session_state:
        st.session_state["min_date"] = data_chrono["timestamp_utc"].min()

    if "max_date" not in st.session_state:
        st.session_state["max_date"] = data_chrono["timestamp_utc"].max()

    sidebar_app(data_chrono)
    body_app(data)


if __name__ == "__main__":
    create_app(load_type)
