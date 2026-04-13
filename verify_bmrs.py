import pandas as pd
from datetime import date
from scrapers.bmrs import fetch_range

records = fetch_range(
    start=date(2024, 1, 1),
    end=date(2024, 1, 7),
)

df = pd.DataFrame([r.model_dump() for r in records])

# Build a proper UTC timestamp from date + period
# Each period is 30 min; period 1 starts at 00:00 UTC
df["timestamp_utc"] = pd.to_datetime(df["settlement_date"]) + pd.to_timedelta(
    (df["settlement_period"] - 1) * 30, unit="min"
)

df = df.sort_values("timestamp_utc").reset_index(drop=True)
print(df[["timestamp_utc", "settlement_period", "system_sell_price"]].head(10))