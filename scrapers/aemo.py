import io
import zipfile
import httpx
import pandas as pd
from datetime import date
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

NEMWEB_BASE = "https://nemweb.com.au/Reports/Archive/DispatchIS_Reports"

