from fastapi import APIRouter
from services.crypto_api import get_binance_price
from crypto_scraper import get_scraped_price
from models.crypto import ArbitrageResult
from database import save_history

router = APIRouter()


@router.get("/compare/{symbol}", response_model=ArbitrageResult)
def compare_prices(symbol: str, threshold: float = 0.5):

    api_data = get_binance_price(symbol)
    scraped_data = get_scraped_price(symbol)

    if not api_data or not scraped_data:
        return {"error": "Could not fetch data from one of the sources"}


    diff = scraped_data.price - api_data.price
    spread = (diff / api_data.price) * 100


    is_profitable = spread >= threshold


    save_history(symbol, api_data.price, scraped_data.price, spread)


    return ArbitrageResult(
        symbol=symbol.upper(),
        api_price=api_data.price,
        scraped_price=scraped_data.price,
        spread_percentage=round(spread, 4),
        is_profitable=is_profitable,
        alert_threshold=threshold
    )
.
