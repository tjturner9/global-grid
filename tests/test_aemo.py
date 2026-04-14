from datetime import date
from scrapers.aemo import fetch_day


def test_fetch_single_day():
    records = fetch_day(date(2025, 4, 5), region="NSW1")
    assert len(records) == 288  # 288 5-min intervals in a day
    assert all(r.region_id == "NSW1" for r in records)
    # Spot price should be plausible for NEM (not negative floor, not at cap)
    prices = [r.rrp for r in records]
    assert min(prices) > -1000
    assert max(prices) < 17_000  # AUD/MWh market price cap
