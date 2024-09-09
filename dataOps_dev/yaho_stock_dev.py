from datetime import time, datetime
import yfinance as yf
from sqlalchemy.exc import RemovedIn20Warning
from GCP_SETUP.gcp_setup import get_pool
import warnings
from sqlalchemy import MetaData, Table, Column, String, text

stock_list = [
    {'index': '^TA125.TA', 'name': 'Tel Aviv 125'},
    {'index': 'PSG-F14.TA', 'name': 'Tel Aviv Bonds 60'},
    {'index': 'BKHYY', 'name': 'bank Hapoalim'},
    {'index': 'ESLT', 'name': 'Elbit'}
]
table_configs = {
    'stocks': {'raw_data': 'stocks.yfinance_stock_data'},
    'server': {'users': 'server.users', 'actions': 'server.raw_actions'}
}


def indices_EoD_by_index_from_date_to_date(index_id: str, start_date: time, end_date: time,
                                           stock_name: str = None, insert: bool = False):
    """
    Retrieves End of Day (EoD) data for a specified stock index within a given date range from the yfinance API.
    param index_id: (str) The ID of the stock index for which EoD data is to be retrieved.
    param start_date: (time) The start date of the date range for which EoD data is to be retrieved.
    param end_date: (time) The end date of the date range for which EoD data is to be retrieved.
    param stock_name: (str, optional) The name of the stock. If not provided, the function will attempt to find it based on the `index_id`.
    param insert: (bool, default=False) If `True`, the retrieved data will be inserted into a database table.
    return: DataFrame: A Pandas DataFrame containing the retrieved EoD data.
    """
    try:
        stock_ticker = yf.Ticker(stock['index'])
        stock_data = stock_ticker.history(start=start_date, end=end_date, interval="1d").reset_index()[
            ['Date', 'Open', 'High',
             'Low', 'Close',
             'Volume']]
        if stock_data.empty:
            raise ValueError('respond from  yf.Ticker is empty')
        stock_data.columns = stock_data.columns.str.lower()
        if stock_name is None:
            symbol_name = next((stock['name'] for stock in stock_list if stock['index'] == index_id), None)
            if symbol_name is None:
                raise ValueError("symbol_name was not provided and was not found in stock list,operation can't be done")
        else:
            symbol_name = stock_name
        stock_data['index_symbol'] = index_id
        stock_data['symbol_name'] = symbol_name
        if insert:
            # create delete query
            conditions = " OR ".join(
                [f"(index_symbol = '{row['index_symbol']}' AND date = '{row['date']}')" for index, row in
                 stock_data.iterrows()])
            delete_query = f"DELETE FROM {table_configs['stocks']['raw_data']} WHERE {conditions}"

            # create insert quesry
            insert_values = ", ".join([
                f"('{row['index_symbol']}', '{row['symbol_name']}', '{row['date']}', {row['open']}, {row['close']}, {row['high']}, {row['low']}, {row['volume']})"
                for index, row in stock_data.iterrows()])
            insert_query = f"INSERT INTO {table_configs['stocks']['raw_data']} (index_symbol, symbol_name, date, open, close, high, low, volume) VALUES {insert_values}"

            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    print(delete_query)
                    conn.execute(text(delete_query))
                    conn.commit()
                    print(insert_query)
                    conn.execute(text(insert_query))
                    conn.commit()
        return stock_data

    except Exception as e:
        print(f"error: {e}")


if __name__ == '__main__':
    for stock in stock_list:
        print(f"---info for stock: {stock['name']}")
        df = indices_EoD_by_index_from_date_to_date(index_id=stock['index'],
                                                    start_date='2024-05-01',
                                                    end_date=datetime.now().strftime('%Y-%m-%d'),
                                                    insert=True
                                                    )
        print(df.head(10000))

    # for stock in stock_list:
    #     print(f"---info for stock: {stock['name']}")
    #     stock_ticker = yf.Ticker(stock['index'])
    #     stock_history = stock_ticker.history(start="2024-05-01", end="2024-05-20", interval="1d").reset_index()[
    #         ['Date', 'Open', 'High',
    #          'Low', 'Close',
    #          'Volume']]
    #     stock_history.columns = stock_history.columns.str.lower()
    #     print(stock_history.head(1000))
    #     print(stock_history.columns)
