import os
import psycopg2
from psycopg2.extras import execute_values


db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
conn = psycopg2.connect(
    dbname=db_name, user=db_user, password=db_password, host=db_host
)


def insert_records(records: list, conn) -> int:
    cur = conn.cursor()
    inserted = 0
    for record in records:
        row = record.to_db_row()
        cur.execute(
            """
            INSERT INTO energy_prices 
                (timestamp_utc, source, region, price, currency, interval_min)
            VALUES 
                (%(timestamp_utc)s, %(source)s, %(region)s, %(price)s, %(currency)s, %(interval_min)s)
            ON CONFLICT DO NOTHING
        """,
            row,
        )
        inserted += cur.rowcount
    conn.commit()
    cur.close()
    return inserted
