import streamlit as st
from tools import load_data, dummy_data_load


def create_dashboard():
    # st.title("Global Grid Analysis")

    data = load_data()
    # data = dummy_data_load()

    st.subheader("Raw data")
    st.dataframe(data)
    st.write(f"Total rows: {len(data)}")
