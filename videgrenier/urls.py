from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (ReservationCreateView, ReservationDeleteView, ReservationModerateView,
                    ReservationDetailView, ReservationListView, ReservationUpdateView)

app_name = 'videgrenier'
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='videgrenier/home.html'), name='home'),
    url(r'^reservations$', ReservationListView.as_view(), name='reservation-list'),
    url(r'^reservation/(?P<pk>\d+)/(?P<accepte>\d)$', ReservationModerateView.as_view(), name='reservation-moderate'),
    url(r'^reservation/reserver$', ReservationCreateView.as_view(), name='reservation-create'),
    url(r'^reservation/annuler$', ReservationDeleteView.as_view(), name='reservation-delete'),
    url(r'^reservation/modifier$', ReservationUpdateView.as_view(), name='reservation-update'),
    url(r'^reservation$', ReservationDetailView.as_view(), name='reservation-detail'),
]
