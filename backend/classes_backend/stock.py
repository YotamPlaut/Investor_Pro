from datetime import datetime
from backend.classes_backend.stats.sharpe_ratio import SharpeRatio
from backend.classes_backend.stats.daily_increase import DailyIncrease
from backend.classes_backend.stats.normal_distribution import NormalDistribution


class Stock:
    def __init__(self, data, statics):
        # Stock attributes
        self.symbol = data.get("index_symbol")
        self.name = data.get("symbol_name")
        self.description = data.get("description")
        self.num_days = data.get("num_days")
        self.last_access_date = datetime.today()

        # Convert date strings to datetime objects and sort the price_data by date
        self.price_data = sorted(
            [
                {"date": datetime.strptime(item["date"], "%Y-%m-%d"), "close_price": item["close_price"]}
                for item in data.get("price_data", [])
            ],
            key=lambda x: x["date"]
        )

        # Initialize additional data
        self.sharpe_ratio = SharpeRatio(statics['sharpe_ratio']) if statics['sharpe_ratio'] else None
        self.daily_increase = DailyIncrease(statics['daily_increase']) if statics['daily_increase'] else None
        self.norm_distribution = NormalDistribution(statics['norm_distribution']) if statics['norm_distribution'] else None

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "name": self.name.replace('_', ' '),
            "description": self.description,
            "num_days": self.num_days,
            "price_data": [
                {
                    "date": item["date"].strftime("%Y-%m-%d"),  # Convert datetime to string
                    "close_price": item["close_price"]
                } for item in self.price_data
            ],
            "sharpe_ratio": self.sharpe_ratio.to_dict() if self.sharpe_ratio else None,
            "daily_increase": self.daily_increase.to_dict() if self.daily_increase else None,
            "norm_distribution": self.norm_distribution.to_dict() if self.norm_distribution else None
        }
