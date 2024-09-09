from GCD_SETUP.gcp_setup import get_pool
from backend.classes_backend.stock_info import StockData
from sqlalchemy import text


class StatisticsManager:

    _instance = None
    table_name = 'stocks.tase_stock_stats'
    statistics_name = ['sharpe_ratio', 'daily_increase', 'norm_distribution']

    def __init__(self):
        self.stock_list = StockData.get_stock_list()

    def get_last_update_stock_stats_by_stats_name(self, stock_name: str, stats_name: str):
        matching_stock_index = next(
            (stock['index_id'] for stock in self.stock_list if stock['name'] == stock_name),
            None)
        if matching_stock_index is None:
            print(f"didn't found matching index for stock: {stock_name}")
            return None
        try:
            engine = get_pool()
            query = f"""
                     select 
                        stats_name,
                        index_symbol,
                        symbol_name,
                        stats_info,
                        insert_time 
                FROM
                    {self.table_name}
                    where  stats_name='{stats_name}' and index_symbol={matching_stock_index}
                    order by insert_time desc limit 1
              """
            with engine.connect() as conn:
                result = conn.execute(text(query)).fetchall()
                stats_data = result[0]

                stock_data_dict = {
                    'Stats_Name': stats_data[0],
                    'Index_Symbol': stats_data[1],
                    'Symbol_Name': stats_data[2],
                    'Stats_Info': stats_data[3],
                    'Insert_Time': stats_data[4].strftime('%Y-%m-%d'),
                }
                # stock_data_dict = json.dumps(stock_data_dict)
                return stock_data_dict
        except Exception as e:
            print(f"error occurred while running query: {e}")
            return None

    def get_all_last_update_stock_stats(self, stock_name: str):
        matching_stock_index = next(
            (stock['index_id'] for stock in self.stock_list if stock['name'] == stock_name),
            None)

        if matching_stock_index is None:
            print(f"didn't found matching index for stock: {stock_name}")
            return None

        try:
            engine = get_pool()
            query = f"""
            with max_dates as(
                            select 
                                stats_name,
                                max(insert_time) as max_insert_time
                                from  {self.table_name}
                                where index_symbol={matching_stock_index}
                                group by 1
                            )
                select 
                    a.stats_name,
                    a.stats_info,
                    a.insert_time,
                    a.index_symbol,
                    a.symbol_name
                from  {self.table_name} a inner join max_dates b 
                on a.stats_name=b.stats_name
                where 
                    a.index_symbol={matching_stock_index}
                    and b.max_insert_time=a.insert_time;
                   """
            with engine.connect() as conn:
                result = conn.execute(text(query)).fetchall()
                stock_stats_dict = {}
                for row in result:
                    # date_str = row['date'].strftime('%Y-%m-%d')
                    # Ensure date is in string format for JSON compatibility
                    stock_stats_dict[row[0]] = {
                        'stats_info': row[1],
                        'insert_time': row[2].strftime('%Y-%m-%d')
                    }
                stock_stats_dict['index_symbol'] = result[0][3]
                stock_stats_dict['symbol_name'] = result[0][4]
                # stock_stats_dict = json.dumps(stock_stats_dict)
                return stock_stats_dict

        except Exception as e:
            print(f"error occurred while running query: {e}")
            return None

    def is_stock_name_exist(self, stock_name):
        for stck in self.stock_list:
            if stck['name'] == stock_name:
                return True
        return False

    def is_stat_name_exist(self, stat_name):
        return stat_name in self.statistics_name
# if __name__ == '__main__':
#     sm = StatisticsManager()
#     data = sm.get_all_last_update_stock_stats('TA_Bond_60')
#     data2 = sm.get_last_update_stock_stats_by_stats_name('TA_Bond_60', stats_name=sm.statistics_name[0])
#     print(data)
#     print(data2)
