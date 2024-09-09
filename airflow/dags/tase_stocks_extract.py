import logging
from datetime import datetime

from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from airflow import DAG
from utilities.tase_api_and_config import (get_Bar,
                                           indices_EoD_by_date,
                                           securities_EoD_by_date,
                                           stock_list,
                                           table_configs,
                                           )


def store_bearer_token(**kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    bearer = get_Bar()
    kwargs['ti'].xcom_push(key='bearer', value=bearer)
    logging.info(f"API call for bearer succeeded for date: '{execution_date}'bearer is:{bearer}")


def extract_stock_data(stock_index, Isindex: bool, **kwargs, ):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    current_bearer_token = kwargs['ti'].xcom_pull(task_ids='get_bearer_token', key='bearer')
    logging.info(f"using current_bearer_token: {current_bearer_token}")
    if Isindex:
        stock_info = indices_EoD_by_date(current_bearer_token, stock_index, execution_date)
    else:
        stock_info = securities_EoD_by_date(current_bearer_token, stock_index, execution_date)
    logging.info(f'Stock info for index {stock_index}: {stock_info}')
    kwargs['ti'].xcom_push(key=f'{stock_index}', value=stock_info)


def store_stock_info(**kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')
    all_stock_info = []
    for stock in stock_list:
        # sanitized_stock_name = stock['name'].replace(" ", "_").replace("-", "_")
        stock_info = kwargs['ti'].xcom_pull(task_ids=f"extract_{stock['index_id']}_info", key=f"{stock['index_id']}")
        if stock_info is None:
            pass
        else:
            all_stock_info.append(stock_info)
            logging.info(f"for stock {stock['index_id']}, info is :{stock_info}")

    if len(all_stock_info) == 0:
        logging.info(f"no record data for date: {execution_date}")
    else:
        delete_values = ", ".join([f"('{info['symbol']}', '{info['date']}')" for info in all_stock_info])
        delete_query = f"DELETE FROM {table_configs['stocks']['raw_data']}  WHERE (index_symbol, date) IN ({delete_values});"
        logging.info(f"running delete_query: {delete_query}")
        postgres_hook.run(sql=delete_query)

        insert_query = """
            INSERT INTO {table_name} (index_symbol, symbol_name, date, open, close, high, low, omc, volume)
            VALUES {values}
            """.format(
            table_name=table_configs['stocks']['raw_data'],
            values=",".join(["('{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {})".format(
                info['symbol'], info['symbol_name'], info['date'], info['open'],
                info['close'], info['high'], info['low'], info['omc'],
                'NULL' if info['volume'] is None else info['volume']
            ) for info in all_stock_info])
        )

        logging.info(f"running insert query : {insert_query}")

        ##run  postgres_hook.run(sql=delete_query)
        postgres_hook.run(sql=insert_query)


default_args = {
    'start_date': datetime(2024, 7, 18),
    'end_date': datetime(2024, 9, 12),
    'schedule_interval': '0 2 * * *',
    'catchup': False,
    'depends_on_past': True,
}
with DAG(
        dag_id='tase_stock_extract',
        default_args=default_args,
        max_active_runs=1
) as dag:
    start_dummy = EmptyOperator(
        task_id='start_dummy'
    )
    get_bearer_token = PythonOperator(
        task_id='get_bearer_token',
        python_callable=store_bearer_token,
        provide_context=True
        # trigger_rule = 'one_success'
    )

    store_stock_info = PythonOperator(
        task_id='store_stock_info',
        python_callable=store_stock_info,
        provide_context=True
        # trigger_rule='one_success'

    )

    for stock in stock_list:
        # sanitized_stock_name = stock['name'].replace(" ", "_").replace("-", "_")
        extract_stock_data_task = PythonOperator(
            task_id=f"extract_{stock['index_id']}_info",
            python_callable=extract_stock_data,
            op_args=[stock['index_id'], stock['IsIndex']],
            provide_context=True
            # trigger_rule='one_success'
        )

        start_dummy >> get_bearer_token >> extract_stock_data_task >> store_stock_info
