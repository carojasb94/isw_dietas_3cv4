from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.usuarios.urls', namespace='usuarios_app')),
    url(r'^', include('apps.dieta.urls', namespace='dietas_app')),
    url(r'^', include('apps.home.urls', namespace='home_app')),

]
