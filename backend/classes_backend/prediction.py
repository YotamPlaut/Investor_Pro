from datetime import datetime


class Prediction:
    def __init__(self, data):
        self.index_symbol = data['index_symbol']
        self.symbol_name = data['symbol_name']
        # Sort the predictions by date
        self.close_predictions_data = sorted(
            data['close_predictions_data'],
            key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S')
        )

    def to_dict(self):
        return {
            'index_symbol': self.index_symbol,
            'symbol_name': self.symbol_name,
            'close_predictions_data': self.close_predictions_data
        }
