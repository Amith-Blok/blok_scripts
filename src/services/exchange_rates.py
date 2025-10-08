import requests
import json
from src.config.logger import logger
from src.config.exchange import FREE_CURRENCY_EXCHANGE_API_KEY

def get_exchange_rates():
    logger.info("Started: get_exchange_rates fn")
    base_url = f"https://api.freecurrencyapi.com/v1/latest?apikey={FREE_CURRENCY_EXCHANGE_API_KEY}&base_currency=USD"
    try:
        response=requests.get(url=base_url)
        data=response.json()
    except Exception as e:
        logger.error(f"Error: {e}")
        return
    logger.info(data)
    logger.info("Started: json writing path data/exchange_rates.json")
    with open("data/exchange_rates.json","w") as f:
        json.dump(data,f)
    logger.info("Finished: json writing path data/exchange_rates.json")
    logger.info("Finished: get_exchange_rates fn")
    return data
