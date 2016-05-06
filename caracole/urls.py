from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from .views import CaracolienUpdateView, PasswordUpdateView, UserDetailView, UserUpdateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^vide-grenier/', include('videgrenier.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profil$', UserDetailView.as_view(), name='profil'),
    url(r'^profil/caracolien$', CaracolienUpdateView.as_view(), name='profil-caracolien'),
    url(r'^profil/utilisateur$', UserUpdateView.as_view(), name='profil-user'),
    url(r'^profil/password$', PasswordUpdateView.as_view(), name='profil-password'),
]
