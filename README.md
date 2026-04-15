# Global Grid — startup guide

## Prerequisites

- Docker Desktop installed and running (Mac/Windows) or Docker pre-installed (GitHub Codespaces)
- Git
- A GitHub account

---

## First time setup

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/global-grid.git
cd global-grid
```

### 2. Create your `.env` file

The `.env` file is not committed to the repo. Create it from scratch:

```bash
cat > .env << 'EOF'
POSTGRES_USER=griduser
POSTGRES_PASSWORD=changeme
POSTGRES_DB=globalgrid
POSTGRES_HOST=postgres
AEMO_BASE_URL=https://nemweb.com.au/Reports/Archive/DispatchIS_Reports
BMRS_BASE_URL=https://data.elexon.co.uk/bmrs/api/v1
EOF
```

### 3. Boot the stack

```bash
docker compose up --build -d
```

Verify Postgres is healthy:

```bash
docker compose ps
```

The `STATUS` column for postgres should show `healthy` before proceeding.

### 4. Initialise the database schema

```bash
docker compose run --rm scraper python db/init_db.py
```

Verify the table and indexes exist:

```bash
docker compose exec postgres psql -U griduser -d globalgrid -c "\d energy_prices"
```

You should see:

```
Indexes:
    "energy_prices_pkey" PRIMARY KEY, btree (id)
    "idx_energy_prices_timestamp" btree (timestamp_utc)
    "idx_energy_prices_unique" UNIQUE, btree (timestamp_utc, source, region)
```

---

## Running the pipeline

Fetch and persist data from both AEMO and BMRS:

```bash
docker compose run --rm scraper python pipeline.py
```

Verify row counts in the database:

```bash
docker compose exec postgres psql -U griduser -d globalgrid -c "SELECT source, COUNT(*) FROM energy_prices GROUP BY source;"
```

---

## Running tests

```bash
docker compose run --rm scraper pytest tests/ -v
```

---

## Verify scripts

Individual scraper verification — useful for testing a single source without running the full pipeline:

```bash
# BMRS — fetches one day, prints 48 rows
docker compose run --rm scraper python verify_bmrs.py

# AEMO — fetches one day, prints 288 rows
docker compose run --rm scraper python verify_aemo.py

# Insert — fetches one day of AEMO data and inserts into Postgres
docker compose run --rm scraper python verify_insert.py
```

---

## Connecting to the database directly

```bash
docker compose exec postgres psql -U griduser -d globalgrid
```

Useful queries:

```sql
-- Row counts by source
SELECT source, COUNT(*) FROM energy_prices GROUP BY source;

-- Latest timestamp per source
SELECT source, MAX(timestamp_utc) FROM energy_prices GROUP BY source;

-- Sample AEMO data with local time
SELECT source, timestamp_utc, timestamp_utc AT TIME ZONE 'Australia/Brisbane' AS local_time
FROM energy_prices
WHERE source = 'AEMO'
ORDER BY timestamp_utc
LIMIT 10;

-- Sample BMRS data with local time
SELECT source, timestamp_utc, timestamp_utc AT TIME ZONE 'Europe/London' AS local_time
FROM energy_prices
WHERE source = 'BMRS'
ORDER BY timestamp_utc
LIMIT 10;
```

---

## Stopping the stack

```bash
docker compose down
```

To also wipe the database volume (forces reinitialisation on next boot):

```bash
docker compose down -v
```

> ⚠️ Use `-v` with caution — it deletes all persisted data. Always required when changing Postgres environment variables or modifying `schema.sql`.

---

## GitHub Codespaces

Docker comes pre-installed in Codespaces. After opening the repo in a codespace:

1. Create the `.env` file using the command in step 2 above
2. Follow steps 3–4 as normal

The `.env` file will need to be recreated each time you open a new codespace as it is not committed to the repo.

---

## Common errors and fixes

| Error | Cause | Fix |
|---|---|---|
| `command not found: docker` | Docker Desktop not running | Open Docker Desktop and wait for the whale icon to stop animating |
| `database "griduser" does not exist` | Healthcheck missing `-d` flag or stale volume | Check `pg_isready -U griduser -d globalgrid` in healthcheck; run `docker compose down -v` |
| Changes to `.env` not taking effect | Stale Docker volume from previous boot | `docker compose down -v && docker compose up --build` |
| `404 Not Found` on AEMO | Date outside available archive range | NEMWeb only holds ~12 months of data; use dates from April 2025 onwards |
| `psycopg2 socket error` | `POSTGRES_HOST` missing from `.env` | Add `POSTGRES_HOST=postgres` to `.env` |
| YAML parse error in docker-compose | Tabs or inconsistent indentation | Use 2 spaces throughout, never tabs |