from django.urls import path
from django.views.generic import TemplateView

from .views import (csview, ReservationDeleteView, ReservationDetailView,
                    ReservationListView, ReservationModerateView, reservation)

app_name = 'videgrenier'
urlpatterns = [
    path('', TemplateView.as_view(template_name='videgrenier/home.html'), name='home'),
    path('plan', TemplateView.as_view(template_name='videgrenier/plan.html'), name='plan'),
    path('reglement', TemplateView.as_view(template_name='videgrenier/reglement.html'), name='reglement'),
    path('reservation', reservation, name='reservation'),
    path('reservation/detail', ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservation/annuler', ReservationDeleteView.as_view(), name='reservation-delete'),
    path('reservation/<int:pk>/<int:accepte>', ReservationModerateView.as_view(), name='reservation-moderate'),
    path('admin', ReservationListView.as_view(), name='reservation-list'),
    path('csv', csview, name='csv'),
    path('fini', TemplateView.as_view(template_name='videgrenier/fini.html'), name='fini'),
]
