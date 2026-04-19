import streamlit as st
from tools import load_data, dummy_data_load

def create_dashboard():
    st.title('Global Grid Analysis')

    # data = load_data()
    data = load_data()

    st.subheader('Raw data')
    st.dataframe(data)