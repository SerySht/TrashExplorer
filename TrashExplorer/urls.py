from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^add_trash/$', views.add_trash, name='add_trash'),

    url(r'^(?P<trash_id>[0-9]+)/$', views.trash_details, name='trash_details'),

    url(r'^(?P<trash_id>[0-9]+)/recover/$', views.recover, name='recover'),

    url(r'^(?P<trash_id>[0-9]+)/delete/$', views.delete, name='delete'),

    url(r'^(?P<trash_id>[0-9]+)/wipe_trash/$', views.wipe_trash, name='wipe_trash'),

    url(r'^(?P<trash_id>[0-9]+)/delete_trash/$', views.delete_trash, name='delete_trash'),

]
