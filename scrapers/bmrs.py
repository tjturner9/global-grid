import httpx
from datetime import date, timedelta
from pydantic import BaseModel, field_validator
from typing import Generator
import logging

logger = logging.getLogger(__name__)

BMRS_BASE = "https://data.elexon.co.uk/bmrs/api/v1"

