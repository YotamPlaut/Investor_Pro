from flask import jsonify, request
from datetime import datetime
from backend.functions.predictions_db_manager import PredictionManager
from backend.classes_backend.prediction import Prediction


def get_stock_prediction():
    curr_datetime = datetime.now()
    http_data = request.args.get('stock_name')

    if http_data is None:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        prediction_db_manager = PredictionManager()
        prediction_fetch = prediction_db_manager.get_last_update_stock_prediction(http_data)
        if prediction_fetch is None:
            return jsonify({'error': 'unable to fetch data'}), 500
        else:
            prediction = Prediction(prediction_fetch)
            return jsonify(prediction.to_dict()), 200
