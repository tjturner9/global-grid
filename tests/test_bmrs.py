# tests/test_bmrs.py
import pytest
from datetime import date
from scrapers.bmrs import fetch_range, BMRSPriceRecord

def test_fetch_single_day():
    records = fetch_range(date(2024, 6, 1), date(2024, 6, 1))
    assert len(records) == 48         # expect full day
    assert all(isinstance(r, BMRSPriceRecord) for r in records)
    assert all(r.system_sell_price > 0 for r in records)