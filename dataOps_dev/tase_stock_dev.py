import datetime

from dataOps_dev.UTILS.utils import *
if __name__ == '__main__':
   #print(get_Bar())

    bearer_token='AAIgZWNiY2VlODk0YTkxZDQ3YTMwY2ZjYTU1NjA3NjkyODjnDG83wkLysg_6PTZco1_EiX151jGkgT8nyRrIR6OC9dQx6bU5zfALHkmuHeSP5mJGhGG5cWUIWUAfiNiZmADq7ZwYdA9hDSj2ISS-lb1CPolMN0l7hY9XNxjQVi6cW-o'
    stock_index=137
    api_start_date = '2023-05-24'
    api_end_date = '2024-05-19'
    api_info = indices_EoD_by_index_from_date_to_date(bearer=bearer_token, index_id=stock_index,
                                                       start_date=api_start_date, end_date=api_end_date)
    print(api_info)
