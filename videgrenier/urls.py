from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (ReservationDeleteView, ReservationDetailView,
                    ReservationListView, ReservationModerateView, reservation)

app_name = 'videgrenier'
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='videgrenier/home.html'), name='home'),
    url(r'^plan$', TemplateView.as_view(template_name='videgrenier/plan.html'), name='plan'),
    url(r'^reglement$', TemplateView.as_view(template_name='videgrenier/reglement.html'), name='reglement'),
    url(r'^reservation$', reservation, name='reservation'),
    url(r'^reservation/detail$', ReservationDetailView.as_view(), name='reservation-detail'),
    url(r'^reservation/annuler$', ReservationDeleteView.as_view(), name='reservation-delete'),
    url(r'^reservation/(?P<pk>\d+)/(?P<accepte>\d)$', ReservationModerateView.as_view(), name='reservation-moderate'),
    url(r'^admin$', ReservationListView.as_view(), name='reservation-list'),
]
