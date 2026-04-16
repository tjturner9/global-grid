import streamlit as st
import pandas as pd
from app.tools import load_data



st.title('Global Grid Analysis')

data = load_data()

st.subheader('Raw data')
st.write(data)