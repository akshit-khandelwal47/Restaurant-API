from .models import storestatus, MenuHours, TimeZone
from datetime import datetime, timedelta
import pytz


def compute_uptime(store_id, start_date=None, end_date=None):
    if not start_date:
        start_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    timezone = get_store_time(store_id)
    business_hours = get_business_hours(store_id)
    hours_open = compute_business_hours_overlap(business_hours, timezone, start_date, end_date)
    uptime = hours_open / timedelta(hours=24) * 100
    downtime = 100 - uptime

    return uptime, downtime
def get_active_status(store_id):
    active_status = storestatus.objects.filter(store_id=store_id).order_by('timestamp')
    return active_status



def get_store_time(store_id):
    timezone = TimeZone.query.filter_by(store_id=store_id).first()
    if timezone is None:
        return pytz.timezone('UTC')
    return pytz.timezone(timezone.timezone_str)

def get_business_hours(store_id):
    business_hours = MenuHours.query.filter_by(store_id=store_id).all()
    return [(mh.week_day, mh.start_time, mh.end_time) for mh in business_hours]

def compute_business_hours_overlap(business_hours, timezone, start_date, end_date):
    total_overlap = timedelta()
    for day, start_time, end_time in business_hours:
        start_time_utc = timezone.localize(datetime.combine(start_date.date(), start_time)).astimezone(pytz.utc)
        end_time_utc = timezone.localize(datetime.combine(end_date.date(), end_time)).astimezone(pytz.utc)
        if start_time_utc >= end_time_utc:
            end_time_utc += timedelta(days=1)
        business_day_start = max(start_date, start_time_utc)
        business_day_end = min(end_date, end_time_utc)
        overlap = (business_day_end - business_day_start).total_seconds() / 3600
        overlap = max(overlap, 0)
        total_overlap += timedelta(hours=overlap)
    return  compute_business_hours_overlap(business_hours, timezone, start_date, end_date)

