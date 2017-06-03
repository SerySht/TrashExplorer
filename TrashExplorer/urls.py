from django.conf.urls import url, include
from django.contrib import admin
from TrashExplorer import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^(?P<trash_id>[0-9]+)/$', views.trash_deatils, name='detail'),
]
