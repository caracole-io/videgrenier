from django.conf.urls import url
from django.views.generic import ListView

from .models import Reservation

app_name = 'videgrenier'
urlpatterns = [
    url(r'^$', ListView.as_view(model=Reservation), name='reservation-list'),
]
