import json
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from datetime import datetime, date
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import timedelta
import os
import pickle
from pathlib import Path


from utilities.ml import train_xgboost_regressor, predict_on_xgboost_regressor

from utilities.tase_api_and_config import (
    stock_list,
    table_configs,
    temp_folders_list,
    get_Bar,
    indices_EoD_by_index_from_date_to_date,
    securities_EoD_by_index_from_date_to_date,
    get_matching_stock_name,

)


def store_bearer_token(**kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    bearer = get_Bar()
    kwargs['ti'].xcom_push(key='bearer', value=bearer)
    logging.info(f"API call for bearer succeeded for date: '{execution_date}'bearer is:{bearer}")


def collect_data(stock_index, **kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    file_path = f"{temp_folders_list['ML']['raw_data']}/{stock_index}_rawData_{execution_date}.parquet"
    try:
        df = pd.read_parquet(file_path)
        if not df.empty:
            logging.info(f"skipping task -> raw data found : {file_path} ")
            return
    except FileNotFoundError:
        logging.info(f"{file_path} was not found, proceeding to collect data.")
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        raise

    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')
    select_query = f"""
        SELECT
            date,
            close
        FROM stocks.tase_stock_data
        WHERE index_symbol = {stock_index}
        AND date <= '{execution_date}'::date;
    """
    logging.info(select_query)

    db_info = postgres_hook.get_pandas_df(sql=select_query)
    db_info['date'] = pd.to_datetime(db_info['date'])
    db_info.set_index('date', inplace=True)
    db_info.sort_index()

    api_end_date = db_info.index.min() - timedelta(days=1)
    db_num_rows = len(db_info)

    api_start_date = api_end_date - timedelta(days=(403 - db_num_rows))
    api_start_date = api_start_date.strftime('%Y-%m-%d')
    api_end_date = api_end_date.strftime('%Y-%m-%d')
    # bearer_token = get_Bar()
    bearer_token = kwargs['ti'].xcom_pull(task_ids='get_bearer_token', key='bearer')

    logging.info(f"---stock_index: {stock_index}")
    logging.info(f"---bearer_token: {bearer_token}")
    logging.info(f"---api_start_date: {api_start_date}")
    logging.info(f"---api_end_date: {api_end_date}")

    is_index = next(
        (stock['IsIndex'] for stock in stock_list if stock['index_id'] == stock_index),
        None
    )
    if is_index:
        api_info = indices_EoD_by_index_from_date_to_date(
            bearer=bearer_token, index_id=stock_index,
            start_date=api_start_date, end_date=api_end_date
        )
    else:
        api_info = securities_EoD_by_index_from_date_to_date(
            bearer=bearer_token, index_id=stock_index,
            start_date=api_start_date, end_date=api_end_date
        )
    logging.info(f"----api_info: {api_info}---")
    api_info = api_info[['date', 'close']]
    api_info['date'] = pd.to_datetime(api_info['date'])
    api_info.set_index('date', inplace=True)
    api_info.sort_index()

    # Merge the two data sources.
    df = pd.concat([api_info, db_info]).sort_index()
    logging.info(f"---final df: {df.head(10)}")

    # save data to temperately location
    # os.makedirs('/opt/***/temp_data', exist_ok=True)
    df.to_parquet(file_path, engine='pyarrow')
    # df.to_csv(f'/opt/airflow/temp_data/{stock_index}_temp_{execution_date}.csv')


def train_model(stock_index, **kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    regressor_file_path = f"{temp_folders_list['ML']['regressors']}/{stock_index}_regressor_{execution_date}.pkl"
    if Path(regressor_file_path).exists():
        logging.info(f'skipping task ->regressor found : {regressor_file_path} ')
        return

    raw_data_file = f"{temp_folders_list['ML']['raw_data']}/{stock_index}_rawData_{execution_date}.parquet"
    df = pd.read_parquet(raw_data_file)
    reg = train_xgboost_regressor(df)
    os.makedirs('/opt/airflow/temp_regressors', exist_ok=True)
    with open(regressor_file_path, 'wb') as f:
        pickle.dump(reg, f)
    return


def predict_future_days(stock_index, **kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    prediction_file = f"{temp_folders_list['ML']['predictions']}/{stock_index}_predictions_{execution_date}.json"
    if Path(prediction_file).exists():
        logging.info(f'skipping task ->prediction found  : {prediction_file} ')
        return

    raw_data_file = f"{temp_folders_list['ML']['raw_data']}/{stock_index}_rawData_{execution_date}.parquet"
    df = pd.read_parquet(raw_data_file)
    regressor_file = f"{temp_folders_list['ML']['regressors']}/{stock_index}_regressor_{execution_date}.pkl"
    with open(regressor_file, 'rb') as f:
        regressor = pickle.load(f)

    predictions = predict_on_xgboost_regressor(reg=regressor, df=df)
    with open(prediction_file, 'w') as f:
        f.write(predictions)


def store_prediction_to_db(**kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    prediction_folder = Path(temp_folders_list['ML']['predictions'])
    prediction_list = []
    for file in prediction_folder.iterdir():
        date_of_prediction = file.stem.split('_')[2]
        stock_of_prediction = file.stem.split('_')[0]
        if date_of_prediction == execution_date:
            logging.info(f'--reading file : {file.stem}')
            with open(file, 'r') as f:
                prediction_list.append(
                    {
                        'index_symbol': stock_of_prediction,
                        'symbol_name': get_matching_stock_name(int(stock_of_prediction)),
                        'predictions': json.load(f)
                    }
                )
    if len(prediction_list) == 0:
        logging.info(f"no prediction found for date: {execution_date}")
        return
    logging.info(f"prediction_list is :{prediction_list}")

    logging.info("start inserting to db")
    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')
    delete_values = ", ".join([f"('{info['index_symbol']}', '{execution_date}')" for info in prediction_list])
    delete_query = f"DELETE FROM {table_configs['stocks']['predictions']}  WHERE (index_symbol, insert_time) IN ({delete_values});"
    logging.info(f"running delete_query: {delete_query}")
    postgres_hook.run(sql=delete_query)
    insert_query = """
              INSERT INTO {table_name}  (index_symbol, symbol_name, predictions, insert_time)
              VALUES {values}
              """.format(
        table_name=table_configs['stocks']['predictions'],
        values=",".join(["('{}', '{}', '{}', '{}')".format(
            info['index_symbol'], "NULL" if info['symbol_name'] is None else info['symbol_name'],
            json.dumps(info['predictions']).replace("'", "''"), execution_date
        ) for info in prediction_list])
    )
    logging.info(f"running insert_query: {insert_query}")
    postgres_hook.run(sql=insert_query)


def garbage_collector(**kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    for folder in temp_folders_list['ML']:
        folder_obj = Path(temp_folders_list['ML'][folder])
        for file in folder_obj.iterdir():
            file_full_path = file.resolve()
            file_name_without_extension = file.stem
            date_of_file = file_name_without_extension.split('_')[2]
            if date_of_file == execution_date:
                try:
                    file.unlink()  # Delete the file
                    print(f"Deleted file: {file_full_path}")
                except FileNotFoundError:
                    print(f"File not found: {file_full_path}")
                except PermissionError:
                    print(f"Permission denied: {file_full_path}")
                except Exception as e:
                    print(f"Error deleting file {file_full_path}: {e}")


def preprocess_validations():
    for folder in temp_folders_list['ML']:
        folder_obj = Path(temp_folders_list['ML'][folder])
        if not folder_obj.exists():
            folder_obj.mkdir(parents=True)
            logging.info(f"Folder '{folder_obj}' created.")
        else:
            logging.info(f"Folder '{folder_obj}' already exists.")


default_args = {
    'start_date': datetime(2024, 7, 18),
    'end_date': datetime(2024, 9, 12),
    'schedule_interval': '0 3 * * *',
    'catchup': False,
    'depends_on_past': True,
}
with DAG(
        dag_id='tase_stock_predict',
        default_args=default_args,
        max_active_runs=1
) as dag:
    preprocess_validations = PythonOperator(
        task_id='preprocess_validations',
        python_callable=preprocess_validations,
        provide_context=True
    )
    get_bearer_token = PythonOperator(
        task_id='get_bearer_token',
        python_callable=store_bearer_token,
        provide_context=True
    )
    store_prediction_to_db = PythonOperator(
        task_id='store_prediction_to_db',
        python_callable=store_prediction_to_db,
        provide_context=True
    )
    remove_temp_files = PythonOperator(
        task_id='remove_temp_files',
        python_callable=garbage_collector,
        provide_context=True
    )

    prediction_tasks = []
    for stock in stock_list:
        collect_data_task = PythonOperator(
            task_id=f"collect_data_{stock['index_id']}",
            python_callable=collect_data,
            op_args=[stock['index_id']],
            provide_context=True
        )
        train_model_task = PythonOperator(
            task_id=f"train_model_{stock['index_id']}",
            python_callable=train_model,
            op_args=[stock['index_id']],
            provide_context=True
        )
        predict_future_days_task = PythonOperator(
            task_id=f"predict_future_days_{stock['index_id']}",
            python_callable=predict_future_days,
            op_args=[stock['index_id']],
            provide_context=True
        )

        # Set up the dependencies for each stock
        get_bearer_token >> collect_data_task >> train_model_task >> predict_future_days_task
        # Collect the final prediction task for each stock to set the dependencies for the store_prediction_to_db.
        prediction_tasks.append(predict_future_days_task)

    # Once all the predictions where completes, run the store_prediction_to_db and the garbage_collector.
    prediction_tasks >> store_prediction_to_db >> remove_temp_files

    # Set the initial dependencies.
    preprocess_validations >> get_bearer_token
