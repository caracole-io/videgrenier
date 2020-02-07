"""Vide Grenier urls."""
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'videgrenier'
urlpatterns = [
    path('', TemplateView.as_view(template_name='videgrenier/home.html'), name='home'),
    path('plan', TemplateView.as_view(template_name='videgrenier/plan.html'), name='plan'),
    path('reglement', TemplateView.as_view(template_name='videgrenier/reglement.html'), name='reglement'),
    path('reservation', views.reservation, name='reservation'),
    path('reservation/detail', views.ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservation/annuler', views.ReservationDeleteView.as_view(), name='reservation-delete'),
    path('reservation/<int:pk>/<int:accepte>', views.ReservationModerateView.as_view(), name='reservation-moderate'),
    path('admin', views.ReservationListView.as_view(), name='reservation-list'),
    path('csv', views.csview, name='csv'),
    path('fini', views.FiniView.as_view(), name='fini'),
]
