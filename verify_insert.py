import os
import psycopg2
import pandas as pd
from datetime import date
from db.init_db import init_db
from db.insert import insert_records
from scrapers.aemo import fetch_day

init_db()
records = fetch_day(date(2025, 4, 5), region="NSW1")

db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
conn = psycopg2.connect(
    dbname=db_name, user=db_user, password=db_password, host=db_host
)

print(insert_records(records, conn))
conn.close()
