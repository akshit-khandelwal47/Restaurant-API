import pandas as pd
import csv
import threading
from datetime import datetime, timedelta
from restaurants_info.models import storestatus
import pytz

def run():

    batch_size = 100
    # with open('/home/akshitkhandelwal/Desktop/RestaurantAPI/store status.csv','r') as file:
    #     reader = csv.DictReader(file)
    #     for row in reader:
    #         store = storestatus(store_id=row.get('store_id'),status=row.get('status'),timestamp=row.get('timestamp_utc').strip("UTC09ijmn"))
    #         store.save()
    data = pd.read_csv('/home/akshitkhandelwal/Desktop/RestaurantAPI/store status.csv',sep=',',chunksize=batch_size)
    timezones_csv = pd.read_csv('/home/akshitkhandelwal/Desktop/RestaurantAPI/timezone.csv', chunksize=batch_size)

    timezone_dict = {}
    for _, row in pd.concat(timezones_csv).iterrows():
        timezone_dict[row['store_id']] = pytz.timezone(row['timezone_str'])

    for each in data:
        each['timestamp_utc'] = pd.to_datetime(each['timestamp_utc'])

        for i, row in each.iterrows():
            store_id = row['store_id']
            status = row['status']
            timezone = timezone_dict.get(store_id,pytz.timezone('America/Chicago'))
            timestamp_local = row['timestamp_utc'].astimezone(timezone)
            store = storestatus(store_id=store_id, status=status, timestamp=timestamp_local)
            # stores = [
            #     storestatus(
            #         store_id =  row['store_id'],
            #         status = row['status'],
            #         timestamp = row['timestamp_utc'].strip("UTC")
            #     )
                
            # ]
            store.save()
            if (i+1) % batch_size == 0:
                store.save()
        store.save()
        
    # storestatus.objects.bulk_create(stores)