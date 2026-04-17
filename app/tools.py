import os
import pandas as pd
import streamlit as st
from datetime import date
import random

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


def dummy_data_load(start: date = date(2025, 4, 5), end: date = date(2025, 4, 7)):
    """Loading dummy data to demo the dashboard without postgres connection"""

    random.seed(42)

    aemo_static = {
        'source': 'AEMO',
        'region': 'NSW1',
        'currency': 'AUD',
        'interval_min': 5
    }

    bmrs_static = {
        'source': 'BMRS',
        'region': 'GB',
        'currency': 'GBP',
        'interval_min': 30
    }

    def create_source_df(static_info, start, end, min_price, max_price):
        dates = pd.date_range(
            start=start, end=end, freq=f"{static_info['interval_min']}min")
        df = pd.DataFrame({'timestamp_utc': dates})

        for key, value in static_info.items():
            df[key] = value

        df['price'] = [round(random.uniform(min_price, max_price), 2)
                       for _ in range(len(df))]
        return df

    aemo_df = create_source_df(aemo_static, start, end, 85, 100)
    bmrs_df = create_source_df(bmrs_static, start, end, 85, 100)

    return pd.concat([aemo_df, bmrs_df], ignore_index=True)
