import logging
from datetime import datetime
import pandas as pd
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow import DAG


from utilities.tase_api_and_config import stock_list,table_configs
from utilities.stats import calc_stock_stats_sharp_ratio, calc_stock_stats_daily_increase, \
    calc_stock_stats_norm_distribution


def extract_stock_data_from_db(stock_index, start_date: datetime = datetime(1970, 1, 1),**kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')
    select_query = f"""
            SELECT * FROM {table_configs['stocks']['raw_data']} 
            WHERE date >= '{start_date}' and date<='{execution_date}' and index_symbol={stock_index}
        """
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(select_query)
    records = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    stock_info = pd.DataFrame(records, columns=column_names)
    logging.info(f"done querying data for index: {stock_index}")
    logging.info(f"df results\n: {stock_info}")

    stock_info_json = stock_info.to_json(orient='split')
    # Push the JSON string to XCom
    if stock_info_json:
        kwargs['ti'].xcom_push(key=f'{stock_index}', value=stock_info_json)
        logging.info(f"succeed to push data to XCom: stock_info_json {stock_info_json}")
    else:
        logging.error("Failed to push data to XCom: stock_info_json is None")


def run_stock_stats_sharp_ratio(stock_index, **kwargs):
    symbol_name = next((stock['name'] for stock in stock_list if stock['index_id'] == int(stock_index)), None)
    stock_info_json = kwargs['ti'].xcom_pull(task_ids=f"extract_{stock_index}_info", key=f'{stock_index}')
    if stock_info_json:
        stock_info = pd.read_json(stock_info_json, orient='split')
        logging.info(f"Processing data for index: {stock_index}")
        logging.info(f"df results\n: {stock_info}")
    else:
        logging.error(f"can't find data for for symbol_name: {symbol_name}")
        return
    sharp_ratio_json = calc_stock_stats_sharp_ratio(stock_data=stock_info)
    logging.info(f"sharp_ratio_dict: {sharp_ratio_json}")
    if sharp_ratio_json:
        kwargs['ti'].xcom_push(key=f'{stock_index}_sharp_ratio', value=sharp_ratio_json)
        logging.info(f"succeed to push data to XCom: {stock_index}_sharp_ratio: {sharp_ratio_json}")
    else:
        logging.error("Failed to push data to XCom: sharp_ratio_json is None")


def run_stock_stats_daily_increase(stock_index, **kwargs):
    symbol_name = next((stock['name'] for stock in stock_list if stock['index_id'] == int(stock_index)), None)
    stock_info_json = kwargs['ti'].xcom_pull(task_ids=f"extract_{stock_index}_info", key=f'{stock_index}')
    if stock_info_json:
        stock_info = pd.read_json(stock_info_json, orient='split')
        logging.info(f"Processing data for index: {stock_index}")
        logging.info(f"df results\n: {stock_info}")
    else:
        logging.error(f"can't find data for for symbol_name: {symbol_name}")
        return
    daily_increase_json = calc_stock_stats_daily_increase(stock_data=stock_info)
    logging.info(f"daily_increase_dict: {daily_increase_json}")
    if daily_increase_json:
        kwargs['ti'].xcom_push(key=f'{stock_index}_daily_increase', value=daily_increase_json)
        logging.info(f"succeed to push data to XCom: {stock_index}_daily_increase: {daily_increase_json}")
    else:
        logging.error("Failed to push data to XCom: daily_increase_json is None")


def run_stock_stats_norm_distribution(stock_index, **kwargs):
    symbol_name = next((stock['name'] for stock in stock_list if stock['index_id'] == int(stock_index)), None)
    stock_info_json = kwargs['ti'].xcom_pull(task_ids=f"extract_{stock_index}_info", key=f'{stock_index}')
    if stock_info_json:
        stock_info = pd.read_json(stock_info_json, orient='split')
        logging.info(f"Processing data for index: {stock_index}")
        logging.info(f"df results\n: {stock_info}")
    else:
        logging.error(f"can't find data for for symbol_name: {symbol_name}")
        return
    norm_distribution_json = calc_stock_stats_norm_distribution(stock_data=stock_info)
    logging.info(f"norm_distribution_dict: {norm_distribution_json}")
    if norm_distribution_json:
        kwargs['ti'].xcom_push(key=f'{stock_index}_norm_distribution', value=norm_distribution_json)
        logging.info(f"succeed to push data to XCom: {stock_index}_norm_distribution: {norm_distribution_json}")
    else:
        logging.error("Failed to push data to XCom: norm_distribution_json is None")


def store_stats(**kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')
    all_stats = []
    for stock in stock_list:
        ##extract stats data from xcom
        sharp_info = kwargs['ti'].xcom_pull(task_ids=f"run_stats_{stock['index_id']}_sharp_ratio",
                                            key=f'{stock["index_id"]}_sharp_ratio')
        daily_increase_info = kwargs['ti'].xcom_pull(task_ids=f"run_stats_{stock['index_id']}_daily_increase",
                                                     key=f'{stock["index_id"]}_daily_increase')

        norm_distribution_info = kwargs['ti'].xcom_pull(task_ids=f"run_stats_{stock['index_id']}_norm_distribution",
                                                        key=f'{stock["index_id"]}_norm_distribution')
        ##Insert info into stats dict
        if sharp_info is None:
            pass
        else:
            sharp_stats = {'stats_name': 'sharpe_ratio', 'symbol': stock["index_id"], 'symbol_name': stock["name"],
                           'insert_time': execution_date, 'info': sharp_info}
            all_stats.append(sharp_stats)
            logging.info(f"for stock {stock['index_id']}, sharp_info is:{sharp_info}")

        if daily_increase_info is None:
            pass
        else:
            daily_increase = {'stats_name': 'daily_increase', 'symbol': stock["index_id"], 'symbol_name': stock["name"],
                              'insert_time': execution_date, 'info': daily_increase_info}
            all_stats.append(daily_increase)
            logging.info(f"for stock {stock['index_id']}, daily_increase is :{daily_increase}")

        if norm_distribution_info is None:
            pass
        else:
            norm_distribution = {'stats_name': 'norm_distribution', 'symbol': stock["index_id"],
                                 'symbol_name': stock["name"],
                                 'insert_time': execution_date, 'info': norm_distribution_info}
            all_stats.append(norm_distribution)
            logging.info(f"for stock {stock['index_id']}, norm_distribution is :{norm_distribution}")

    if len(all_stats) == 0:
        logging.info(f"no record stats for date: {execution_date}")
    # set up and run insert query
    else:
        insert_query = """
                  INSERT INTO {table_name} (index_symbol, symbol_name, stats_name, stats_info, insert_time)
                  VALUES {values}
                  """.format(
                    table_name=table_configs['stocks']['stats'],
                    values=",".join(["('{}', '{}', '{}', '{}', '{}')".format(
                                stats['symbol'], stats['symbol_name'], stats['stats_name'], stats['info'],
                                stats['insert_time']) for stats in all_stats]))
        logging.info(f"running insert query : {insert_query}")
        postgres_hook.run(sql=insert_query)


default_args = {
    'start_date': datetime(2024, 7, 18),
    'end_date': datetime(2024, 9, 12),
    'schedule_interval': '0 3 * * *',
    'catchup': False,
    'depends_on_past': True,
}
with DAG(
        dag_id='tase_stock_stats',
        default_args=default_args,
        max_active_runs=1
) as dag:
    start_dummy = EmptyOperator(
        task_id='start_dummy'
    )

    store_stocks_stats = PythonOperator(
        task_id='store_stocks_stats',
        python_callable=store_stats,
        provide_context=True
        # trigger_rule='one_success'
    )

    for stock in stock_list:
        extract_stock_data_from_db_task = PythonOperator(
            task_id=f"extract_{stock['index_id']}_info",
            python_callable=extract_stock_data_from_db,
            op_args=[stock['index_id'],datetime(2020, 1, 1)],
            provide_context=True
        )
        run_stock_stats_sharp_ratio_task = PythonOperator(
            task_id=f"run_stats_{stock['index_id']}_sharp_ratio",
            python_callable=run_stock_stats_sharp_ratio,
            op_args=[stock['index_id']],
            provide_context=True
        )
        run_stock_stats_daily_increase_task = PythonOperator(
            task_id=f"run_stats_{stock['index_id']}_daily_increase",
            python_callable=run_stock_stats_daily_increase,
            op_args=[stock['index_id']],
            provide_context=True
        )
        run_stock_stats_norm_distribution_task = PythonOperator(
            task_id=f"run_stats_{stock['index_id']}_norm_distribution",
            python_callable=run_stock_stats_norm_distribution,
            op_args=[stock['index_id']],
            provide_context=True
        )

        start_dummy >> extract_stock_data_from_db_task >> [run_stock_stats_sharp_ratio_task,
                                                           run_stock_stats_daily_increase_task,
                                                           run_stock_stats_norm_distribution_task] >> store_stocks_stats
