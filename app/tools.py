import os
import pandas as pd
import streamlit as st
import psycopg2

@st.cache_data
def load_data():
        
    db_name = os.getenv("POSTGRES_DB")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    conn = psycopg2.connect(
        dbname=db_name, user=db_user, password=db_password, host=db_host
    )

    sql_query = "SELECT * FROM energy_prices"

    df = pd.read_sql_query(sql=sql_query, con=conn)

    conn.close()

    return df
