__author__ = 'metallica'
from django.conf.urls import include, url

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^test_chat', 'apps.chat.views.test_chat', name='test_chat'),
]


