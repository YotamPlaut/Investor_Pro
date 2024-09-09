import datetime
from GCD_SETUP.gcp_setup import get_pool
from backend.classes_backend.stock_info import StockData
from sqlalchemy import text
from sqlalchemy.exc import InterfaceError
from backend.classes_backend.stock import Stock


class StockManager:
    _instance = None
    data_table_name = 'stocks.tase_stock_data'
    info_table_name = 'stocks.tase_stock_info'

    def __init__(self):
        self.stock_list = StockData.get_stock_list()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_stock_data_by_date(self, stock_name: str, date: datetime):
        """
         Fetches stock data for a given stock name starting from a specific date.
        :param stock_name: The name of the stock, which must be present in the stock_list.
        :param date: The start date for fetching the stock records, in the format of yyyy-mm-dd.
        :return: A JSON string containing:
                 - 'info': A dictionary where keys are dates and values are dictionaries of stock data (fields: Index_Symbol, Symbol_Name, Open, Close, High, Low, OMC, Volume).
                 - 'num_days': The number of unique dates in the data.
                 - 'Index_Symbol': The index symbol of the stock.
                 - 'Symbol_Name': The name of the stock.
                 If an error occurs, None is returned.
        """
        matching_stock_index = next(
            (stock['index_id'] for stock in self.stock_list if stock['name'] == stock_name),
            None)
        if matching_stock_index is None:
            print(f"didnt found maching index for stock: {stock_name}")
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
                    from {self.data_table_name} a left join {self.info_table_name} b 
                    on a.index_symbol=b.index_symbol
                    where a.index_symbol='{matching_stock_index}' and date>=date('{date}');
              """
            with engine.connect() as conn:
                result = conn.execute(text(query)).fetchall()
                stock_data_dict = {'price_data': []}
                for row in result:
                    stock_data_dict['price_data'].append(
                        {
                            'date': row[0].strftime('%Y-%m-%d'),
                            'close_price': row[4]
                        }
                    )
                num_days = len(stock_data_dict['price_data'])
                stock_data_dict['num_days'] = num_days
                stock_data_dict['index_symbol'] = matching_stock_index
                stock_data_dict['symbol_name'] = stock_name
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
                #stock_data_json = json.dumps(stock_data_dict)
                return stock_data_dict

        except InterfaceError:
            return None
        except Exception as e:
            print(f"error occurred while running query: {e}")
            return None

    def is_valid_index(self, stock_index: int):
        for stock in self.stock_list:
            if stock['index_id'] == stock_index:
                return True
        return False

    def get_all_stocks(self):
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
        from {self.info_table_name}
                    """
        )
        try:
            engine = get_pool()
            with engine.connect() as conn:
                result = conn.execute(text(select_query)).fetchall()

                all_stock = [{'index_symbol': stck[0],
                              'symbol_name': stck[1],
                              'description': stck[2]
                              } for stck in result]
                # all_stock = {f'{stock[0]}': stock[1] for stock in result}
                return all_stock
        except Exception as e:
            print(f"error occurred while running query: {e}")
            return None


if __name__ == '__main__':
    st_manager = StockManager()
    data = st_manager.get_stock_data_by_date('Bank_Hapoalim', '2024-05-06')
    print(data)
    stock = Stock(data)
    print(stock)
    print(stock.price_data)
