from django.urls import path

from uploaded.views import uploaded


urlpatterns = [
    path('', uploaded, name='uploaded'),
]
