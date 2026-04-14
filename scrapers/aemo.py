import io
import zipfile
import httpx
import pandas as pd
from datetime import date
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

NEMWEB_BASE = "https://nemweb.com.au/Reports/Archive/DispatchIS_Reports"


class AEMOPriceRecord(BaseModel):
    settlement_date: date
    interval_datetime: str      # e.g. "2024/01/01 00:05:00"
    region_id: str              # NSW1, VIC1, QLD1, SA1, TAS1
    rrp: float                  # Regional Reference Price AUD/MWh
    dispatch_interval: int      # 1–288 per day (5-min intervals)


def _date_to_filename(d: date) -> str:
    """NEMWeb archive filename pattern."""
    return f"PUBLIC_DISPATCHIS_{d.strftime('%Y%m%d')}.zip"


def fetch_day(d: date, region: str = "NSW1") -> list[AEMOPriceRecord]:
    """
    Fetch all 5-min dispatch prices for a single date and region.
    Returns up to 288 records (one per 5-min interval).
    """
    url = f"{NEMWEB_BASE}/{_date_to_filename(d)}"

    with httpx.Client(timeout=60) as client:
        response = client.get(url)
        response.raise_for_status()

    # Outer ZIP → inner ZIP → CSV
    outer = zipfile.ZipFile(io.BytesIO(response.content))
    data_rows = []
    for inner_name in outer.namelist():
        inner = zipfile.ZipFile(io.BytesIO(outer.read(inner_name)))
        csv_name = inner.namelist()[0]
        raw_bytes = inner.read(csv_name)

        # Parse MMS CSV — only "D" rows for DISPATCHPRICE table
        lines = raw_bytes.decode("utf-8").splitlines()
        data_rows.extend([l for l in lines if l.startswith("D,DISPATCH,PRICE")])

    if not data_rows:
        logger.warning("No DISPATCHPRICE rows found for %s", d)
        return []

        # MMS column order (from AEMO MMS Data Model):
        # D, DISPATCH, PRICE, <version>, SETTLEMENTDATE, RUNNO, REGIONID,
        # DISPATCHINTERVAL, INTERVENTION, RRP, RAISE6SECRRP, ...
    cols = [
        "row_type", "table_name", "sub_type", "version",
        "SETTLEMENTDATE", "RUNNO", "REGIONID", "DISPATCHINTERVAL",
        "INTERVENTION", "RRP",
    ]

    df = pd.read_csv(
        io.StringIO("\n".join(data_rows)),
        header=None,
        usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        names=cols,
    )

    # Filter: target region, no intervention pricing
    df = df[(df["REGIONID"] == region) & (df["INTERVENTION"] == 0)]

    records = []
    for _, row in df.iterrows():
        try:
            records.append(AEMOPriceRecord(
                settlement_date=d,
                interval_datetime=row["SETTLEMENTDATE"],
                region_id=row["REGIONID"],
                rrp=float(row["RRP"]),
                dispatch_interval=int(row["DISPATCHINTERVAL"]),
            ))
        except Exception as e:
            logger.warning("Skipping malformed row: %s", e)

    return records