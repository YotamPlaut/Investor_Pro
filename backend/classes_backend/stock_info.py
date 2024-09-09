class StockData:
    _stock_list = []

    @classmethod
    def get_stock_list(cls):
        return cls._stock_list

    @classmethod
    def initialize_stock_data(cls, stock_data):
        # Process stock data to remove 'IsIndex' value
        processed_data = [
            {'index_id': stock['index_symbol'], 'name': stock['symbol_name']}
            for stock in stock_data
        ]
        cls._stock_list = processed_data

    @classmethod
    def get_stock_id(cls, stock_name):
        for stock in StockData.get_stock_list():
            if stock['name'] == stock_name:
                return stock['index_id']
        # If the stock name is not found
        return None
