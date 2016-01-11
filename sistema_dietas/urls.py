from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('apps.usuarios.urls', namespace='usuarios_app')),
    url(r'^', include('apps.home.urls', namespace='home_app')),
    url(r'^', include('apps.dieta.urls', namespace='dietas_app')),
    url(r'^', include('apps.chat.urls', namespace='chat_app')),
    url(r'^', include('apps.nutriologo.urls', namespace='nutriologo_app')),


    url(r'^reset/password_reset/$', 'django.contrib.auth.views.password_reset', name='reset_password_reset1'),
    url(r'^reset/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    # login with python social auth


]
