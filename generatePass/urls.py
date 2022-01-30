from django.urls import path

from generatePass.views import genpass


urlpatterns = [
    path('', genpass, name='genpass'),
]
