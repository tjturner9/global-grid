import os
import psycopg2


def init_db() -> None:

    db_name = os.getenv("POSTGRES_DB")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    conn = psycopg2.connect(
        dbname=db_name, 
        user=db_user, 
        password=db_password, 
        host=db_host
    )

    cur = conn.cursor()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, "schema.sql")
    with open(schema_path, "r") as file:
        sql_script = file.read()

    cur.execute(sql_script)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    init_db()
