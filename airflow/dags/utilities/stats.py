import json
import logging
import numpy as np
import pandas as pd


def calc_stock_stats_sharp_ratio(stock_data: pd.DataFrame,
                                 risk_free_rate_annual=0.045,
                                 trading_days_per_year: int = 252):
    try:
        stock_data = stock_data.copy()

        # Calculate daily returns
        stock_data['daily_returns'] = stock_data['close'].pct_change().dropna()

        # Calculate the daily risk-free rate
        daily_risk_free_rate = (1 + risk_free_rate_annual) ** (1 / trading_days_per_year) - 1

        # Calculate the excess returns
        stock_data['excess_returns'] = stock_data['daily_returns'] - daily_risk_free_rate

        # Calculate the average of excess returns
        avg_excess_return = stock_data['excess_returns'].mean()

        # Calculate the standard deviation of excess returns
        std_excess_return = stock_data['excess_returns'].std()

        # Calculate the Sharpe Ratio
        sharpe_ratio = avg_excess_return / std_excess_return

        # Annualize the Sharpe Ratio
        annualized_sharpe_ratio = sharpe_ratio * np.sqrt(trading_days_per_year)

        total_days = stock_data.shape[0]
        res_json = json.dumps({'total_days_in_view': total_days, 'sharp_ratio': annualized_sharpe_ratio})
        return res_json

    except Exception as e:
        logging.ERROR(e)


def calc_stock_stats_daily_increase(stock_data: pd.DataFrame,
                                    buckets=None):
    if buckets is None:
        buckets = [-float('inf'), -0.2, -0.1, -0.05, -0.03, -0.01, 0.01, 0.03, 0.05,
                   0.1, 0.2, float('inf')]
    try:
        stock_data = stock_data.copy()
        stock_data['increase_val'] = (stock_data['close'] - stock_data['open']) / stock_data['open']

        bucket_counts = pd.cut(stock_data['increase_val'], bins=buckets).value_counts().sort_index()
        total_days = stock_data.shape[0]
        bucket_percentages = (bucket_counts / total_days) * 100
        res_dict = {
            "total_days_in_view": int(total_days),
            "buckets": []
        }
        for bucket_range, count, percentage in zip(bucket_counts.index, bucket_counts.values,
                                                   bucket_percentages.values):
            if count > 0:
                bucket_start, bucket_end = bucket_range.left, bucket_range.right
                bucket_info = {
                    "bucket_start": float(bucket_start),
                    "bucket_end": float(bucket_end),
                    "count": int(count),
                    "percentage_of_total": float(percentage)
                }
                res_dict["buckets"].append(bucket_info)
        res_json = json.dumps(res_dict)
        return res_json
    except Exception as e:
        logging.ERROR(e)


def calc_stock_stats_norm_distribution(stock_data: pd.DataFrame):
    try:
        stock_data = stock_data.copy()
        stock_data['daily_returns'] = stock_data['close'].pct_change().dropna()
        avg_daily_returns = stock_data['daily_returns'].mean()
        std_daily_returns = stock_data['daily_returns'].std()
        total_days = stock_data.shape[0]
        res_json = json.dumps({'total_days_in_view': total_days, 'avg_daily_returns': avg_daily_returns,
                           'std_daily_returns': std_daily_returns})
        return res_json
    except Exception as e:
        logging.ERROR(e)

