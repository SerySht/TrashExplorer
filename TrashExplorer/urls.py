from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^add/$', views.add_trash, name='add_trash'),

    url(r'^(?P<trash_name>[a-zA-Z0-9]+)/$', views.trash_details, name='detail'),

    url(r'^(?P<trash_name>[a-zA-Z0-9]+)/recover/$', views.recover, name='recover'),

    url(r'^(?P<trash_name>[a-zA-Z0-9]+)/delete/$', views.delete, name='delete'),

]
