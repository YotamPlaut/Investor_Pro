from datetime import datetime
from backend.functions.event_db_manager import EventDatabaseManager
from backend.functions.statistics_db_manager import StatisticsManager
from flask import jsonify, request


def get_single_stat():
    function_called_timestamp = datetime.now()
    # Get account details from the request
    data = request.json

    # Check if all required fields are provided
    if 'stat_name' not in data or 'stock_id' not in data or 'user_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    stats_db_manager = StatisticsManager()

    if not stats_db_manager.is_stock_name_exist(data['stock_id']):
        return jsonify({'error': 'stock id not found'}), 404

    if not stats_db_manager.is_stat_name_exist(data['stat_name']):
        return jsonify({'error': 'statistic name not found'}), 404

    statistics = stats_db_manager.get_last_update_stock_stats_by_stats_name(data['stock_id'], data['stat_name'])

    event_db_manager = EventDatabaseManager()
    event_details = {data['stock_id']: data['stat_name']}
    event_db_manager.insert_raw_action('statistics search', function_called_timestamp, data['user_id'], event_details)

    if statistics is None:
        return jsonify({'error': 'unable to fetch data'}), 500
    else:
        return jsonify(statistics), 200


def get_all_stats():
    function_called_timestamp = datetime.now()
    # Get account details from the request
    user_id = request.args.get('user_id')
    stock_name = request.args.get('stock_name')

    # Check if all required fields are provided
    if stock_name is None: # or 'user_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    stats_db_manager = StatisticsManager()

    if not stats_db_manager.is_stock_name_exist(stock_name):
        return jsonify({'error': 'stock id not found'}), 404

    statistics = stats_db_manager.get_all_last_update_stock_stats(stock_name)

    event_db_manager = EventDatabaseManager()
    event_db_manager.insert_raw_action('statistics search', function_called_timestamp, user_id,
                                       {'stock_name': stock_name})

    if statistics is None:
        return jsonify({'error': 'unable to fetch data'}), 500
    else:
        print(statistics)
        return jsonify({'message': 'okay'}), 200
