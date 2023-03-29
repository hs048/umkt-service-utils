from django.urls import path
from umkt_service_utils.views import *

urlpatterns = [
    path('', group_list),
    path('<str:name>', group_detil),
]
