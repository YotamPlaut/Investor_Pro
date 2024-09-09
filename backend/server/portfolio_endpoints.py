from datetime import datetime
from flask import jsonify, request
from backend.functions.event_db_manager import EventDatabaseManager
from backend.functions.portfolio_db_manager import PortfolioDatabaseManager
from backend.classes_backend.portfolio import Portfolio
from backend.classes_backend.stock_info import StockData


def create_new_portfolio():
    curr_datetime = datetime.now()
    data = request.json
    if 'username' not in data or 'portfolio_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        portfolio_manager = PortfolioDatabaseManager()
        exists = portfolio_manager.is_username_and_portfolio_name_exists(data['username'],
                                                                         data['portfolio_id'])
        if exists is None:
            return jsonify({'error': 'failed to interact with database'}), 500
        elif exists:
            return jsonify({'error': 'portfolio already exists for user'}), 400

        result = portfolio_manager.insert_new_portfolio(data['username'], data['portfolio_id'])
        if result:
            event_db_manager = EventDatabaseManager()
            event_db_manager.insert_raw_action('created new portfolio', curr_datetime,
                                               data['username'], {'port_id': data['portfolio_id']})
            return jsonify({'message': 'successfully created new portfolio'}), 200
        else:
            return jsonify({'error': 'failed to interact with database'}), 500


def delete_portfolio():
    curr_datetime = datetime.now()
    data = request.json
    if 'username' not in data or 'portfolio_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        portfolio_manager = PortfolioDatabaseManager()
        exists = portfolio_manager.is_username_and_portfolio_name_exists(data['username'],
                                                                         data['portfolio_id'])

        if exists is None:
            return jsonify({'error': 'failed to interact with database'}), 500
        if not exists:
            return jsonify({'error': 'portfolio id not found for this user'}), 404

        res = portfolio_manager.remove_portfolio(data['username'], data['portfolio_id'])
        if res:
            event_db_manager = EventDatabaseManager()
            event_db_manager.insert_raw_action('deleted portfolio', curr_datetime,
                                               data['username'], {'port_id': data['portfolio_id']})
            return jsonify({'message': 'successfully removed portfolio'}), 200
        else:
            return jsonify({'error': 'failed to interact with database'}), 500


def add_stock_to_portfolio():
    curr_datetime = datetime.now()
    data = request.json
    if 'username' not in data or 'portfolio_id' not in data or 'stock_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        portfolio_manager = PortfolioDatabaseManager()
        exists = portfolio_manager.is_username_and_portfolio_name_exists(data['username'],
                                                                         data['portfolio_id'])
        if exists is None:
            return jsonify({'error': 'failed to interact with database'}), 500
        if not exists:
            return jsonify({'error': 'portfolio id not found for this user'}), 404

        stock_id = StockData.get_stock_id(data['stock_id'])
        res = portfolio_manager.add_new_stock_to_portfolio(data['username'], data['portfolio_id'], stock_id)
        if res:
            event_db_manager = EventDatabaseManager()
            event_db_manager.insert_raw_action('add stock to portfolio', curr_datetime,
                                               data['username'], {'port_id': data['portfolio_id'],
                                                                  'stock_id': data['stock_id']})
            return jsonify({'message': 'successfully added stock to portfolio'}), 200
        else:
            return jsonify({'error': 'failed to interact with database'}), 500


def remove_stock_from_portfolio():
    curr_datetime = datetime.now()
    data = request.json
    if 'username' not in data or 'portfolio_id' not in data or 'stock_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        portfolio_manager = PortfolioDatabaseManager()
        exists = portfolio_manager.is_username_and_portfolio_name_exists(data['username'], data['portfolio_id'])
        if not exists:
            return jsonify({'error': 'portfolio id not found for this user'}), 404

        stock_id = StockData()
        res = portfolio_manager.remove_stock_from_portfolio(data['username'], data['portfolio_id'], data['stock_id'])
        if res:
            event_db_manager = EventDatabaseManager()
            event_db_manager.insert_raw_action('removed stock from portfolio', curr_datetime,
                                               data['username'], {'port_id': data['portfolio_id'],
                                                                  'stock_id': data['stock_id']})
            return jsonify({'message': 'successfully removed stock from portfolio'}), 200
        else:
            return jsonify({'error': 'failed to interact with database'}), 500


def get_all_user_portfolios():
    data = request.args.get('username')
    if data is None:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        pm = PortfolioDatabaseManager()
        portfolios_temp = pm.get_all_user_portfolios(data)
        if portfolios_temp == 0:
            return jsonify({'error': 'failed to interact with database'}), 500
        else:
            portfolios = []
            for port_id in portfolios_temp.keys():
                port = Portfolio(port_id, portfolios_temp[port_id])
                portfolios.append(port.to_dict())
            return jsonify(portfolios), 200
