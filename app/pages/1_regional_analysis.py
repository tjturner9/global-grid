import streamlit as st
from dashboard import dashboard_body_region, dashboard_sidebar_region, import_data


data = import_data(load_type='dummy')
data = data[data['source'] == 'AEMO']

if 'min_date' not in st.session_state:
    st.session_state['selected_regions'] = []

dashboard_sidebar_region(data)

dashboard_body_region(data)
