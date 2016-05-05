from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^vide-grenier/', include('videgrenier.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
