from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PriceData(BaseModel):
    exchange: str
    symbol: str
    price: float
    timestamp: datetime = datetime.now()


class ArbitrageResult(BaseModel):
    symbol: str
    api_price: float
    scraped_price: float
    spread_percentage: float
    is_profitable: bool
    alert_threshold: float
