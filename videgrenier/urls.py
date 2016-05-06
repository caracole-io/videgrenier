from django.conf.urls import url

from .views import (HomeView, ReservationCreateView, ReservationDeleteView,
                    ReservationDetailView, ReservationListView, ReservationUpdateView)

app_name = 'videgrenier'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^reservations$', ReservationListView.as_view(), name='reservation-list'),
    url(r'^reservation/(?P<pk>\d+)/(?P<accepte>\d)$', ReservationUpdateView.as_view(), name='reservation-update'),
    url(r'^reservation/reserver$', ReservationCreateView.as_view(), name='reservation-create'),
    url(r'^reservation/annuler$', ReservationDeleteView.as_view(), name='reservation-delete'),
    url(r'^reservation$', ReservationDetailView.as_view(), name='reservation-detail'),
]
