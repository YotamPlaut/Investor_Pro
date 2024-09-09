from datetime import datetime


class SharpeRatio:
    def __init__(self, data):
        self.total_days_in_view = data['stats_info']['total_days_in_view']
        self.sharp_ratio = data['stats_info']['sharp_ratio']
        self.insert_time = datetime.strptime(data['insert_time'], '%Y-%m-%d')

    def to_dict(self):
        return {
            'stats_info': {
                'total_days_in_view': self.total_days_in_view,
                'sharp_ratio': self.sharp_ratio
            },
            'insert_time': self.insert_time.strftime('%Y-%m-%d')
        }
