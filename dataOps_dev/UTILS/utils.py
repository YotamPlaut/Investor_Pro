import json
from sqlalchemy.exc import RemovedIn20Warning
from datetime import time, datetime
from sqlalchemy import text
import pandas as pd
import warnings
import sqlalchemy
import pg8000
import http.client
import os

table_configs = {
    'stocks': {'raw_data': 'stocks.tase_stock_data',
               'stats': 'stocks.tase_stock_stats',
               'info': 'stocks.tase_stock_info',
               'predictions': 'stocks.tase_stock_predictions',
               },
    'server': {'users': 'server.users', 'actions': 'server.raw_actions', 'portfolio': 'server.portfolios'}
}
stock_list = [
    {'index_id': 137, 'name': 'TA-125 Index', 'IsIndex': True},
    {'index_id': 147, 'name': 'TA-SME 60 Index', 'IsIndex': True},
    {'index_id': 709, 'name': 'TA-Bond 60 Index', 'IsIndex': True},
    {'index_id': 662577, 'name': 'Bank Hapoalim', 'IsIndex': False},
    {'index_id': 691212, 'name': 'Bank Discount', 'IsIndex': False},
]


#################### DB ACCESS FUNCTIONS ####################
def getconn() -> pg8000.Connection:
    """
    Establishes and returns a connection to the PostgreSQL database using pg8000.

    This function connects to the PostgreSQL database using credentials and configuration details
    obtained from environment variables. The connection is established using the `pg8000` library.

    Returns:
        pg8000.Connection: A connection object to the PostgreSQL database.

    """
    conn: pg8000.Connection = pg8000.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST'),
    )
    return conn


def get_pool():
    """
    Creates and returns a SQLAlchemy engine for connecting to a PostgreSQL database using pg8000.

    This function sets up a SQLAlchemy engine configured to connect to a PostgreSQL database. The engine
    is created using the `pg8000` library as the database driver. Connection details are obtained from
    environment variables.

    Returns:
        sqlalchemy.engine.Engine: A SQLAlchemy engine instance configured for PostgreSQL.

    """
    pool = sqlalchemy.create_engine(
        f"postgresql+pg8000://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}",
        creator=getconn,
        future=True
        # Additional options if needed
    )
    return pool


