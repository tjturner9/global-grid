import os
import psycopg2
from datetime import date
from db.init_db import init_db
from db.insert import insert_records
from scrapers import aemo, bmrs
import logging

logging.basicConfig(level=logging.INFO)

def run_pipeline(start: date = date(2025, 5, 5), end: date = date(2025, 5, 7)):
    # Initialise database schema
    init_db()

    # Fetch date range from AEMO
    aemo_records = aemo.fetch_all_region_range(
        start=start,
        end=end,
    )

    # Fetch date rande from BMRS
    bmrs_records = bmrs.fetch_range(
        start=start,
        end=end,
    )

    # Inset records
    db_name = os.getenv("POSTGRES_DB")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    conn = psycopg2.connect(
        dbname=db_name, user=db_user, password=db_password, host=db_host
    )

    inserted_rows = 0
    inserted_rows += insert_records(aemo_records, conn)

    inserted_rows += insert_records(bmrs_records, conn)

    conn.close()

    logging.info('Inserted %s rows', inserted_rows)

if __name__ == "__main__":
    run_pipeline()
