from rest_framework.response import Response
from rest_framework.decorators import api_view
from restaurants_info.reports import *
from restaurants_info.models import *
import secrets
from django.http import JsonResponse
from restaurants_info.serializers import *
# Create your views here.




@api_view(['POST'])
def trigger_report():
    try:
        report_id = secrets.token_urlsafe(16)
        generate_report(report_id)
        return JsonResponse({'report_id': report_id, 'message': 'Hello', 'status_code':200})
    except Exception as e:
        return JsonResponse({'message': 'Failed', 'status_code': 500, 'Error': str(e)})

@api_view(['GET'])
def get_report(request):
    try:
        report_id = request.args.get('report_id')
        if not report_id:
            return JsonResponse({'error': 'Missing report ID', "error_code": 400})

        report_status = get_report_status_from_db(report_id)
        if not report_status:
            return JsonResponse({'error': 'Invalid report ID',"error_code": 400})

        if report_status == 'Running':
            return JsonResponse({'status': 'Running','message': 'Success', 'error_code':200})
        elif report_status == 'Complete':
            report_data = get_report_data_from_db(report_id)
            if report_data:
                return Response(report_data, mimetype='text/csv')
            else:
                return JsonResponse({'error': 'Failed to retrieve report data',"error_code": 400})
        else:
            return JsonResponse({'error': 'Invalid report status',"error_code": 400})
    except Exception as e:
        return JsonResponse({ "error_message": "Something went Wrong", "Error_code":500, "error":str(e)})