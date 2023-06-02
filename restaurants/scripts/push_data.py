import pandas as pd
import csv
import threading
from datetime import datetime, timedelta
from restaurants_info.models import storestatus,TimeZone,MenuHours
import pytz

def run():

    batch_size = 100
   
    data = pd.read_csv('/home/akshitkhandelwal/Desktop/RestaurantAPI/store status.csv',sep=',',chunksize=batch_size)
    timezones_csv = pd.read_csv('/home/akshitkhandelwal/Desktop/RestaurantAPI/timezone.csv',sep=',',chunksize=batch_size)
    menu_csv = pd.read_csv('/home/akshitkhandelwal/Desktop/RestaurantAPI/Menu hours.csv',chunksize=batch_size)

    timezone_dict = {}
    for _, row in pd.concat(timezones_csv).iterrows():
        timezone_dict[row['store_id']] = pytz.timezone(row['timezone_str'])
    import pdb;pdb.set_trace()
    for each in data:
        each['timestamp_utc'] = pd.to_datetime(each['timestamp_utc'])

        for i, row in each.iterrows():
            store_id = row['store_id']
            status = row['status']
            timezone = timezone_dict.get(store_id,pytz.timezone('America/Chicago'))
            timestamp_local = row['timestamp_utc'].astimezone(timezone)
            store = storestatus(store_id=store_id, status=status, timestamp=timestamp_local)
            store.save()
            if (i+1) % batch_size == 0:
                store.save()
        store.save()
    for each in timezones_csv:
        for i,row in each.iterrows():
            store_id = row['store_id']
            timezone_str = row['timezone_str']
            timez = TimeZone(store_id=store_id,timezone_str=timezone_str)
            timez.save()
        
            if (i+1) % batch_size == 0:
                timez.save()
        timez.save()

    for each in menu_csv:
        for i, row in each.iterrows():
            store_id = row['store_id']
            week_day = row['day']
            start_time = pd.to_datetime(row['start_time_local']).time()
            end_time = pd.to_datetime(row['end_time_local']).time()
            menu = MenuHours(store_id=store_id,week_day=week_day,start_time=start_time,end_time=end_time)
            menu.save()

            if (i+1) % batch_size == 0:
                menu.save()
        menu.save()

