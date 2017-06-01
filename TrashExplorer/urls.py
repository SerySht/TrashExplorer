from django.conf.urls import url, include
from django.contrib import admin
from TrashExplorer import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
]
