from datetime import datetime
from flask import jsonify, request
from backend.functions.user_database_manager import UserDatabaseManager
from backend.functions.event_db_manager import EventDatabaseManager


def create_new_account():

    function_called_timestamp = datetime.now()
    # Get account details from the request
    data = request.json

    # Check if all required fields are provided
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    user_db_manager = UserDatabaseManager()

    # Check if the username is already taken
    exists = user_db_manager.is_username_exists(data['username'])
    if exists is None:
        return jsonify({'error': 'failed to interact with database'}), 500
    if exists:
        return jsonify({'error': 'Username already taken'}), 400

    res = user_db_manager.load_new_user_to_database(data['username'], data['password'], data['email'])
    if res:
        event_db_manager = EventDatabaseManager()
        event_db_manager.insert_raw_action('sign_up', function_called_timestamp, data['username'])
        return jsonify({'message': 'Account added successfully'}), 200
    else:
        return jsonify({'error': 'failed to interact with database'}), 500


def get_all_users_info():
    user_db_manager = UserDatabaseManager()
    data = user_db_manager.get_all_users_info()
    print(data)
    if data == 1:
        return jsonify({'error': 'failed to connect to data base'}), 503
    if data == 2:
        return jsonify({'error': 'unexpected error occurred'}), 500
    return jsonify({'message': 'test'}), 200


def change_password():

    curr_datetime = datetime.now()
    data = request.json
    if 'username' not in data or 'new_password' not in data or 'old_password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    user_db_manager = UserDatabaseManager()

    # Check if the username exists in db
    if not user_db_manager.is_username_exists(data['username']):
        return jsonify({'error': 'Invalid Username'}), 400

    if user_db_manager.authenticate_user_password(data['username'], data['old_password']):
        user_db_manager.change_password(data['username'], data['new_password'])
        event_db_manager = EventDatabaseManager()
        event_db_manager.insert_raw_action('password_change', curr_datetime, data['username'])
        return jsonify({'message': 'successfully changed password'}), 200
    else:
        return jsonify({'error': 'incorrect password'}), 404


def login():
    curr_datetime = datetime.now()
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        db_manager = UserDatabaseManager()
        exists = db_manager.authenticate_user_password(data['username'], data['password'])
        if exists is None:
            return jsonify({'error': 'failed to interact with database'}), 500
        elif exists == 1:
            event_db_manager = EventDatabaseManager()
            event_db_manager.insert_raw_action('login', curr_datetime, data['username'])
            return jsonify({'message': 'successfully logged in'}), 200
        elif exists == 0:
            return jsonify({'error': 'invalid username or password'}), 400
        elif exists == -1:
            return jsonify({'error': 'failed to interact with database'}), 500
