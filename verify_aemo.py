import pandas as pd
from datetime import date
from scrapers.aemo import fetch_day

records = fetch_day(date(2025, 4, 5), region="NSW1")

df = pd.DataFrame([r.model_dump() for r in records])

print(df[['interval_datetime','region_id','rrp']])