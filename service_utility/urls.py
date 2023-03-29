from django.urls import path
from service_utility.views import *

urlpatterns = [
    path('', group_list),
    path('<str:name>', group_detil),
]
