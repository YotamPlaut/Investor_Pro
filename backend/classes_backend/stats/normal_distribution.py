from datetime import datetime


class NormalDistribution:
    def __init__(self, data):
        self.total_days_in_view = data['stats_info']['total_days_in_view']
        self.avg_daily_returns = data['stats_info']['avg_daily_returns']
        self.std_daily_returns = data['stats_info']['std_daily_returns']
        self.insert_time = datetime.strptime(data['insert_time'], '%Y-%m-%d')

    def to_dict(self):
        return {
            'stats_info': {
                'total_days_in_view': self.total_days_in_view,
                'avg_daily_returns': self.avg_daily_returns,
                'std_daily_returns': self.std_daily_returns
            },
            'insert_time': self.insert_time.strftime('%Y-%m-%d')
        }