#################### TASE API FUNCTIONS ####################
def get_Bar():
    """
    Retrieves an OAuth 2.0 access token from the Tel Aviv Stock Exchange (TASE) API.

    This function establishes an HTTPS connection to the TASE API and sends a POST
    request to the authentication endpoint using client credentials to obtain an
    access token. The token is required for making authenticated requests to the TASE API.

    Returns:
        str: The access token necessary for authenticated API requests.


    """

    conn = http.client.HTTPSConnection("openapigw.tase.co.il")
    payload = 'grant_type=client_credentials&scope=tase'
    headers = {
        'Authorization': 'Basic ZWNiY2VlODk0YTkxZDQ3YTMwY2ZjYTU1NjA3NjkyODg6NGU0MThmNTYxNmM4ZjMwZjBkMjM0MjBkMzFlOGM2NzA=',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    conn.request("POST", "/tase/prod/oauth/oauth2/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_dict = json.loads(data)
    return json_dict['access_token']


def indices_EoD_by_index_from_date_to_date(bearer: str,
                                           index_id: int,
                                           start_date: time,
                                           end_date: time,
                                           stock_name: str = None,
                                           insert: bool = False,):
    """
    Retrieves End of Day (EoD) data for a specified stock index -for Index stocks (TA_125...) within a given date range from the Tel Aviv Stock Exchange (TASE) API.

    param bearer: (str) The bearer token for authentication with the TASE API.
    param index_id: (int) The ID of the stock index for which EoD data is to be retrieved.
    param start_date: (time) The start date of the date range for which EoD data is to be retrieved.
    param end_date: (time) The end date of the date range for which EoD data is to be retrieved.
    param stock_name: (str, optional) The name of the stock. If not provided, the function will attempt to find it based on the `index_id`.
    param insert: (bool, default=False) If `True`, the retrieved data will be inserted into a database table.
    return: DataFrame: A Pandas DataFrame containing the retrieved EoD data.

    """

    conn = http.client.HTTPSConnection("openapigw.tase.co.il")

    headers = {
        'Authorization': f"Bearer {bearer}",
        'accept': "application/json"
    }
    conn.request("GET",
                 f"/tase/prod/api/v1/indices/eod/history/ten-years/by-index?indexId={index_id}&fromDate={start_date}&toDate={end_date}",
                 headers=headers)
    res = conn.getresponse()
    data = res.read()
    try:
        dat = json.loads(data)
        if stock_name is None:
            symbol_name = next((stock['name'] for stock in stock_list if stock['index_id'] == int(index_id)), None)
            if symbol_name is None:
                raise ValueError("symbol_name was not provided and was not found in stock list,operation can't be done")
        else:
            symbol_name = stock_name
        df = pd.DataFrame(dat['indexEndOfDay']['result'])
        df['symbol_name'] = symbol_name
        df = df.rename(columns={
            'indexId': 'index_symbol',
            'tradeDate': 'date',
            'indexOpeningPrice': 'open',
            'closingIndexPrice': 'close',
            'high': 'high',
            'low': 'low',
            'overallMarketCap': 'omc'
        })

        # Reorder columns
        df = df[['index_symbol', 'symbol_name', 'date', 'open', 'close', 'high', 'low', 'omc']]
        if insert:
            # create delete query
            conditions = " OR ".join(
                [f"(index_symbol = '{row['index_symbol']}' AND date = '{row['date']}')" for index, row in
                 df.iterrows()])
            delete_query = f"DELETE FROM {table_configs['stocks']['raw_data']} WHERE {conditions}"

            # create insert query
            insert_values = ", ".join([
                f"('{row['index_symbol']}', '{row['symbol_name']}', '{row['date']}', {row['open']}, {row['close']}, {row['high']}, {row['low']}, {row['omc']})"
                for index, row in df.iterrows()])
            insert_query = f"INSERT INTO {table_configs['stocks']['raw_data']} (index_symbol, symbol_name, date, open, close, high, low, omc) VALUES {insert_values}"

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
        return df

        # print(dat['indexEndOfDay']['result'])
    except Exception as e:
        print(f"error: {e}")


def securities_EoD_by_index_from_date_to_date(bearer: str,
                                              index_id: int,
                                              start_date: time,
                                              end_date: time,
                                              stock_name: str = None,
                                              insert: bool = False,):
    """
    Retrieves End of Day (EoD) data for a specified stock index -for actual stocks (bank_hapoim.....) within a given date range from the Tel Aviv Stock Exchange (TASE) API.

    param bearer: (str) The bearer token for authentication with the TASE API.
    param index_id: (int) The ID of the stock index for which EoD data is to be retrieved.
    param start_date: (time) The start date of the date range for which EoD data is to be retrieved.
    param end_date: (time) The end date of the date range for which EoD data is to be retrieved.
    param stock_name: (str, optional) The name of the stock. If not provided, the function will attempt to find it based on the `index_id`.
    param insert: (bool, default=False) If `True`, the retrieved data will be inserted into a database table.
    return: DataFrame: A Pandas DataFrame containing the retrieved EoD data.

    """
    import http.client

    conn = http.client.HTTPSConnection("openapigw.tase.co.il")

    headers = {
        'Authorization': f"Bearer {bearer}",
        'accept': "application/json"
    }

    conn.request("GET",
                 f"/tase/prod/api/v1/securities/trading/eod/history/ten-years/by-security?securityId={index_id}&fromDate={start_date}&toDate={end_date}",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    try:
        dat = json.loads(data)
        if stock_name is None:
            symbol_name = next((stock['name'] for stock in stock_list if stock['index_id'] == int(index_id)), None)
            if symbol_name is None:
                raise ValueError("symbol_name was not provided and was not found in stock list,operation can't be done")
        else:
            symbol_name = stock_name
        df = pd.DataFrame(dat['securitiesEndOfDayTradingData']['result'])
        df['symbol_name'] = symbol_name
        df = df.rename(columns={
            'securityId': 'index_symbol',
            'tradeDate': 'date',
            'openingPrice': 'open',
            'closingPrice': 'close',
            'high': 'high',
            'low': 'low',
            'marketCap': 'omc',
            'volume': 'volume'
        })
        df = df[['index_symbol', 'symbol_name', 'date', 'open', 'close', 'high', 'low', 'omc', 'volume']]
        if insert:
            # create delete query
            conditions = " OR ".join(
                [f"(index_symbol = '{row['index_symbol']}' AND date = '{row['date']}')" for index, row in
                 df.iterrows()])
            delete_query = f"DELETE FROM {table_configs['stocks']['raw_data']} WHERE {conditions}"

            # create insert query
            insert_values = ", ".join([
                f"('{row['index_symbol']}', '{row['symbol_name']}', '{row['date']}', {row['open']}, {row['close']}, {row['high']}, {row['low']}, {row['omc']}, {row['volume']})"
                for index, row in df.iterrows()])
            insert_query = f"INSERT INTO {table_configs['stocks']['raw_data']} (index_symbol, symbol_name, date, open, close, high, low, omc,volume ) VALUES {insert_values}"

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
        return df
    except Exception as e:
        pass


###################################################################


##################### STOCKS INFO FUNCTIONS #########################
def get_matching_stock_name_index(stock_name: str = None, stock_index: int = None):
    """
        Retrieves the corresponding stock index or stock name from the stock list.

        This function checks if either `stock_name` or `stock_index` is provided.
        If a `stock_name` is provided, it returns the corresponding stock index.
        If a `stock_index` is provided, it returns the corresponding stock name.
        If both are None, the function prints an error message and returns None.

        Args:
            stock_name (str, optional): The name of the stock for which to find the index. Defaults to None.
            stock_index (int, optional): The index of the stock for which to find the name. Defaults to None.

        Returns:
            int or str: The corresponding stock index if `stock_name` is provided, or the corresponding
            stock name if `stock_index` is provided. Returns None if neither argument is provided, or
            if no matching stock is found.

        Raises:
            ValueError: If both `stock_name` and `stock_index` are None.
    """

    if (stock_name is None) and (stock_index is None):
        raise ValueError("both stock_name and stock_index are null")
    if stock_name is not None:
        matching_stock_index = next(
            (stock['index_id'] for stock in stock_list if stock['name'] == stock_name),
            None)
        return matching_stock_index
    if stock_index is not None:
        matching_stock_name = next(
            (stock['name'] for stock in stock_list if stock['index_id'] == stock_index),
            None)
        return matching_stock_name


def get_matching_is_index(stock_name: str = None, stock_index: int = None):
    """
      Retrieves whether the stock is an index based on the provided stock name or stock index.

      This function checks if either `stock_name` or `stock_index` is provided.
      If a `stock_name` is provided, it returns the corresponding `IsIndex` value from the stock list.
      If a `stock_index` is provided, it returns the corresponding `is_index` value from the stock list.
      If both are None, the function prints an error message and returns None.

      Args:
          stock_name (str, optional): The name of the stock for which to find the `IsIndex` value. Defaults to None.
          stock_index (int, optional): The index of the stock for which to find the `is_index` value. Defaults to None.

      Returns:
          bool: The `IsIndex` or `is_index` value indicating whether the stock is an index.
          Returns None if neither argument is provided or if no matching stock is found.
        """
    if (stock_name is None) and (stock_index is None):
        raise ValueError("both stock_name and stock_index are null")
    if stock_name is not None:
        is_index = next(
            (stock['IsIndex'] for stock in stock_list if stock['name'] == stock_name),
            None)
        return is_index
    if stock_index is not None:
        is_index = next(
            (stock['is_index'] for stock in stock_list if stock['index_id'] == stock_index),
            None)
        return is_index


#####################################################################


#####################  DB STOCKS  FUNCTIONS #####################
def get_stock_data_by_date(stock_name: str, date: time):
    """
     Fetches stock data for a given stock name starting from a specific date.
    param stock_name: The name of the stock, which must be present in the stock_list.
    param date: The start date for fetching the stock records, in the format of yyyy-mm-dd.
    return: A JSON string containing:
             - 'info': A dictionary where keys are dates and values are dictionaries of stock data (fields: Index_Symbol, Symbol_Name, Open, Close, High, Low, OMC, Volume).
             - 'num_days': The number of unique dates in the data.
             - 'Index_Symbol': The index symbol of the stock.
             - 'Symbol_Name': The name of the stock.
             If an error occurs, None is returned.
    """
    matching_stock_index = get_matching_stock_name_index(stock_name=stock_name)
    # matching_stock_index = next(
    #     (stock['index_id'] for stock in stock_list if stock['name'] == stock_name),
    #     None)
    if matching_stock_index is None:
        print(f"didn't found matching index for stock: {stock_name}")
        return None
    try:
        engine = get_pool()
        query = f"""
                 select 
                    date,
                    a.index_symbol,
                    a.symbol_name,
                    open,
                    close,
                    high,
                    low,
                    omc,
                    volume,
                    b.description
                from {table_configs['stocks']['raw_data']} a left join {table_configs['stocks']['info']} b 
                on a.index_symbol=b.index_symbol
                where a.index_symbol='{matching_stock_index}' and date>=date('{date}');
          """
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            stock_data_dict = {'price_data': []}
            for row in result:
                stock_data_dict['price_data'].append(
                    {
                        'date': row['date'].strftime('%Y-%m-%d'),
                        'close_price': row[4]
                    }
                )
            num_days = len(stock_data_dict['price_data'])
            stock_data_dict['num_days'] = num_days
            stock_data_dict['Index_Symbol'] = matching_stock_index
            stock_data_dict['Symbol_Name'] = stock_name
            stock_data_dict['description'] = stock_name
            stock_data_dict['description'] = result[0][9]
            # date_str = row['date'].strftime('%Y-%m-%d')  # Ensure date is in string format for JSON compatibility
            # stock_data_dict['price_data'][row[0].strftime('%Y-%m-%d')] = {
            # 'Index_Symbol': row[1],
            # 'Symbol_Name': row[2],
            # 'Open': row[3],
            # 'Close': row[4],
            # 'High': row[5],
            # 'Low': row[6],
            # 'OMC': row[7],
            # 'Volume': row[8]
            # }
            # Add the number of unique dates to the JSON object

            # Convert dictionary to JSON
            stock_data_json = json.dumps(stock_data_dict)
            return stock_data_json
    except Exception as e:
        print(f"error occurred while running query: {e}")
        return None


def get_all_stocks():
    """
    Retrieves all distinct stocks from the database.
    :return: A JSON string representing a dictionary where each key is the 'index_symbol'
             and the corresponding value is the 'symbol_name'. Returns None if no stocks
             are found or if an error occurs.
    """
    select_query = (
        f"""
    select
        index_symbol,
        symbol_name,
        description 
    from {table_configs['stocks']['info']}
                """
    )
    try:
        engine = get_pool()
        with engine.connect() as conn:
            result = conn.execute(text(select_query)).fetchall()

            all_stock = [{'index_symbol': stock[0],
                          'symbol_name': stock[1],
                          'description': stock[2]
                          } for stock in result]
            # all_stock = {f'{stock[0]}': stock[1] for stock in result}
            return json.dumps(all_stock)
    except Exception as e:
        print(f"error occurred while running query: {e}")
        return None


def get_last_update_stock_stats_by_stats_name(stock_name: str, stats_name: str):
    """
    Retrieves the most recent stock statistics for a given stock and statistics name.

    This function fetches the latest stock statistics for a specific stock based on the
    provided `stock_name` and `stats_name`. It queries a database table and returns
    the result as a JSON object containing the relevant stock data. If no matching
    stock index is found, or if an error occurs during the query, the function will
    return None.

    Args:
        stock_name (str): The name of the stock for which to retrieve the statistics.
        stats_name (str): The name of the statistics to retrieve (e.g., price, volume).

    Returns:
        str: A JSON string containing the stock statistics (e.g., `Stats_Name`,
        `Index_Symbol`, `Symbol_Name`, `Stats_Info`, `Insert_Time`), or None if no
        matching data is found or an error occurs.
    """
    matching_stock_index = get_matching_stock_name_index(stock_name=stock_name)
    if matching_stock_index is None:
        print(f"didn't found matching index for stock: {stock_name}")
        return None
    try:
        engine = get_pool()
        query = f"""
                 select 
                    stats_name,
                    index_symbol,
                    symbol_name,
                    stats_info,
                    insert_time 
            FROM
                {table_configs['stocks']['stats']}
                where  stats_name='{stats_name}' and index_symbol={matching_stock_index}
                order by insert_time desc limit 1
          """
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            stats_data = result[0]

            stock_data_dict = {
                'Stats_Name': stats_data[0],
                'Index_Symbol': stats_data[1],
                'Symbol_Name': stats_data[2],
                'Stats_Info': stats_data[3],
                'Insert_Time': stats_data[4].strftime('%Y-%m-%d'),
            }
            stock_data_dict = json.dumps(stock_data_dict)
            return stock_data_dict
    except Exception as e:
        print(f"error occurred while running query: {e}")
        return None


def get_all_last_update_stock_stats(stock_name: str):
    """
    Retrieves the most recent statistics for a given stock based on its name.

    This function fetches the latest available statistics for a specified stock by querying the
    database. It retrieves the most recent `stats_info` and `insert_time` for each statistic type
    (e.g., price, volume) related to the stock. The result is returned as a JSON object containing
    the relevant stock statistics.

    Args:
        stock_name (str): The name of the stock for which to retrieve the statistics.

    Returns:
        str: A JSON string containing the stock's statistics, including:
             - `stats_info`: The information related to each statistic.
             - `insert_time`: The time the statistics were last updated.
             - `Index_Symbol`: The stock's index symbol.
             - `symbol_name`: The name of the stock.
        Returns None if no matching data is found or an error occurs.

    """
    matching_stock_index = get_matching_stock_name_index(stock_name=stock_name)
    if matching_stock_index is None:
        print(f"didn't found matching index for stock: {stock_name}")
        return None
    try:
        engine = get_pool()
        query = f"""
        with max_dates as(
                        select 
                            stats_name,
                            max(insert_time) as max_insert_time
                            from  {table_configs['stocks']['stats']}
                            where index_symbol={matching_stock_index}
                            group by 1
                        )
            select 
                a.stats_name,
                a.stats_info,
                a.insert_time,
                a.index_symbol,
                a.symbol_name
            from  {table_configs['stocks']['stats']} a inner join max_dates b 
            on a.stats_name=b.stats_name
            where 
                a.index_symbol={matching_stock_index}
                and b.max_insert_time=a.insert_time;
               """
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            stock_stats_dict = {}
            for row in result:
                # date_str = row['date'].strftime('%Y-%m-%d')  # Ensure date is in string format for JSON compatibility
                stock_stats_dict[row[0]] = {
                    'stats_info': row[1],
                    'insert_time': row[2].strftime('%Y-%m-%d')
                }
            stock_stats_dict['Index_Symbol'] = result[0][3]
            stock_stats_dict['symbol_name'] = result[0][4]
            stock_stats_dict = json.dumps(stock_stats_dict)
            return stock_stats_dict

    except Exception as e:
        print(f"error occurred while running query: {e}")
        return None


def get_last_update_stock_prediction(stock_name: str):
    """
    Retrieves the most recent stock price predictions for a given stock based on its name.

    This function fetches the latest stock price predictions from the database for the specified
    stock. It retrieves the most recent prediction data, including the stock's index symbol,
    name, and predicted closing prices for future dates. The result is returned as a JSON object.

    Args:
        stock_name (str): The name of the stock for which to retrieve the predictions.

    Returns:
        str: A JSON string containing the stock prediction data, including:
             - `Index_Symbol`: The stock's index symbol.
             - `Symbol_Name`: The stock's name.
             - `close_predictions_data`: A list of dictionaries containing the predicted closing
               prices and their corresponding dates.
        Returns None if no matching data is found or an error occurs.

    """
    matching_stock_index = get_matching_stock_name_index(stock_name=stock_name)
    if matching_stock_index is None:
        print(f"didn't found matching index for stock: {stock_name}")
        return None
    try:
        engine = get_pool()
        query = f"""
                select 
                    index_symbol,
                    symbol_name,
                    predictions
                from {table_configs['stocks']['predictions']}
                where index_symbol='{matching_stock_index}'
                order by insert_time desc limit 1
            """
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            stock_predict_results = {}
            for row in result:
                stock_predict_results['Index_Symbol'] = row[0]
                stock_predict_results['Symbol_Name'] = row[1]
                stock_predict_results['close_predictions_data'] = [{'date': date, 'pred': price}
                                                                   for date, price in row[2].items()]
            return json.dumps(stock_predict_results)
    except Exception as e:
        print(f"error occurred while running query: {e}")
        return None


#####################################################################


#####################  DB SERVER  FUNCTIONS #####################
def check_if_user_exists(user_name: str, email: str):
    """
    Check if a user exists in the database based on their username or email.

    param user_name: The username to check.
    param email: The email address to check.
    return: A dictionary containing a code and a message.
        - code (int): 0 if the user or email is found in the database, 1 otherwise.
        - msg (str): A message indicating whether the user or email is found in the database or not.
    """
    engine = get_pool()
    with engine.connect() as conn:
        result = conn.execute(
            text(
                f"SELECT distinct user_id,email_address FROM {table_configs['server']['users']}"))  # Use conn.execute instead of engine.execute
        df = pd.DataFrame(result, columns=['user_id', 'email_address'])
        if user_name in df['user_id'].values:
            return {'code': 0, 'msg': 'user found in db'}
        if email in df['email_address'].values:
            return {'code': 0, 'msg': 'email_address found in db'}
        return {'code': 1, 'msg': 'user and email not found in db'}


def insert_new_portfolio(user_id: str, portfolio_id: str, stock_array: {} = None):
    """
    Inserts a new portfolio entry into the database for a specified user.

    This function inserts a new record into the `portfolio` table in the database, including
    the user ID, portfolio ID, and an array of stocks. The insertion is performed using an
    SQL `INSERT` statement.

    Args:
        user_id (str): The ID of the user for whom the portfolio is being inserted.
        portfolio_id (str): The ID of the portfolio to be inserted.
        stock_array (dict): A string representation of the array of stocks to be included in the portfolio.

    Returns:
        dict: A dictionary with the following keys:
            - 'code': An integer status code (1 for success).
            - 'msg': A message indicating the result of the operation.
        Returns None if an error occurs during the insertion.



    """
    try:
        insert_query = (
            f"""
                                   INSERT INTO {table_configs['server']['portfolio']} (user_id,
                                                                  portfolio_id,
                                                                  stock_array
                                                                  )
                                   VALUES ('{user_id}','{portfolio_id}','{stock_array}')
                                   """
        )
        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                conn.execute(text(insert_query))
                conn.commit()
            return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was inserted to db"}
    except Exception as e:
        print(f"error occurred while running insert query: {e} ")
        return None


def remove_portfolio(user_id: str, portfolio_id: str):
    """
    Deletes a portfolio entry from the database for a specified user.

    This function removes a record from the `portfolio` table in the database based on the
    provided user ID and portfolio ID. The deletion is performed using an SQL `DELETE` statement.

    Args:
        user_id (str): The ID of the user for whom the portfolio is being removed.
        portfolio_id (str): The ID of the portfolio to be deleted.

    Returns:
        dict: A dictionary with the following keys:
            - 'code': An integer status code (1 for success).
            - 'msg': A message indicating the result of the operation.
        Returns None if an error occurs during the deletion.
    """
    try:
        delete_query = (
            f"""
                DELETE FROM {table_configs['server']['portfolio']}
                        WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';

             """
        )
        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                conn.execute(text(delete_query))
                conn.commit()
            return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was removed from db"}
    except Exception as e:
        print(f"error occurred while running delete query: {e}")
        return None


def add_new_stock_to_portfolio(user_id: str, portfolio_id: str, stock_int: int):
    """
    Updates the stock array in a portfolio entry for a specified user by adding a new stock.

    This function updates a record in the `portfolio` table in the database. If the specified stock
    is not already present in the `stock_array`, it appends the stock to the array. The update is
    performed using an SQL `UPDATE` statement.

    Args:
        user_id (str): The ID of the user for whom the portfolio is being updated.
        portfolio_id (str): The ID of the portfolio to be updated.
        stock_int (int): The stock identifier to be added to the portfolio.

    Returns:
        dict: A dictionary with the following keys:
            - 'code': An integer status code (1 for success).
            - 'msg': A message indicating the result of the operation.
        Returns None if an error occurs during the update.

    """
    try:
        update_query = (
            f"""
               UPDATE {table_configs['server']['portfolio']}
               SET stock_array = CASE
                                WHEN NOT ({stock_int} = ANY(stock_array)) THEN stock_array || {stock_int}
                                ELSE stock_array END
               WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';
            """
        )
        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                conn.execute(text(update_query))
                conn.commit()
        return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was was updated"}

    except Exception as e:
        print(f"error occurred while running update query :{e} ")
    return None


def remove_stock_from_portfolio(user_id: str, portfolio_id: str, stock_int: int):
    """
    Removes a specific stock from the stock array in a portfolio entry for a given user.

    This function updates a record in the `portfolio` table in the database by removing a specified
    stock from the `stock_array`. The update is performed using an SQL `UPDATE` statement that
    utilizes the `array_remove` function to remove the stock identifier from the array.

    Args:
        user_id (str): The ID of the user whose portfolio is being updated.
        portfolio_id (str): The ID of the portfolio from which the stock will be removed.
        stock_int (int): The stock identifier to be removed from the portfolio.

    Returns:
        dict: A dictionary with the following keys:
            - 'code': An integer status code (1 for success).
            - 'msg': A message indicating the result of the operation.
        Returns None if an error occurs during the update.
    """
    try:
        update_query = (
            f"""
               UPDATE {table_configs['server']['portfolio']}
               SET stock_array = array_remove(stock_array, {stock_int})
               WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';
            """
        )
        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                conn.execute(text(update_query))
                conn.commit()
        return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was was updated"}

    except Exception as e:
        print(f"error occurred while running update query: {e} ")
    return None


def get_all_portfolios(user_id: str):
    """
    Retrieves all portfolios for a specified user, including stocks in each portfolio.

    This function fetches portfolio data from the database for a given user, including:
    - Portfolios with their stock IDs.
    - Portfolios with no stocks, represented with a placeholder stock ID of -1.
    - Stocks are mapped to their corresponding symbols from the `distinct_stock` dataset.

    The function returns a JSON string where each key is a portfolio ID, and each value is a dictionary
    mapping stock IDs to their symbol names. If a portfolio has no stocks, its value is `None`.

    Args:
        user_id (str): The ID of the user whose portfolios are to be retrieved.

    Returns:
        str: A JSON string where each key is a portfolio ID and each value is a dictionary with:
             - Stock IDs as keys.
             - Stock symbols as values.
             If a portfolio has no stocks, its value is `None`.
        Returns None if an error occurs during the query execution.
    """
    try:
        select_query = f"""
    with portfolios as(
            select 
                portfolio_id,
                UNNEST(stock_array) as stock_id
                from {table_configs['server']['portfolio']} where user_id='{user_id}' and cardinality(stock_array)>0
                ),
        empty_portfolios as(
            select 
                portfolio_id,
                -1 as stock_id 
            from {table_configs['server']['portfolio']} where user_id='{user_id}' and cardinality(stock_array)=0
            ),
        all_portfolios as(
            select 
                    portfolio_id, 
                    stock_id 
                from portfolios union 
            select 
                    portfolio_id,
                    stock_id
                from empty_portfolios
            ),
        distinct_stock as(
             select 
                distinct 
                index_symbol,
                symbol_name 
                from {table_configs['stocks']['raw_data']}
            )
        select 
         a.portfolio_id,
         case when a.stock_id=-1 then null else stock_id end as stock_id,
         b.symbol_name 
    from all_portfolios a LEFT join distinct_stock b on a.stock_id=index_symbol
        """
        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                result = conn.execute(text(select_query)).fetchall()
                dict_res = {}
                for row in result:
                    if row[1] is None:
                        dict_res[row[0]] = None
                    else:
                        if row[0] in dict_res.keys():
                            dict_res[row[0]].update({row[1]: row[2]})
                        else:
                            dict_res[row[0]] = {row[1]: row[2]}
        return json.dumps(dict_res)
    except Exception as e:
        print(f"error occurred while running query: {e}")


def insert_new_user_to_db(user_id: str, hash_pass: str, email_address: str, install_date: datetime,
                          creation_date: datetime, update_date: datetime):
    """
    Insert a new user into the database if the user ID or email address doesn't already exist.

    Parameters:
    - user_id (str): The user ID.
    - hash_pass (str): The hashed password.
    - email_address (str): The email address.
    - install_date (datetime): The installation date.
    - creation_date (datetime): The creation date.
    - update_date (datetime): The update date.

    Returns:
    - dict or None: A dictionary containing a code and a message if the user is inserted successfully,
      or None if an error occurs during the insertion process.
        - code (int): 0 if the user or email is found in the database, 1 otherwise.
        - msg (str): A message indicating whether the user or email is found in the database or not.
    """
    is_user_exists = check_if_user_exists(user_id, email_address)
    if is_user_exists['code'] == 0:
        return {'code': 0, 'msg': 'user or email found in db'}
    else:
        # noinspection PyBroadException
        try:
            insert_query = (
                f"""
                                       INSERT INTO {table_configs['server']['users']} (user_id,
                                                                       hash_pass,
                                                                       email_address,
                                                                       install_date,
                                                                       creation_date,
                                                                       update_date)
                                       VALUES ('{user_id}','{hash_pass}','{email_address}','{install_date}','{creation_date}','{update_date}' )
                                       """
            )
            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    conn.execute(text(insert_query))
                    conn.commit()
                return {'code': 1, 'msg': f" user: {user_id}, {email_address} was inserted to db"}
        except Exception as e:
            print(f"error occurred while running insert query: {e}")
            return None


def insert_raw_action(evt_name: str, server_time: datetime, user_id: str, evt_details: dict = None):
    """
    Inserts a raw action record into the database.

    param user_id: user id- needs to be from server. Users!
    param evt_name: Name of the event.
    param server_time: Timestamp representing the time when the event occurred on the server.
    param evt_details: Additional details about the event, stored as a dictionary. Defaults to None.

    return: A dictionary containing a code and a message indicating the result of the insertion operation.
        - 'code' (int): Indicates the status of the insertion operation. 1 indicates success, while None indicates an error occurred.
        - 'msg' (str): A message describing the outcome of the insertion operation. If successful, it indicates that the action was listed in the database.
    """
    if evt_details is None:
        evt_details = {}  # Set evt_details to an empty dictionary if None

    server_time_str = server_time.isoformat()

    # Convert evt_details to a JSON string
    evt_details_str = json.dumps(evt_details)

    try:
        insert_query = f"""
            INSERT INTO {table_configs['server']['actions']} (evt_date, evt_time, evt_name, server_time, evt_details, user_id)
            VALUES ('{datetime.now().date()}', '{datetime.now()}', '{evt_name}', '{server_time_str}', '{evt_details_str}' ,'{user_id}')
        """

        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                conn.execute(text(insert_query))
            return {'code': 1, 'msg': f"Action listed in db"}
    except Exception as e:
        print("Error occurred while running insert query:", e)
        return None
