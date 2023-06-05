import json
from restaurants_info.models import storestatus, Report
from restaurants_info.timemode import compute_uptime
from datetime import datetime

def generate_report(report_id):
    report = Report(report_id=report_id, status='Running', data='')
    report.save()
    report_data = []
    stores = storestatus.query.all()
    print(stores)
    for store in stores:
        uptime, downtime = compute_uptime(store.store_id)
        report_data.append({
            'store_id': store.store_id,
            'status': store.status,
            'uptime': round(uptime, 2),
            'downtime': round(downtime, 2)
        })

    report.status = 'Complete'
    report.completed_at = datetime.utcnow()
    report.data = json.dumps(report_data)
    report.save()

    return report


def get_report_status_from_db(report_id):
    report = Report.query.filter_by(report_id=report_id).first()
    if report is None:
        return None
    else:
        return report.status

def get_report_data_from_db(report_id):
    
    report = Report.query.filter_by(report_id=report_id).first()

    if report is None:
        raise ValueError(f"No report found for report_id: {report_id}")

    return report.data

