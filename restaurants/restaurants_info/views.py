from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
# Create your views here.

# @api_view(['GET'])
def getData(request):
    return HttpResponse("Hello")