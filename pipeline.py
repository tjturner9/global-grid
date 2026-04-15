import os
import psycopg2
from datetime import date
from db.init_db import init_db
from db.insert import insert_records
from scrapers import aemo, bmrs
import logging

logging.basicConfig(level=logging.INFO)

# Initialise database schema
init_db()
record_dates = {"start": date(2025, 4, 5), "end": date(2025, 4, 7)}

# Fetch date range from AEMO
aemo_records = aemo.fetch_range(
    start=record_dates["start"],
    end=record_dates["end"],
)

# Fetch date rande from BMRS
bmrs_records = bmrs.fetch_range(
    start=record_dates["start"],
    end=record_dates["end"],
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

print(f"Inserted {inserted_rows} rows")
