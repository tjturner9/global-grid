CREATE TABLE IF NOT EXISTS energy_prices (
    id SERIAL PRIMARY KEY,
    timestamp_utc TIMESTAMPTZ NOT NULL,
    source VARCHAR(20) NOT NULL,
    region VARCHAR(20) NOT NULL,
    price NUMERIC(10,5) NOT NULL,
    currency VARCHAR(20) NOT NULL,
    interval_min INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_energy_prices_timestamp
ON energy_prices (timestamp_utc);