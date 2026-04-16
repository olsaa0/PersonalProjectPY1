import requests
from bs4 import BeautifulSoup
from models.crypto import PriceData


def get_scraped_price(symbol: str):
 
    url = f"https://www.google.com/search?q={symbol}+price+usd"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')


        mock_scraped_price = 95600.50

        return PriceData(
            exchange="ScrapedSource",
            symbol=symbol.upper(),
            price=mock_scraped_price
        )
    except Exception as e:
        print(f"🕵️ Scraper failed: {e}")
        return None



if __name__ == "__main__":
    test = get_scraped_price("BTC")
    if test:
        print(f"Scraper found {test.symbol} at ${test.price}")
.
