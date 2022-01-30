from django.urls import path

from strJsonTOCsv.views import JsontoCsv


urlpatterns = [
    path('', JsontoCsv, name='jsontocsv'),
]
