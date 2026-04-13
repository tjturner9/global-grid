import httpx
from datetime import date, timedelta
from pydantic import BaseModel, field_validator
from typing import Generator
import logging

logger = logging.getLogger(__name__)

BMRS_BASE = "https://data.elexon.co.uk/bmrs/api/v1"


class BMRSPriceRecord(BaseModel):
    settlement_date: date
    settlement_period: int          # 1–48
    system_sell_price: float        # £/MWh
    system_buy_price: float         # £/MWh
    net_imbalance_volume: float     # MWh

    @field_validator("settlement_period")
    @classmethod
    def valid_period(cls, v: int) -> int:
        if not (1 <= v <= 50):
            raise ValueError(f"Unexpected settlement period: {v}")
        return v


def fetch_day(settlement_date: date, client: httpx.Client) -> list[BMRSPriceRecord]:
    """Fetch all settlement periods for a single date."""
    url = f"{BMRS_BASE}/balancing/settlement/system-prices/{settlement_date}"
    response = client.get(url, timeout=30)
    response.raise_for_status()

    raw = response.json().get("data", [])

    records = []
    for row in raw:
        try:
            records.append(BMRSPriceRecord(
                settlement_date=row["settlementDate"],
                settlement_period=row["settlementPeriod"],
                system_sell_price=row["systemSellPrice"],
                system_buy_price=row["systemBuyPrice"],
                net_imbalance_volume=row["netImbalanceVolume"],
            ))
        except Exception as e:
            logger.warning("Skipping malformed row %s: %s", row, e)

    return records


def date_range(start: date, end: date) -> Generator[date, None, None]:
    """Yields each date from start up to and including end."""
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def fetch_range(start: date, end: date) -> list[BMRSPriceRecord]:
    """Fetch all settlement periods across a date range."""
    all_records: list[BMRSPriceRecord] = []

    with httpx.Client(base_url=BMRS_BASE) as client:
        for day in date_range(start, end):
            logger.info("Fetching BMRS %s", day)
            try:
                records = fetch_day(day, client)
                all_records.extend(records)
                logger.info("  → %d periods", len(records))
            except httpx.HTTPStatusError as e:
                logger.error("HTTP error for %s: %s", day, e)
            except httpx.RequestError as e:
                logger.error("Network error for %s: %s", day, e)

    return all_records