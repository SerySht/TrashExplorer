from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<trash_name>[a-zA-Z0-9]+)/$', views.trash_deatils, name='detail'),
]
