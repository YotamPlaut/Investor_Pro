from datetime import datetime
from backend.classes_backend.stats.bucket import Bucket


class DailyIncrease:
    def __init__(self, data):
        self.total_days_in_view = data['stats_info']['total_days_in_view']
        self.insert_time = datetime.strptime(data['insert_time'], '%Y-%m-%d')
        self.buckets = [
            Bucket(bucket) for bucket in data['stats_info'].get('buckets', [])
        ]

    def to_dict(self):
        return {
            'stats_info': {
                'total_days_in_view': self.total_days_in_view,
                'buckets': [bucket.to_dict() for bucket in self.buckets]
            },
            'insert_time': self.insert_time.strftime('%Y-%m-%d')
        }
