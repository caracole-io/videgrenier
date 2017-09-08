from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

from .views import profil, profil_password

app_name = 'caracole'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'old^$', RedirectView.as_view(url='http://caracole.le-pic.org'), name='old'),
    url(r'^vide-grenier/', include('videgrenier.urls')),
    url(r'^cagnottesolidaire/', include('cagnottesolidaire.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profil$', profil, name='profil'),
    url(r'^profil/password$', profil_password, name='profil-password'),
]
