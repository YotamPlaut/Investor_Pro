###CONST####
from xgboost import XGBRegressor
import pandas as pd
import json

target = 'close'
feature = ['dayofweek', 'quarter', 'month', 'year', 'dayofyear', 'close_28_before', 'close_7_before',
           'close_3_before', 'close_2_before', 'close_1_before']


#####


def add_feature(df):
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    return df


def add_lag_feature(df):
    df['close_28_before'] = df['close'].shift(28)
    df['close_7_before'] = df['close'].shift(7)
    df['close_3_before'] = df['close'].shift(3)
    df['close_2_before'] = df['close'].shift(2)
    df['close_1_before'] = df['close'].shift(1)
    return df


def add_future_days_to_df(df, future_days):
    df = df.copy()
    start_date = df.index.max() + pd.DateOffset(days=1)
    end_date = start_date + pd.DateOffset(days=future_days)
    time_span = pd.date_range(start_date, end_date)
    future_df = pd.DataFrame(index=time_span)
    future_df['isFuture'] = True
    df['isFuture'] = False
    df_and_Future = pd.concat([df, future_df])
    df_and_Future = add_feature(df_and_Future)
    df_and_Future = add_lag_feature(df_and_Future)
    return df_and_Future


def train_xgboost_regressor(df, n_estimators: int = 6000, early_stopping_rounds: int = 50,
                            learning_rate: int = 0.001,
                            verbose=1000):
    df = df.copy()
    df = add_feature(df)
    df = add_lag_feature(df)

    X_all = df[feature]
    y_all = df[target]

    reg = XGBRegressor(n_estimators=n_estimators, early_stopping_rounds=early_stopping_rounds,
                       learning_rate=learning_rate)
    reg.fit(X_all, y_all,
            eval_set=[(X_all, y_all)],
            verbose=verbose
            )
    return reg


def predict_on_xgboost_regressor(reg, df, future_days=7):
    df = add_future_days_to_df(df=df, future_days=future_days)
    future = df.query('isFuture').copy()
    predictions = reg.predict(future[feature])
    predictions_dict = {str(ts): round(float(val), 2) for ts, val in zip(future.index, predictions)}
    predictions_json = json.dumps(predictions_dict)
    return predictions_json
