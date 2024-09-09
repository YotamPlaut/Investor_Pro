from flask import Flask, jsonify
from backend.functions.event_db_manager import EventDatabaseManager
from backend.functions.portfolio_db_manager import PortfolioDatabaseManager
from user_endpoints import create_new_account, login, get_all_users_info, change_password
from portfolio_endpoints import create_new_portfolio, delete_portfolio, add_stock_to_portfolio,\
    remove_stock_from_portfolio, get_all_user_portfolios
from stats_endpoints import get_single_stat, get_all_stats
from stock_endpoints import get_stock_info, get_all_stocks
from predictions_endpoints import get_stock_prediction
from backend.functions.stock_db_manager import StockManager
from backend.classes_backend.stock_info import StockData

app = Flask(__name__)


@app.route('/alive', methods=['GET'])
def alive():
    return jsonify({'message': 'alive'}), 200


def initialize_stock_data():
    db = StockManager()
    stock_data = db.get_all_stocks()  # Fetch stock data
    StockData.initialize_stock_data(stock_data)  # Initialize StockData


# ------ user endpoints ------
app.route('/create-new-account', methods=['POST'])(create_new_account)

app.route('/login', methods=['POST'])(login)

app.route('/get-all-users-info', methods=['GET'])(get_all_users_info)

app.route('/change-password', methods=['POST'])(change_password)


# ------- stocks endpoints -------
app.route('/get-all-stocks', methods=['GET'])(get_all_stocks)

app.route('/get-stock-info', methods=['GET'])(get_stock_info)

# ------- stocks endpoints -------

app.route('/get-stock-prediction', methods=['GET'])(get_stock_prediction)


# ------- event test -----
@app.route('/get-all-events', methods=['GET'])
def get_all_events():
    events_db_manager = EventDatabaseManager()
    data = events_db_manager.get_all_events()
    print(data)
    print(type(data))
    return jsonify({'message': 'test'}), 200


# ------- portfolio endpoints -------
@app.route('/get-all-portfolios', methods=['GET'])
def get_all_portfolios():
    port_manager = PortfolioDatabaseManager()
    data = port_manager.get_all_portfolios()
    print(data)
    return jsonify({'message': 'test'}), 200


app.route('/create-new-portfolio', methods=['POST'])(create_new_portfolio)

app.route('/delete-portfolio', methods=['DELETE'])(delete_portfolio)

app.route('/add-stock-to-portfolio', methods=['POST'])(add_stock_to_portfolio)

app.route('/remove-stock-from-portfolio', methods=['POST'])(remove_stock_from_portfolio)

app.route('/get-all-user-portfolios', methods=['GET'])(get_all_user_portfolios)


# ------ statistics endpoints ------
app.route('/get-single-stats', methods=['GET'])(get_single_stat)

app.route('/get-all-stats', methods=['GET'])(get_all_stats)


if __name__ == '__main__':
    # app.run(debug=True)
    # to allow machines in my network access the server
    # run the following function with the none local host ip it prints on the screen
    initialize_stock_data()
    app.run(host='0.0.0.0', port=5000, debug=True)
