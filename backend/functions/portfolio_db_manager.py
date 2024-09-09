from GCD_SETUP.gcp_setup import get_pool
from sqlalchemy import text
import warnings
from sqlalchemy.exc import InterfaceError


class PortfolioDatabaseManager:

    _instance = None
    table_name = 'server.portfolios'
    stock_table_name = 'stocks.tase_stock_data'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # test this one:
    def is_username_and_portfolio_name_exists(self, username: str, portfolio_name):
        try:
            engine = get_pool()
            with engine.connect() as conn:
                query = text(f"SELECT COUNT(*) FROM {self.table_name} WHERE user_id = '{username}' "
                             f"AND portfolio_id = '{portfolio_name}' ")
                result = conn.execute(query)
                exists = result.scalar() > 0
                return exists
        except InterfaceError:
            return None
        except Exception:
            return None

    def insert_new_portfolio(self, user_id: str, portfolio_id: str, stock_array=None):
        if stock_array is None:
            stock_array = {}
        try:
            insert_query = (
                f"""
                   INSERT INTO {self.table_name} (user_id,
                                                  portfolio_id,
                                                  stock_array
                                                  )
                   VALUES ('{user_id}','{portfolio_id}','{stock_array}')
                """
            )
            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    conn.execute(text(insert_query))
                    conn.commit()
                return 1

        except InterfaceError:
            return 0

        except Exception as e:
            print("error occurred while running insert query")
            print(e)
            return 0

    def remove_portfolio(self, user_id: str, portfolio_id: str):
        try:
            delete_query = (
                f"""
                    DELETE FROM {self.table_name}
                            WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';

                 """
            )
            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    conn.execute(text(delete_query))
                    conn.commit()
                return 1

        except InterfaceError:
            return 0

        except Exception as e:
            print("error occurred while running delete query")
            return 0

    def add_new_stock_to_portfolio(self, user_id: str, portfolio_id: str, stock_int: int):
        try:
            update_query = (
                f"""
                   UPDATE {self.table_name}
                   SET stock_array = CASE
                                    WHEN NOT ({stock_int} = ANY(stock_array)) THEN stock_array || {stock_int}
                                    ELSE stock_array END
                   WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';
                """
            )
            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    conn.execute(text(update_query))
                    conn.commit()
            return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was was updated"}

        except Exception as e:
            print("error occurred while running update query ")
        return None

    def remove_stock_from_portfolio(self, user_id: str, portfolio_id: str, stock_int: int):
        try:
            update_query = (
                f"""
                   UPDATE {self.table_name}
                   SET stock_array = array_remove(stock_array, {stock_int})
                   WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';
                """
            )
            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    conn.execute(text(update_query))
                    print(update_query)
                    conn.commit()
            return 1

        except InterfaceError:
            return 0

        except Exception as e:
            print("error occurred while running update query ")
            return 0

    def get_all_portfolios(self):
        engine = get_pool()
        with engine.connect() as conn:
            result = conn.execute(
                text(f'SELECT * FROM {self.table_name}'))  # Use conn.execute instead of engine.execute
            return result.fetchall()

    def get_all_user_portfolios(self, user_id: str):
        try:
            select_query = f"""
        with portfolios as(
                select 
                    portfolio_id,
                    UNNEST(stock_array) as stock_id
                    from {self.table_name} where user_id='{user_id}' and cardinality(stock_array)>0
                    ),
            empty_portfolios as(
                select 
                    portfolio_id,
                    -1 as stock_id 
                from {self.table_name} where user_id='{user_id}' and cardinality(stock_array)=0
                ),
            all_portfolios as(
                select 
                        portfolio_id, 
                        stock_id 
                    from portfolios union 
                select 
                        portfolio_id,
                        stock_id
                    from empty_portfolios
                ),
            distinct_stock as(
                 select 
                    distinct 
                    index_symbol,
                    symbol_name 
                    from {self.stock_table_name}
                )
            select 
             a.portfolio_id,
             case when a.stock_id=-1 then null else stock_id end as stock_id,
             b.symbol_name 
        from all_portfolios a LEFT join distinct_stock b on a.stock_id=index_symbol
            """
            # try:
            #     select_query=f"""
            #     with portfolios as(
            #                     select
            #                         portfolio_id,
            #                         UNNEST(stock_array) as stock_id
            #                     from  {table_configs['server']['portfolio']} where user_id='{user_id}'
            #                     ),
            #         distinct_stock as(
            #                     select
            #                         distinct
            #                          index_symbol,
            #                          symbol_name
            #                     from {table_configs['stocks']['raw_data']}
            #                     )
            #     select
            #      a.*,
            #      b.symbol_name
            # from portfolios a LEFT join distinct_stock b on a.stock_id=index_symbol
            #     """
            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    result = conn.execute(text(select_query)).fetchall()
                    dict_res = {}
                    for row in result:
                        if row[1] is None:
                            dict_res[row[0]] = None
                        else:
                            if row[0] in dict_res.keys():
                                dict_res[row[0]].update({row[1]: row[2]})
                            else:
                                dict_res[row[0]] = {row[1]: row[2]}
            return dict_res
        except InterfaceError:
            return 0

        except Exception:
            return 0


if __name__ == '__main__':
    pdm = PortfolioDatabaseManager()
    data = pdm.get_all_user_portfolios('shachar')
    print(data)
