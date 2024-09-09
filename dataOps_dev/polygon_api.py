import numpy as np
import requests
from logger import CustomLogger, setup_logger

#####################################################
polygon_api_key = "yHG2uglFVLSopGfOeZ561olwMlY2BA2k"

####################################################

def get_stock_daily_data(symbol: str, date: str):
    """
    :param symbol:  the stock symbol as a string.
    :param date: a date in the format of yyyy-mm-dd
    :return: a json object contains the open,close,high,low prices from the symbol on a specific date
    """
    # create a logger object
    logger = setup_logger()

    query = f'https://api.polygon.io/v1/open-close/AAPL/2024-04-23?adjusted=true&apiKey={polygon_api_key}dfdf'
    response = requests.get(query)

    if response.status_code == 200:
        dat = response.json()
        # extract values from response
        try:
            stock_info = {'symbol': dat['symbol'],
                          'date': dat['from'],
                          'open': dat['open'],
                          'close': dat['close'],
                          'high': dat['high'],
                          'low': dat['low']
                          }
            print(stock_info)
            logger.info(f'API call completed successfully for : {symbol} for date :{date}')
            return stock_info
        except Exception as e:
            logger.error(f'extracting response values has failed for: {symbol} for date: {date} error msg: {e}')
    else:
        logger.error(f'API request had failed for: {symbol} for date: {date}')


if __name__ == '__main__':
    get_stock_daily_data(symbol='AAPL', date='2024-04-26')
