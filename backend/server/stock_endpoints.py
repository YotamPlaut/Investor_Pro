from datetime import datetime, timedelta
from backend.classes_backend.stock import Stock
from backend.functions.stock_db_manager import StockManager
from flask import jsonify, request
from backend.classes_backend.cache_mechanism.my_cache import LRUCache
from backend.functions.statistics_db_manager import StatisticsManager
from backend.classes_backend.stock_info import StockData


cache = LRUCache(capacity=3)


def get_stock_info():
    curr_datetime = datetime.now()
    http_data = request.args.get('stock_name')  # Assuming stock_name is the cache key
    date = curr_datetime - timedelta(days=365)

    if http_data is None:
        return jsonify({'error': 'Missing required fields'}), 400
    stock_id = StockData.get_stock_id(http_data)

    if stock_id is None:
        return jsonify({'error': 'invalid stock name'}), 404
    # Check if the stock is already in the cache
    cached_stock = cache.get(stock_id)

    if cached_stock != -1:  # Stock is found in the cache
        print(f"Stock '{http_data}' found in cache.")
        return jsonify(cached_stock.to_dict()), 200

    # Stock not found in cache, fetch from StockManager
    stock_manager = StockManager()
    stats_manager = StatisticsManager()
    stock_info = stock_manager.get_stock_data_by_date(http_data, date)
    stats_info = stats_manager.get_all_last_update_stock_stats(http_data)
    if stock_info is None:
        return jsonify({'error': 'Unable to fetch data'}), 500

    # Create Stock object
    stock = Stock(stock_info, stats_info)

    # Add the fetched stock data to the cache
    cache.put(stock_id, stock)

    return jsonify(stock.to_dict()), 200


def get_all_stocks():
    curr_datetime = datetime.now()
    stock_manager = StockManager()
    result = stock_manager.get_all_stocks()
    if result is None:
        return jsonify({'error': 'unable to fetch data'}), 500

    else:
        stock_names = []
        for stck in result:
            stock_names.append(stck['symbol_name'])

        return jsonify({'result': stock_names}), 200
