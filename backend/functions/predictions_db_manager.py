import datetime
from GCD_SETUP.gcp_setup import get_pool
from backend.classes_backend.stock_info import StockData
from sqlalchemy import text
from sqlalchemy.exc import InterfaceError
from backend.classes_backend.stock import Stock


class PredictionManager:

    _instance = None
    prediction_table_name = 'stocks.tase_stock_predictions'
    data_table_name = 'stocks.tase_stock_data'
    info_table_name = 'stocks.tase_stock_info'

    def __init__(self):
        self.stock_list = StockData.get_stock_list()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_matching_stock_name_index(self, stock_name):
        for stock in self.stock_list:
            if stock['name'] == stock_name:
                return stock['index_id']
        return None

    def get_last_update_stock_prediction(self, stock_name: str):
        """
        Retrieves the most recent stock price predictions for a given stock based on its name.

        This function fetches the latest stock price predictions from the database for the specified
        stock. It retrieves the most recent prediction data, including the stock's index symbol,
        name, and predicted closing prices for future dates. The result is returned as a JSON object.

        Args:
            stock_name (str): The name of the stock for which to retrieve the predictions.

        Returns:
            dict: A JSON string containing the stock prediction data, including:
                 - `Index_Symbol`: The stock's index symbol.
                 - `Symbol_Name`: The stock's name.
                 - `close_predictions_data`: A list of dictionaries containing the predicted closing
                   prices and their corresponding dates.
            Returns None if no matching data is found or an error occurs.

        """
        matching_stock_index = self.get_matching_stock_name_index(stock_name=stock_name)
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
                    from {self.prediction_table_name}
                    where index_symbol='{matching_stock_index}'
                    order by insert_time desc limit 1
                """
            with engine.connect() as conn:
                result = conn.execute(text(query)).fetchall()
                stock_predict_results = {}
                for row in result:
                    stock_predict_results['index_symbol'] = row[0]
                    stock_predict_results['symbol_name'] = row[1]
                    stock_predict_results['close_predictions_data'] = [{'date': date, 'close_price': price}
                                                                       for date, price in row[2].items()]
                return stock_predict_results

        except Exception as e:
            print(f"error occurred while running query: {e}")
            return None
