from django.urls import path
from .views import *
from rest_framework import routers




urlpatterns = [
    path('trigger_report/', trigger_report),
    path('get_report/', get_report),
]