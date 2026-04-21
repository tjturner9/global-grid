import os
import pandas as pd
import streamlit as st
from datetime import date
import random

import psycopg2


# @st.cache_data
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
        "source": "AEMO",
        "currency": "AUD",
        "interval_min": 5,
    }

    bmrs_static = {
        "source": "BMRS",
        "region": "GB",
        "currency": "GBP",
        "interval_min": 30,
    }

    def _load_static_info(dates, static_info, min_price, max_price):

        df = pd.DataFrame({"timestamp_utc": dates})

        for key, value in static_info.items():
            df[key] = value

        df["price"] = [
            round(random.uniform(min_price, max_price), 2) for _ in range(len(df))
        ]

        return df

    def create_source_df(static_info, start, end, min_price, max_price):
        dates = pd.date_range(
            start=start, end=end, freq=f"{static_info['interval_min']}min"
        )

        if "AUD" in static_info.values():
            dfs = []
            regions = ["NSW1", "VIC1", "QLD1", "SA1", "TAS1"]

            for region in regions:
                static_info['region'] = region

                df = _load_static_info(
                    dates, static_info, min_price, max_price)
                dfs.append(df)

            df = pd.concat(dfs, ignore_index=True)
        else:
            df = _load_static_info(dates, static_info, min_price, max_price)

        return df

    aemo_df = create_source_df(aemo_static, start, end, 85, 100)
    bmrs_df = create_source_df(bmrs_static, start, end, 40, 55)

    return pd.concat([aemo_df, bmrs_df], ignore_index=True)


def pivot_data(df, min_date, max_date):
    """data prep for time series chart"""

    df[df['timestamp_utc'].between(min_date, max_date)]
    # Aggregate - group by timestamp and source
    grouped_data = df.groupby(by=['timestamp_utc', 'source'], as_index=False)[
        'price'].mean()

    # pivot - reshape timestamp into index an each source as a column
    pivoted_data = grouped_data.pivot(
        columns='source', index='timestamp_utc', values='price')

    # resampling - resample the df to 30-min intervals
    resampled_data = pivoted_data.resample('30min').mean()

    return resampled_data


def calculate_spread(df):
    df = df.copy()
    # convert BMRS to AUD
    # TODO - replace static rate with historic rate, lookup by timestamp
    conversion_rate = 2.03
    df['BMRS_AUD'] = df['BMRS'] * conversion_rate

    # add dpread column (AEMO - BMRS_AUD)
    df['spread'] = df['AEMO'] - df['BMRS_AUD']

    df = df.drop(columns=['AEMO', 'BMRS', 'BMRS_AUD'])

    return df


def region_pivot(df: pd.DataFrame):
    df = df.copy()

    df = df.pivot(columns='region', index='timestamp_utc', values='price')

    return df
